
import pytest

from backend.app.services.scoring import calculate_quiz_result


# ==========================================
# TEST 1: NORMAL SCORE CALCULATION
# ==========================================

def test_calculate_perfect_score():
    result = calculate_quiz_result(4, 4)

    assert result["score"] == 40
    assert result["accuracy"] == 100.0
    assert result["correct_answers"] == 4


# ==========================================
# TEST 2: PARTIAL SCORE
# ==========================================

def test_calculate_partial_score():
    result = calculate_quiz_result(3, 4)

    assert result["score"] == 30
    assert result["accuracy"] == 75.0


# ==========================================
# TEST 3: ZERO CORRECT ANSWERS
# ==========================================

def test_zero_correct_answers():
    result = calculate_quiz_result(0, 4)

    assert result["score"] == 0
    assert result["accuracy"] == 0.0


# ==========================================
# TEST 4: INVALID TOTAL QUESTIONS
# ==========================================

def test_zero_total_questions():
    with pytest.raises(ValueError):
        calculate_quiz_result(0, 0)


# ==========================================
# TEST 5: NEGATIVE CORRECT ANSWERS
# ==========================================

def test_negative_correct_answers():
    with pytest.raises(ValueError):
        calculate_quiz_result(-1, 4)


# ==========================================
# TEST 6: CORRECT ANSWERS EXCEED TOTAL
# ==========================================

def test_correct_answers_exceed_total():
    with pytest.raises(ValueError):
        calculate_quiz_result(5, 4)


# ==========================================
# TEST 7: PARAMETRIZED SCORING TESTS
# ==========================================

@pytest.mark.parametrize(
    "correct, total, expected_score, expected_accuracy",
    [
        (1, 4, 10, 25.0),
        (2, 4, 20, 50.0),
        (3, 4, 30, 75.0),
        (4, 4, 40, 100.0),
        (5, 5, 50, 100.0),
    ]
)
def test_multiple_scoring_cases(
    correct,
    total,
    expected_score,
    expected_accuracy
):
    result = calculate_quiz_result(correct, total)

    assert result["score"] == expected_score
    assert result["accuracy"] == expected_accuracy
