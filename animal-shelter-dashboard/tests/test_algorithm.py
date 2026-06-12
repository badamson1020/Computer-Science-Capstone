"""Test suite for the weighted matching algorithm functions.

Covers calculate_match_score and get_scored_results with a variety of dog
and criteria combinations to verify scoring accuracy, partial matching,
case insensitivity, age buffer behavior, threshold filtering, and sort order.
"""

import unittest
from models.algorithm import calculate_match_score, get_scored_results


class TestAlgorithm(unittest.TestCase):
    """Test the weighted matching algorithm functions.

    Uses a BASE_DOG that matches no criteria in STANDARD_CRITERIA by design.
    Each test overrides exactly one or more fields to isolate specific criteria,
    ensuring scores are predictable and unambiguous.

    Age buffer calculations for STANDARD_CRITERIA (age_min=30, age_max=155):
        age_range = 125, buffer = 25
        Lower buffer boundary = 5, Upper buffer boundary = 180

    MIN_SCORE_THRESHOLD is defined in algorithm.py and controls which dogs are
    included in get_scored_results output. Tests reference its current value of 55
    in comments. If the threshold changes test expectations may need to be reviewed.
    """

    ###########################################################
    # Standard criteria. Weights sum to 100.
    ###########################################################

    STANDARD_CRITERIA = {
        "breeds": ["Labrador Retriever Mix"],
        "sex": ["Intact Female"],
        "age_min": 30,
        "age_max": 155,
        "breed_weight": 50,
        "sex_weight": 20,
        "age_weight": 30
    }

    ###########################################################
    # Base dog: matches no criteria in STANDARD_CRITERIA.
    # Used as foundation for single criterion isolation tests.
    ###########################################################

    BASE_DOG = {
        "breed": "Poodle",
        "sex_upon_outcome": "Intact Male",
        "age_upon_outcome_in_weeks": 200.0
    }

    ###########################################################
    # Named dogs: used across multiple get_scored_results tests
    ###########################################################

    # Matches all criteria scores 100. MIN_SCORE_THRESHOLD is currently 55.
    DOG_PERFECT_MATCH = {
        "breed": "Labrador Retriever Mix",
        "sex_upon_outcome": "Intact Female",
        "age_upon_outcome_in_weeks": 92.0
    }

    # Matches breed and sex but not age so scores 70, above MIN_SCORE_THRESHOLD of 55
    DOG_BREED_AND_SEX_MATCH = {
        "breed": "Labrador Retriever Mix",
        "sex_upon_outcome": "Intact Female",
        "age_upon_outcome_in_weeks": 200.0
    }

    ###########################################################
    # Test calculate_match_score: Breed scoring
    ###########################################################

    def test_exact_breed_match_returns_full_breed_weight(self):
        # Only breed matches. Score should equal breed weight only (50).
        dog = {**self.BASE_DOG, "breed": "Labrador Retriever Mix"}
        score = calculate_match_score(dog, self.STANDARD_CRITERIA)
        self.assertEqual(50.0, score)

    def test_exact_breed_match_wrong_casing_returns_full_breed_weight(self):
        # Verifies case-insensitive exact breed matching.
        # "LABRADOR RETRIEVER MIX" should match "Labrador Retriever Mix."
        dog = {**self.BASE_DOG, "breed": "LABRADOR RETRIEVER MIX"}
        score = calculate_match_score(dog, self.STANDARD_CRITERIA)
        self.assertEqual(50.0, score)

    def test_partial_breed_match_selected_in_dog_returns_half_breed_weight(self):
        # Verifies partial match where selected breed is substring of dog breed.
        # Selected "Labrador" should partially match dog breed "Labrador Retriever Mix"
        dog = {**self.BASE_DOG, "breed": "Labrador Retriever Mix"}
        criteria = {**self.STANDARD_CRITERIA, "breeds": ["Labrador"]}
        score = calculate_match_score(dog, criteria)
        self.assertEqual(25.0, score)

    def test_partial_breed_match_dog_in_selected_returns_half_breed_weight(self):
        # Verifies partial match where dog breed is substring of selected breed.
        # Dog breed "Labrador" should partially match selected "Labrador Retriever Mix"
        dog = {**self.BASE_DOG, "breed": "Labrador"}
        score = calculate_match_score(dog, self.STANDARD_CRITERIA)
        self.assertEqual(25.0, score)

    def test_no_breed_match_returns_zero_breed_score(self):
        # Sex and age match, only breed does not match.
        # Score should equal sex weight + age weight (20 + 30 = 50)
        # confirming breed contributed zero when it did not match.
        dog = {**self.BASE_DOG,
               "sex_upon_outcome": "Intact Female",
               "age_upon_outcome_in_weeks": 92.0}
        score = calculate_match_score(dog, self.STANDARD_CRITERIA)
        self.assertEqual(50.0, score)

    ###########################################################
    # Test calculate_match_score: Sex scoring
    ###########################################################

    def test_sex_match_returns_full_sex_weight(self):
        # Only sex matches, score should equal sex weight only (20)
        dog = {**self.BASE_DOG, "sex_upon_outcome": "Intact Female"}
        score = calculate_match_score(dog, self.STANDARD_CRITERIA)
        self.assertEqual(20.0, score)

    def test_sex_match_wrong_casing_returns_full_sex_weight(self):
        # Verifies case-insensitive sex matching.
        # "INTACT FEMALE" should match "Intact Female."
        dog = {**self.BASE_DOG, "sex_upon_outcome": "INTACT FEMALE"}
        score = calculate_match_score(dog, self.STANDARD_CRITERIA)
        self.assertEqual(20.0, score)

    def test_no_sex_match_returns_zero_sex_score(self):
        # Breed and age match, only sex does not match.
        # Score should equal breed weight + age weight (50 + 30 = 80)
        # confirming sex contributed zero when it did not match.
        dog = {**self.BASE_DOG,
               "breed": "Labrador Retriever Mix",
               "age_upon_outcome_in_weeks": 92.0}
        score = calculate_match_score(dog, self.STANDARD_CRITERIA)
        self.assertEqual(80.0, score)

    ###########################################################
    # Test calculate_match_score: Age scoring
    ###########################################################

    def test_age_exactly_at_minimum_boundary_returns_full_age_weight(self):
        # Edge case, age exactly at minimum boundary (30) should get full weight (30)
        dog = {**self.BASE_DOG, "age_upon_outcome_in_weeks": 30.0}
        score = calculate_match_score(dog, self.STANDARD_CRITERIA)
        self.assertEqual(30.0, score)

    def test_age_exactly_at_maximum_boundary_returns_full_age_weight(self):
        # Edge case, age exactly at maximum boundary (155) should get full weight (30)
        dog = {**self.BASE_DOG, "age_upon_outcome_in_weeks": 155.0}
        score = calculate_match_score(dog, self.STANDARD_CRITERIA)
        self.assertEqual(30.0, score)

    def test_age_within_range_returns_full_age_weight(self):
        # Age comfortably within range should get full weight (30)
        dog = {**self.BASE_DOG, "age_upon_outcome_in_weeks": 92.0}
        score = calculate_match_score(dog, self.STANDARD_CRITERIA)
        self.assertEqual(30.0, score)

    def test_age_at_lower_buffer_boundary_returns_half_age_weight(self):
        # Edge case, age exactly at lower 20% buffer boundary (5) should get half weight (15)
        # age_range=125, buffer=25, lower boundary = 30 - 25 = 5
        dog = {**self.BASE_DOG, "age_upon_outcome_in_weeks": 5.0}
        score = calculate_match_score(dog, self.STANDARD_CRITERIA)
        self.assertEqual(15.0, score)

    def test_age_at_upper_buffer_boundary_returns_half_age_weight(self):
        # Edge case, age exactly at upper 20% buffer boundary (180) should get half weight (15)
        # age_range=125, buffer=25, upper boundary = 155 + 25 = 180
        dog = {**self.BASE_DOG, "age_upon_outcome_in_weeks": 180.0}
        score = calculate_match_score(dog, self.STANDARD_CRITERIA)
        self.assertEqual(15.0, score)

    def test_age_outside_lower_buffer_returns_zero_age_score(self):
        # Age just outside lower buffer boundary (4) should get zero.
        # Breed and sex match so score equals breed weight + sex weight (50 + 20 = 70)
        # confirming age contributed zero when outside the buffer.
        dog = {**self.BASE_DOG,
               "breed": "Labrador Retriever Mix",
               "sex_upon_outcome": "Intact Female",
               "age_upon_outcome_in_weeks": 4.0}
        score = calculate_match_score(dog, self.STANDARD_CRITERIA)
        self.assertEqual(70.0, score)

    def test_age_outside_upper_buffer_returns_zero_age_score(self):
        # Age just outside upper buffer boundary (181) should get zero.
        # Breed and sex match so score equals breed weight + sex weight (50 + 20 = 70)
        # confirming age contributed zero when outside the buffer.
        dog = {**self.BASE_DOG,
               "breed": "Labrador Retriever Mix",
               "sex_upon_outcome": "Intact Female",
               "age_upon_outcome_in_weeks": 181.0}
        score = calculate_match_score(dog, self.STANDARD_CRITERIA)
        self.assertEqual(70.0, score)

    ###########################################################
    # Test calculate_match_score: Combined scoring
    ###########################################################

    def test_empty_criteria_returns_zero_score(self):
        # All weights are zero, no criteria to score against
        criteria = {
            "breeds": [],
            "sex": [],
            "age_min": None,
            "age_max": None,
            "breed_weight": 0,
            "sex_weight": 0,
            "age_weight": 0
        }
        score = calculate_match_score(self.DOG_PERFECT_MATCH, criteria)
        self.assertEqual(0.0, score)

    def test_all_criteria_matching_returns_100(self):
        # Perfect match on all criteria with weights summing to 100
        # should return a score of exactly 100
        score = calculate_match_score(self.DOG_PERFECT_MATCH, self.STANDARD_CRITERIA)
        self.assertEqual(100.0, score)

    def test_no_criteria_matching_returns_zero(self):
        # BASE_DOG matches no criteria, so breed, sex, and age all return zero.
        # Confirms all three criteria correctly return zero when there is no match.
        score = calculate_match_score(self.BASE_DOG, self.STANDARD_CRITERIA)
        self.assertEqual(0.0, score)

    ###########################################################
    # Test get_scored_results
    ###########################################################

    def test_dogs_above_threshold_are_included(self):
        # Perfect match scores 100. Above MIN_SCORE_THRESHOLD of 55.
        data = [dict(self.DOG_PERFECT_MATCH)]
        result = get_scored_results(data, self.STANDARD_CRITERIA)
        self.assertEqual(1, len(result))

    def test_dogs_below_threshold_are_excluded(self):
        # BASE_DOG scores 0, below MIN_SCORE_THRESHOLD of 55.
        data = [dict(self.BASE_DOG)]
        result = get_scored_results(data, self.STANDARD_CRITERIA)
        self.assertEqual(0, len(result))

    def test_results_are_sorted_descending_by_score(self):
        # Mix of dogs with different scores. Results should be sorted
        # highest score first.
        data = [
            dict(self.BASE_DOG),                  # score 0: excluded
            dict(self.DOG_BREED_AND_SEX_MATCH),   # score 70: included
            dict(self.DOG_PERFECT_MATCH),          # score 100: included
        ]
        result = get_scored_results(data, self.STANDARD_CRITERIA)
        scores = [dog['match_score'] for dog in result]
        self.assertEqual(scores, sorted(scores, reverse=True))

    def test_empty_data_returns_empty_list(self):
        result = get_scored_results([], self.STANDARD_CRITERIA)
        self.assertEqual([], result)

    def test_returns_correct_number_of_results(self):
        # Two dogs above threshold (100 and 70), one below (0)
        # only two should be returned
        data = [
            dict(self.DOG_PERFECT_MATCH),         # score 100: above threshold
            dict(self.DOG_BREED_AND_SEX_MATCH),   # score 70: above threshold
            dict(self.BASE_DOG),                  # score 0: below threshold
        ]
        result = get_scored_results(data, self.STANDARD_CRITERIA)
        self.assertEqual(2, len(result))

    def test_match_score_is_added_to_each_result(self):
        # Verifies match_score field is added to each returned dog dictionary
        data = [dict(self.DOG_PERFECT_MATCH)]
        result = get_scored_results(data, self.STANDARD_CRITERIA)
        self.assertIn('match_score', result[0])
        self.assertEqual(100.0, result[0]['match_score'])


if __name__ == "__main__":
    unittest.main()