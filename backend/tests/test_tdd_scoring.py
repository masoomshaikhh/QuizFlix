
from backend.app.services import scoring


def test_calculate_accuracy():
    assert scoring.calculate_accuracy(3, 4) == 75.0


def test_calculate_accuracy_perfect():
    assert scoring.calculate_accuracy(4, 4) == 100.0


def test_calculate_accuracy_zero_correct():
    assert scoring.calculate_accuracy(0, 4) == 0.0
