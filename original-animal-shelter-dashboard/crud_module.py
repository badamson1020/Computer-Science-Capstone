# Python Code to perform CRUD operations 

from pymongo import MongoClient 
from bson.objectid import ObjectId 

class AnimalShelter(object): 
    # Initializing the MongoClient. This helps to access the MongoDB 
    # databases and collections. This is hard-coded to use the aac 
    # database, the animals collection, and the aac user.      
    def __init__(self, user="aacuser", password="Gorgan12!", host="localhost", port=27017, db="aac", col="animals"):

        # Initialize Connection 
        # Try/catch to handle connection issues to the db
        try:
            # Create string to connect to MongoDB
            self.client = MongoClient(f"mongodb://{user}:{password}@{host}:{port}")
            
            # Connect to the db and collection
            self.database = self.client[db]
            self.collection = self.database[col]
        
        except Exception as e:
            raise Exception(f"Connection failed to MongoDB: {e}")

            
    # Create a method to return the next available record number for use in the create method
    def next_record(self):
        """
        Looks for the next record number not currently in use.
        Examines the highest "rec_num" in the collection
        and then returns the next value.
        If no record number exists starts at 1.
        """
        try:
            #Sorts records in descending order to find the last number used
            last = self.collection.find_one(sort=[("rec_num", -1)])
            if last and "rec_num" in last:
                return last["rec_num"] + 1
            else:
                return 1 
        except Exception as e:
            print(f"Unexpected error in next_record: {e}")
            return 1
    
    
    def create(self, data):
        """
        Add a document into the MongoDB collection with an associated
        unique "rec_num" value.
        :param data: dictionary with values and a unique key-value pair
        :return: True for successful insert, else False
        """
        if data is not None and isinstance(data, dict):
            try:
                # Insert documents with generated rec_num
                data["rec_num"] = self.next_record()
                    
                document_insertion = self.collection.insert_one(data)
                return True if document_insertion.inserted_id else False
            except Exception as e:
                print(f"An error occurred while inserting a document: {e}")
                return False
        else:
            raise ValueError("Data cannot be an empty dictionary")
       

    def read(self, query):
        """
        Search for documents from the collection.
        :param query: dictionary containing values for comparison and search
        :return: list of documents or empty list if no matching values
        """
        if query is not None and isinstance(query, dict):
            try:
                found = self.collection.find(query)
                documents_listed = list(found)                        # convert found documents into a list
                return documents_listed if documents_listed else []   # return the found list or an empty list
            except Exception as e:
                print(f"An error occurred while attempting to query the collection: {e}")
                return []
        else:
            raise ValueError("Query cannot be an empty dictionary")
            
            
    def update(self, query, update_values, many=False):
        """
        Update document(s) in the collection.
        :param query: dictionary containing values for comparison and search
        :param update_values: dictionary of update operators such as {"$set"}
        :param many: if True update_many, else update_one
        :return: number of documents updated
        """
        if not isinstance(query, dict) or not isinstance(update_values, dict):
            raise ValueError("Both query and update_values must be dictionaries")

        try:
            if many:
                result = self.collection.update_many(query, update_values)
            else:
                result = self.collection.update_one(query, update_values)
            return result.modified_count
        except Exception as e:
            print(f"An error occurred while updating: {e}")
            return 0
        

    def delete(self, query, many=False):
        """
        Delete document(s) from the collection.
        :param query: dictionary containing values for comparison and search
        :param many: if True delete_many, else delete_one
        :return: number of documents deleted
        """
        if not isinstance(query, dict):
            raise ValueError("Query must be a dictionary")

        try:
            if many:
                result = self.collection.delete_many(query)
            else:
                result = self.collection.delete_one(query)
            return result.deleted_count
        except Exception as e:
            print(f"An error occurred while deleting: {e}")
            return 0