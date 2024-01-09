import pytest
from tensorflow.keras.models import load_model
from model import X_test, y_test  # Import your testing data split


def test_model_accuracy():
    """
    Simply testing whether the generated model has greater than 90% accuracy on the validation set.
    The test will generate a model as specified in model.py, and then check the accuracy at the end.
    Tests cannot be made for individual texts since the model cannot be 100% accurate.
    """
    model = load_model('big_data_seq_150.h5')
    _, accuracy = model.evaluate(X_test, y_test)
    assert accuracy > 0.90


if __name__ == "__main__":
    pytest.main()
