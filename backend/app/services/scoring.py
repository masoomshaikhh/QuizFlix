
def calculate_accuracy(correct_answers: int, total_questions: int) -> float:
    """
    Calculate quiz accuracy as a percentage.
    """

    if total_questions <= 0:
        raise ValueError("Total questions must be greater than zero.")

    if correct_answers < 0:
        raise ValueError("Correct answers cannot be negative.")

    if correct_answers > total_questions:
        raise ValueError("Correct answers cannot exceed total questions.")

    accuracy = (correct_answers / total_questions) * 100

    return round(accuracy, 2)


def calculate_quiz_result(correct_answers: int, total_questions: int) -> dict:
    """
    Calculate the final quiz score and accuracy.
    """

    accuracy = calculate_accuracy(
        correct_answers,
        total_questions
    )

    score = correct_answers * 10

    return {
        "correct_answers": correct_answers,
        "total_questions": total_questions,
        "score": score,
        "accuracy": accuracy
    }
