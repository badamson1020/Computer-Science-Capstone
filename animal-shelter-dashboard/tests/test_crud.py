"""Test suite for the ShelterCRUD module.

Covers happy path and error path scenarios for all CRUD methods and the
aggregate method. Tests run against a dedicated AAC_Test database to ensure
real shelter data is never affected during testing.
"""

import unittest
from dotenv import load_dotenv
load_dotenv(".env.test", override=True)  # loads test env variables FIRST
from models.shelter_crud import ShelterCRUD  # ShelterCRUD reads .env.test variables when imported


class TestShelterCRUD(unittest.TestCase):
    """Test the ShelterCRUD module against a dedicated test database.

    All tests operate on AAC_Test which mirrors the production database,
    ensuring real shelter data is never at risk. A unique animal_type value
    of 'Test' identifies and cleans up test documents to maintain a consistent
    test environment between runs. Only public methods are used throughout.
    Internal collection access is intentionally avoided to test behavior
    not implementation details.
    """

    # Unique marker used to identify test documents in the collection.
    # No records from the test database should have this animal_type value.
    # This ensures a consistent test environment between tests and helps identify
    # when tests may have crashed unexpectedly in a previous test run.
    TEST_ANIMAL_TYPE = "Test"

    # Sample test document used across multiple tests
    TEST_DOCUMENT = {
        "name": "Goddard",
        "animal_type": TEST_ANIMAL_TYPE,
        "breed": "Robot Dog",
        "age_upon_outcome_in_weeks": 52.0,
        "sex_upon_outcome": "Intact Male",
        "location_lat": 30.75,
        "location_long": -97.48,
        "outcome_type": "Adoption",
        "animal_id": "TEST001"
    }

    # Second test document used for many=True tests
    TEST_DOCUMENT_2 = {
        "name": "Sparky",
        "animal_type": TEST_ANIMAL_TYPE,
        "breed": "Electric Dog",
        "age_upon_outcome_in_weeks": 26.0,
        "sex_upon_outcome": "Intact Female",
        "location_lat": 30.85,
        "location_long": -97.68,
        "outcome_type": "Adoption",
        "animal_id": "TEST002"
    }

    @classmethod
    def setUpClass(cls) -> None:
        """Check for existing test documents before any tests run.

        Checks for documents with animal_type 'Test' in the test database to ensure
        a clean starting state. Leftover documents from a previous test run that did
        not complete cleanly would cause false failures. Aborts the entire test suite
        if any are found so they can be reviewed and removed before retrying.
        Closes the connection immediately after the check since it is no longer needed.
        """
        shelter_check = ShelterCRUD()
        existing_test_docs = shelter_check.read({"animal_type": cls.TEST_ANIMAL_TYPE})
        shelter_check.close()

        if existing_test_docs:
            raise Exception(
                f"Found {len(existing_test_docs)} existing document(s) with "
                f"animal_type '{cls.TEST_ANIMAL_TYPE}' in the collection. "
                f"Tests aborted to prevent data corruption. "
                f"Please review and remove these documents before running tests. "
                f"Documents found: {existing_test_docs}"
            )

    def setUp(self) -> None:
        """Create a fresh connection and insert two test documents before each test.

        Test documents are identified by animal_type 'Test' and cleaned up after
        every test to maintain a consistent test environment between runs.
        dict() creates a shallow copy before passing to create() to prevent
        create() from modifying the shared class level TEST_DOCUMENT constant
        when it adds the rec_num field to the inserted document.
        """
        self.shelter = ShelterCRUD()
        # dict() creates a shallow copy before passing to create() to prevent
        # create() from modifying the shared class level TEST_DOCUMENT constant
        # when it adds the rec_num field to the inserted document.
        self.shelter.create(dict(self.TEST_DOCUMENT))
        self.shelter.create(dict(self.TEST_DOCUMENT_2))

    def tearDown(self) -> None:
        """Remove all test documents and close the connection after each test.

        Deletes all documents with animal_type 'Test' using the public delete method,
        ensuring a consistent state before the next test run. Closes the MongoDB
        connection to free up resources after each test.
        """
        self.shelter.delete({"animal_type": self.TEST_ANIMAL_TYPE}, many=True)
        self.shelter.close()

    ###########################################################
    # Test create
    ###########################################################

    def test_create_with_valid_document_returns_true(self):
        new_doc = {"name": "TestCreate", "animal_type": self.TEST_ANIMAL_TYPE, "breed": "Test Breed"}
        result = self.shelter.create(new_doc)
        self.assertTrue(result)

    def test_create_assigns_sequential_rec_num_to_inserted_document(self):
        # Reads the test documents inserted in setUp to find the current highest rec_num.
        # Since setUp inserts the most recent documents their rec_num values represent
        # the current maximum in the collection.
        test_docs = self.shelter.read({"animal_type": self.TEST_ANIMAL_TYPE})
        current_max = max(doc["rec_num"] for doc in test_docs)

        # Creates a new document and verifies its rec_num is exactly one higher
        # than the current maximum, confirming sequential record numbering.
        new_doc = {"name": "TestRecNum", "animal_type": self.TEST_ANIMAL_TYPE, "breed": "Test Breed"}
        self.shelter.create(new_doc)
        inserted = self.shelter.read({"name": "TestRecNum"})

        self.assertEqual(1, len(inserted))
        self.assertEqual(current_max + 1, inserted[0]["rec_num"])

    def test_create_with_null_value_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.shelter.create(None)

    def test_create_with_non_dictionary_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.shelter.create("not a dictionary")

    def test_create_with_empty_dictionary_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.shelter.create({})

    ###########################################################
    # Test read
    ###########################################################

    def test_read_existing_shelter_data_returns_non_empty_list(self):
        # Verifies read works correctly against pre-existing test shelter data
        result = self.shelter.read({"animal_type": "Dog"})
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

    def test_read_inserted_test_document_returns_correct_document(self):
        # Verifies read correctly retrieves a document we inserted
        result = self.shelter.read({"animal_id": "TEST001"})
        self.assertEqual(1, len(result))
        self.assertEqual("Goddard", result[0]["name"])

    def test_read_with_no_matching_documents_returns_empty_list(self):
        result = self.shelter.read({"animal_id": "NONEXISTENT999"})
        self.assertEqual([], result)

    def test_read_with_null_value_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.shelter.read(None)

    def test_read_with_non_dictionary_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.shelter.read("not a dictionary")

    def test_read_with_empty_dictionary_returns_all_documents(self):
        # Verifies read({}) follows standard CRUD convention and returns all documents
        # rather than raising an error, unlike delete and update which block empty
        # queries to prevent catastrophic data loss.
        result = self.shelter.read({})
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

    ###########################################################
    # Test update
    ###########################################################

    def test_update_with_valid_query_updates_document_successfully(self):
        # Verifies update modifies the correct document and returns modified count
        # then reads the document back using the public read method to verify the change
        result = self.shelter.update(
            {"animal_id": "TEST001"},
            {"$set": {"breed": "Updated Robot Dog"}}
        )
        self.assertEqual(1, result)
        updated = self.shelter.read({"animal_id": "TEST001"})
        self.assertEqual("Updated Robot Dog", updated[0]["breed"])

    def test_update_with_many_true_updates_multiple_documents(self):
        # Verifies update with many=True modifies all matching documents
        # then reads them back to confirm both documents were actually updated
        result = self.shelter.update(
            {"animal_type": self.TEST_ANIMAL_TYPE},
            {"$set": {"breed": "Batch Updated"}},
            many=True
        )
        self.assertEqual(2, result)
        updated_docs = self.shelter.read({"animal_type": self.TEST_ANIMAL_TYPE})
        for doc in updated_docs:
            self.assertEqual("Batch Updated", doc["breed"])

    def test_update_with_null_query_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.shelter.update(None, {"$set": {"breed": "Test"}})

    def test_update_with_null_update_values_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.shelter.update({"animal_id": "TEST001"}, None)

    def test_update_with_non_dictionary_query_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.shelter.update("not a dictionary", {"$set": {"breed": "Test"}})

    def test_update_with_empty_query_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.shelter.update({}, {"$set": {"breed": "Test"}})

    def test_update_with_empty_update_values_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.shelter.update({"animal_id": "TEST001"}, {})

    ###########################################################
    # Test delete
    ###########################################################

    def test_delete_with_valid_query_deletes_document_successfully(self):
        # Verifies delete removes the correct document and returns deleted count
        # then reads back to confirm the document no longer exists
        result = self.shelter.delete({"animal_id": "TEST001"})
        self.assertEqual(1, result)
        deleted = self.shelter.read({"animal_id": "TEST001"})
        self.assertEqual([], deleted)

    def test_delete_with_many_true_deletes_multiple_documents(self):
        # Verifies delete with many=True removes all matching documents
        # then reads back to confirm no test documents remain
        result = self.shelter.delete(
            {"animal_type": self.TEST_ANIMAL_TYPE},
            many=True
        )
        self.assertEqual(2, result)
        deleted_docs = self.shelter.read({"animal_type": self.TEST_ANIMAL_TYPE})
        self.assertEqual([], deleted_docs)

    def test_delete_with_null_value_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.shelter.delete(None)

    def test_delete_with_non_dictionary_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.shelter.delete("not a dictionary")

    def test_delete_with_empty_dictionary_raises_value_error(self):
        # Verifies empty query is rejected. An empty query would match and
        # delete all 10,000 shelter records which is the most dangerous
        # gap in the codebase and must be explicitly prevented.
        # If the validation fails in this test setting the production
        # database is secure, since these tests are run on a separate test database.
        with self.assertRaises(ValueError):
            self.shelter.delete({})

    ###########################################################
    # Test read_distinct
    ###########################################################

    def test_read_distinct_returns_list_of_dog_breeds(self):
        # Verifies read_distinct returns a non-empty list of breed values
        # when filtered to dogs only. Confirms the filter query works correctly
        # by checking that known dog breeds exist in the results and that
        # non-dog animal types are not present.
        result = self.shelter.read_distinct("breed", {"animal_type": "Dog"})
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        # Verify known dog breeds are present in the results
        self.assertIn("Labrador Retriever Mix", result)
        self.assertIn("German Shepherd", result)
        # Verify test document breeds are not present since they are not dogs
        self.assertNotIn("Robot Dog", result)
        self.assertNotIn("Electric Dog", result)

    def test_read_distinct_returns_no_duplicates(self):
        # Verifies read_distinct returns unique values only.
        # The result list should have the same length as a set of the same values.
        result = self.shelter.read_distinct("breed", {"animal_type": "Dog"})
        self.assertEqual(len(result), len(set(result)))

    def test_read_distinct_filter_query_excludes_non_matching_documents(self):
        # Verifies the filter query correctly limits results.
        # Dog breeds should not appear when filtering for test documents only.
        result = self.shelter.read_distinct("breed", {"animal_type": self.TEST_ANIMAL_TYPE})
        self.assertIn("Robot Dog", result)
        self.assertIn("Electric Dog", result)
        self.assertEqual(2, len(result))

    def test_read_distinct_returns_empty_list_for_no_matching_documents(self):
        # Verifies read_distinct returns empty list when no documents match the filter
        result = self.shelter.read_distinct("breed", {"animal_type": "NONEXISTENT"})
        self.assertEqual([], result)

    def test_read_distinct_with_null_field_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.shelter.read_distinct(None)

    def test_read_distinct_with_empty_field_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.shelter.read_distinct("")

    ###########################################################
    # Test aggregate
    ###########################################################

    def test_aggregate_with_valid_pipeline_returns_non_empty_list(self):
        # Verifies aggregate executes a valid pipeline and returns results.
        # Uses a simple count pipeline that will always return a result
        # as long as the collection has documents.
        result = self.shelter.aggregate([
            {"$group": {"_id": None, "count": {"$sum": 1}}}
        ])
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

    def test_aggregate_count_pipeline_returns_correct_structure(self):
        # Verifies the result contains the expected key from the pipeline
        result = self.shelter.aggregate([
            {"$group": {"_id": None, "count": {"$sum": 1}}}
        ])
        self.assertIn("count", result[0])

    def test_aggregate_match_pipeline_filters_correctly(self):
        # Verifies a $match stage correctly filters documents.
        # Test documents have animal_type "Test" which should
        # return exactly the two documents inserted in setUp.
        result = self.shelter.aggregate([
            {"$match": {"animal_type": self.TEST_ANIMAL_TYPE}},
            {"$count": "total"}
        ])
        self.assertEqual(1, len(result))
        self.assertEqual(2, result[0]["total"])

    def test_aggregate_with_facet_returns_multiple_calculations(self):
        # Verifies $facet stage runs multiple calculations simultaneously
        # and returns all results in a single response object
        result = self.shelter.aggregate([
            {"$match": {"animal_type": self.TEST_ANIMAL_TYPE}},
            {"$facet": {
                "totalCount": [{"$count": "total"}],
                "byBreed": [
                    {"$group": {"_id": "$breed", "count": {"$sum": 1}}}
                ]
            }}
        ])
        self.assertEqual(1, len(result))
        self.assertIn("totalCount", result[0])
        self.assertIn("byBreed", result[0])

    def test_aggregate_with_null_pipeline_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.shelter.aggregate(None)

    def test_aggregate_with_non_list_pipeline_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.shelter.aggregate({"$match": {}})

    def test_aggregate_with_empty_pipeline_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.shelter.aggregate([])


if __name__ == "__main__":
    unittest.main()
