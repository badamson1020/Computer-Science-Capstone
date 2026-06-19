"""CRUD operations and aggregation for the animal shelter MongoDB collection.

Provides methods for creating, reading, updating, deleting, and aggregating
animal records stored in MongoDB. Database credentials are loaded from a
private .env file to prevent exposure in public repositories.
"""

from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables from .env file.
# Credentials are stored externally to prevent exposure in public repositories,
# addressing a recognized secure coding vulnerability.
load_dotenv()


class ShelterCRUD:
    """Provide CRUD operations and aggregation for the animal shelter database.

    Connects to a MongoDB collection containing animal shelter records and
    exposes methods for creating, reading, updating, deleting, and aggregating
    documents. All connection parameters are loaded from a private .env file
    rather than being hardcoded in the source code.
    """

    def __init__(self) -> None:
        """Initialize the ShelterCRUD instance and establish a MongoDB connection.

        Connection parameters are loaded from a private .env file rather than
        being hardcoded, preventing exposure of sensitive credentials in
        public repositories.

        Raises:
            Exception: If the connection to MongoDB fails.
        """
        try:
            user = os.getenv("MONGO_USER")
            password = os.getenv("MONGO_PASS")
            host = os.getenv("MONGO_HOST", "localhost")
            port = int(os.getenv("MONGO_PORT", 27017))
            db = os.getenv("MONGO_DB", "AAC")
            col = os.getenv("MONGO_COL", "animals")

            self._client = MongoClient(
                f"mongodb://{user}:{password}@{host}:{port}/{db}",
                authSource=os.getenv("MONGO_AUTH", "AAC")
            )
            self._database = self._client[db]
            self._collection = self._database[col]

        except Exception as e:
            raise Exception(f"Connection failed to MongoDB: {e}")

    def _next_record(self) -> int:
        """Return the next available sequential record number.

        Examines the highest rec_num value in the collection and returns
        the next value. A sequential record number is assigned to each document
        on creation to provide a simple readable identifier independent of
        MongoDB's internal ObjectId. Private method called only by create().

        Returns:
            Next available record number as an integer, or 1 if no records exist.
        """
        try:
            # Sorts records in descending order to find the last number used
            last = self._collection.find_one(sort=[("rec_num", -1)])
            if last and "rec_num" in last:
                return last["rec_num"] + 1
            else:
                return 1
        except Exception as e:
            print(f"Unexpected error in _next_record: {e}")
            return 1

    def create(self, data: dict) -> bool:
        """Insert a document into the collection with a unique rec_num value.

        Args:
            data: Dictionary containing the document to insert.

        Returns:
            True for successful insert, else False.

        Raises:
            ValueError: If data is None, not a dictionary, or an empty dictionary.
        """
        if data is None:
            raise ValueError("Data cannot be null.")
        elif not isinstance(data, dict):
            raise ValueError("Data must be a dictionary.")
        elif len(data) == 0:
            raise ValueError("Data cannot be an empty dictionary.")

        try:
            data["rec_num"] = self._next_record()
            document_insertion = self._collection.insert_one(data)
            return True if document_insertion.inserted_id else False
        except Exception as e:
            print(f"An error occurred while inserting a document: {e}")
            return False

    def read(self, query: dict) -> list[dict]:
        """Retrieve documents from the collection matching the given query.

        An empty query {} is intentionally allowed following standard MongoDB
        and CRUD conventions where find({}) returns all documents. Unlike delete()
        and update() which block empty queries to prevent catastrophic data loss,
        read() with an empty query is a legitimate and safe operation used to
        retrieve all records when needed. Pass {} to retrieve all documents.

        Args:
            query: Dictionary containing values for comparison and search.

        Returns:
            List of matching documents, or empty list if no matches found.

        Raises:
            ValueError: If query is None or not a dictionary.
        """
        if query is None:
            raise ValueError("Query cannot be null.")
        elif not isinstance(query, dict):
            raise ValueError("Query must be a dictionary.")

        try:
            found = self._collection.find(query)
            documents_listed = list(found)
            return documents_listed if documents_listed else []
        except Exception as e:
            print(f"An error occurred while attempting to query the collection: {e}")
            return []

    def update(self, query: dict, update_values: dict, many: bool = False) -> int:
        """Update one or more documents in the collection.

        Args:
            query: Dictionary containing values for comparison and search.
            update_values: Dictionary of update operators such as {"$set"}.
            many: If True uses update_many, else update_one.

        Returns:
            Number of documents updated.

        Raises:
            ValueError: If query or update_values are None, not dictionaries,
                or empty dictionaries.
        """
        if query is None or update_values is None:
            raise ValueError("Query and update values cannot be null.")
        elif not isinstance(query, dict) or not isinstance(update_values, dict):
            raise ValueError("Query and update values must be dictionaries.")
        elif len(query) == 0 or len(update_values) == 0:
            raise ValueError("Query and update values cannot be empty dictionaries.")

        try:
            if many:
                result = self._collection.update_many(query, update_values)
            else:
                result = self._collection.update_one(query, update_values)
            return result.modified_count
        except Exception as e:
            print(f"An error occurred while updating: {e}")
            return 0

    def delete(self, query: dict, many: bool = False) -> int:
        """Delete one or more documents from the collection.

        Empty queries are explicitly blocked to prevent accidentally deleting
        all documents in the collection, which would be catastrophic for the
        shelter database.

        Args:
            query: Dictionary containing values for comparison and search.
            many: If True uses delete_many, else delete_one.

        Returns:
            Number of documents deleted.

        Raises:
            ValueError: If query is None, not a dictionary, or an empty dictionary.
        """
        if query is None:
            raise ValueError("Query cannot be null.")
        elif not isinstance(query, dict):
            raise ValueError("Query must be a dictionary.")
        elif len(query) == 0:
            raise ValueError("Query cannot be an empty dictionary.")

        try:
            if many:
                result = self._collection.delete_many(query)
            else:
                result = self._collection.delete_one(query)
            return result.deleted_count
        except Exception as e:
            print(f"An error occurred while deleting: {e}")
            return 0

    def read_distinct(self, field: str, filter_query: dict | None = None) -> list:
        """Return a list of distinct values for the specified field.

        An optional filter query limits which documents are considered.
        For example, retrieving distinct breeds for dogs only rather than
        all animal types in the collection. An empty filter is acceptable
        here since distinct() returns a small summarized list of unique values
        rather than full documents, making the risk negligible.

        Args:
            field: The field name to get distinct values for.
            filter_query: Optional dictionary to filter documents before
                getting distinct values.

        Returns:
            List of distinct values for the specified field.

        Raises:
            ValueError: If field is None or empty string.
        """
        if field is None:
            raise ValueError("Field cannot be null.")
        elif len(field) == 0:
            raise ValueError("Field cannot be empty.")

        try:
            query = filter_query if filter_query is not None else {}
            return list(self._collection.distinct(field, query))
        except Exception as e:
            print(f"An error occurred while getting distinct values: {e}")
            return []

    def aggregate(self, pipeline: list) -> list[dict]:
        """Execute a MongoDB aggregation pipeline and return the results.

        The method is intentionally generic, accepting any valid pipeline
        rather than building one internally. This keeps the CRUD module focused
        on database communication while allowing callers to define their own
        aggregation logic, making the method reusable for any future pipeline
        needs beyond the statistics panel.

        Performing aggregation at the database level rather than retrieving raw
        records and processing them in Python is more efficient and scalable,
        particularly for large collections.

        Args:
            pipeline: List of MongoDB aggregation pipeline stage dictionaries.

        Returns:
            List of result documents returned by the aggregation pipeline.

        Raises:
            ValueError: If pipeline is None, not a list, or an empty list.
        """
        if pipeline is None:
            raise ValueError("Pipeline cannot be null.")
        elif not isinstance(pipeline, list):
            raise ValueError("Pipeline must be a list.")
        elif len(pipeline) == 0:
            raise ValueError("Pipeline cannot be empty.")

        try:
            results = list(self._collection.aggregate(pipeline))
            return results if results else []
        except Exception as e:
            print(f"An error occurred while executing the aggregation pipeline: {e}")
            return []

    def close(self) -> None:
        """Close the MongoDB client connection and free up resources.

        Should be called when the ShelterCRUD instance is no longer needed
        to prevent resource leaks and ensure clean shutdown.
        """
        self._client.close()