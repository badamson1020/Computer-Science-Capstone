"""Weighted matching algorithm for the Grazioso Salvare animal shelter dashboard.

Contains the core business logic for scoring and filtering rescue dog candidates
against user defined criteria. Separated from the dashboard UI layer to follow
the Model View Controller pattern. Algorithm logic is independently testable
and reusable without requiring the Dash application to be running.
"""

###########################
# Algorithm Constants
###########################


# Minimum score threshold for weighted search results.
# Dogs scoring below this value are excluded from results to prevent
# irrelevant matches from cluttering the data table while still showing
# partial matches that binary filtering would exclude entirely.
# A threshold of 55 balances completeness with result relevance.
MIN_SCORE_THRESHOLD = 55

# Small tolerance for floating point boundary comparisons.
# Database age values are stored as long floats which may differ
# from user entered whole numbers by tiny amounts due to floating
# point representation. Epsilon prevents dogs at the exact boundary
# from being incorrectly excluded or incorrectly placed in the buffer zone.
EPSILON = 0.001


###########################
# Algorithm Functions
###########################


def calculate_match_score(dog: dict, criteria: dict) -> float:
    """Calculate a weighted match score between 0 and 100 for a dog against user defined criteria.

    Each criterion contributes to the total score proportionally to its assigned weight.

    Scoring rules:
        Breed: full weight for exact match, half weight for partial match, zero otherwise.
        A set comprehension is used for the exact match check rather than a list
        because set lookups are O(1) vs O(n) for lists, the hash based lookup
        jumps directly to the value rather than scanning each element sequentially.
        Partial match checks if either string is a substring of the other,
        catching cases like "German Shepherd" partially matching "German Shepherd Mix".

        Sex: full weight for match against any selected sex value, zero otherwise.
        Multiple sex selections are treated as equally valid full matches.

        Age: full weight if within preferred range, half weight if within 20% of
        boundary, zero if completely outside. The 20% buffer avoids penalizing dogs
        just barely outside the range the same as dogs far outside it.

    Args:
        dog: Dictionary containing dog field values as retrieved from the shelter collection.
        criteria: Dictionary containing breeds, sex values, age range, and weights.

    Returns:
        Weighted match score between 0 and 100.
    """
    score = 0.0

    breed_weight = criteria.get("breed_weight", 0)
    sex_weight = criteria.get("sex_weight", 0)
    age_weight = criteria.get("age_weight", 0)

    # Breed scoring: exact match gets full weight, partial match gets half weight.
    if breed_weight > 0:
        selected_breeds = criteria.get("breeds", [])
        dog_breed = dog.get("breed", "")

        # Convert to lowercase set for O(1) exact match lookup.
        # Case-insensitive comparison handles any inconsistencies in database casing.
        selected_breeds_lower = {b.lower() for b in selected_breeds}

        if dog_breed.lower() in selected_breeds_lower:
            score += breed_weight
        elif any(b.lower() in dog_breed.lower() or dog_breed.lower() in b.lower()
                 for b in selected_breeds):
            # Partial match: checks if either string is a substring of the other.
            # Uses the original selected_breeds list here rather than the set since
            # substring checking requires iterating through values. Sets do not
            # support substring operations, only exact membership testing.
            score += breed_weight * 0.5

    # Sex scoring: full weight if the dog matches any selected sex value, zero otherwise.
    # Multiple sex selections are treated as equally valid full matches.
    # Case-insensitive comparison handles any inconsistencies in database casing,
    # consistent with the breed matching approach.
    if sex_weight > 0:
        selected_sex = criteria.get("sex", [])
        dog_sex = dog.get("sex_upon_outcome", "")

        # Convert to lowercase set for O(1) case insensitive lookup.
        # Same approach used for breed exact matching.
        selected_sex_lower = {s.lower() for s in selected_sex}

        if dog_sex.lower() in selected_sex_lower:
            score += sex_weight

    # Age scoring: full weight within range, half weight within 20% buffer of boundary,
    # zero outside. The 20% buffer prevents a dog just barely outside the range from
    # being scored the same as a dog completely outside it.
    if age_weight > 0:
        age_min = criteria.get("age_min")
        age_max = criteria.get("age_max")
        dog_age = dog.get("age_upon_outcome_in_weeks")

        if dog_age is not None and age_min is not None and age_max is not None:
            age_range = age_max - age_min
            buffer = age_range * 0.2

            # EPSILON allows for a small tolerance for floating point boundary comparisons.
            if (age_min - EPSILON) <= dog_age <= (age_max + EPSILON):
                # Within preferred range gets full weight.
                score += age_weight
            elif (age_min - buffer - EPSILON) <= dog_age < (age_min - EPSILON) or \
                    (age_max + EPSILON) < dog_age <= (age_max + buffer + EPSILON):
                # Within 20% buffer of the boundary gets half weight.
                score += age_weight * 0.5

    return round(score, 1)


def get_scored_results(data: list[dict], criteria: dict) -> list[dict]:
    """Score each dog against the provided criteria and return ranked results.

    Filters out dogs below the minimum score threshold and returns results
    sorted by score descending so the best matches appear first.
    Separating this logic from the callback keeps update_table focused on
    data retrieval and formatting rather than algorithm execution.

    Args:
        data: List of dog record dictionaries retrieved from the shelter collection.
        criteria: Dictionary containing search criteria and weights.

    Returns:
        List of scored dog records above the minimum threshold, sorted descending.
    """
    scored_data = []
    for dog in data:
        score = calculate_match_score(dog, criteria)
        # score is safe to compare against MIN_SCORE_THRESHOLD without epsilon because
        # calculate_match_score returns round(score, 1). Scores are always multiples
        # of whole number weights multiplied by 1, 0.5, or 0 which have exact binary
        # floating point representations. No floating point imprecision can occur here.
        if score >= MIN_SCORE_THRESHOLD:
            dog['match_score'] = score
            scored_data.append(dog)

    # Sort descending so that highest scoring matches appear first.
    # Ranking by relevance is a core part of the weighted algorithm output.
    scored_data.sort(key=lambda x: x['match_score'], reverse=True)
    return scored_data