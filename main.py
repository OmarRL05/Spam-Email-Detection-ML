"""
Main entry point for the Spam Detection Model.

This script provides a simple command-line interface to either:
1. Train the model: Loads the dataset, processes the text, trains the
   Logistic Regression model, and saves the fitted model and vectorizer.
2. Predict: Loads a single email, processes it using the saved
   vectorizer, and predicts if it's spam/ham using the saved model.
"""
from email.errors import CharsetError

from spam_model import SpamModel

print(r"""
___       __    ______                            
__ |     / /_______  /__________________ ________ 
__ | /| / /_  _ \_  /_  ___/  __ \_  __ `__ \  _ \
__ |/ |/ / /  __/  / / /__ / /_/ /  / / / / /  __/
____/|__/  \___//_/  \___/ \____//_/ /_/ /_/\___/
""")
prompt = (
    "- !Hi! ¿Do you want to save me for later?\n"
    ":Logistic Regression Spam Model\n"
    "Save model? (y/n): "
)

train = input("Type 'start' to train & test the model, otherwise type any other thing to predict you own email\n- ")
spamModel = SpamModel()
if train == "start":
    spamModel.load_data(500)
    spamModel.set_training(train_size=0.8)
    spamModel.start_training(max_iter=1500)
    spamModel.start_test(show=True)
    while (save := input(prompt).strip().lower()) not in ('y', 'n'):
        print("\n" * 50)
        print("Non-valid answer, try again. Please enter 'y' or 'n'.")
    if save == "y":
        spamModel.save_model()
    else:
        print("End program.")

else:
    try:
        file = input("Introduce the directory url of your file\nExample: '../email-dataset/data/inmail.1'\n- ")
        spamModel.predict_new(file)
    except FileNotFoundError as e:
        print(f"[FILE ERROR]: {e}")
    except ValueError as e:
        print(f"[DATA ERRORS]: {e}")
    except Exception as e:
        print(f"[UNEXPECTED ERROR]: {e}")