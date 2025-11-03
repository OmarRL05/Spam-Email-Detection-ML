"""
Main entry point for the Spam Detection Model.

This script provides a simple command-line interface to either:
1. Train the model: Loads the dataset, processes the text, trains the
   Logistic Regression model, and saves the fitted model and vectorizer.
2. Predict: Loads a single email, processes it using the saved
   vectorizer, and predicts if it's spam/ham using the saved model.
"""
from spam_model import SpamModel

train = input("Select an option - (e = to train & test, any other key = predict): ")
spamModel = SpamModel()
if train == "e":
    spamModel.load_data(500)
    spamModel.set_training()
    spamModel.start_training()
    spamModel.start_test(show=True)
    spamModel.save_model()
else:
    try:
        spamModel.predict_new("../email-dataset/data/inmail.1")
    except FileNotFoundError as e:
        print(f"[FILE ERROR]: {e}")
    except ValueError as e:
        print(f"[DATA ERRORS]: {e}")
    except Exception as e:
        print(f"[UNEXPECTED ERROR]: {e}")