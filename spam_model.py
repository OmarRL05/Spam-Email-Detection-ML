from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import joblib
from load_user_data import read_user_data, transform_user_input
from load_dataset import read_data, init_dataset
from sklearn.linear_model import LogisticRegression

class SpamModel:
    def __init__(self):
        """
        Initializes the SpamModel, creating placeholder attributes.
        The LogisticRegression model is initialized but not fitted.
        """
        self._lr = LogisticRegression()
        self.data = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None

    def load_data(self, data_amount):
        """
        Loads the training dataset from the index file.

        :param data_amount: The number of emails to load from the dataset.
        """
        self.data = read_data(amount=data_amount)

    def set_training(self, train_size=0.7, random_state=42):
        """
        Prepares and splits the loaded data into training and testing sets.

        This method vectorizes the text data using init_dataset, saves the
        fitted vectorizer ('vectorizer.pkl'), and then splits the data
        into X_train, X_test, y_train, and y_test.

        :param train_size: The proportion of the dataset to include in the
                           training split (e.g., 0.7 for 70%).
        :param random_state: A seed for the random split for reproducibility.
        """
        X, y, vectorizer= init_dataset(self.data)
        joblib.dump(vectorizer, 'vectorizer.pkl')
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, train_size=train_size, random_state=random_state)

    def start_training(self, max_iter=500, random_state=42):
        """
        Fits the Logistic Regression model to the training data.

        :param max_iter: Maximum number of iterations for the solver.
        :param random_state: Seed for reproducibility.
        """
        self._lr = LogisticRegression(max_iter=max_iter, random_state=random_state)
        self._lr.fit(self.X_train, self.y_train)

    def save_model(self):
        """
        Saves the fitted Logistic Regression model to a file.
        """
        joblib.dump(self._lr, 'spam_model.pkl')
        print("Model trained and saved to 'spam_model.pkl'!")

    def start_test(self, show=False):
        """
        Evaluates the trained model against the test set and prints the accuracy.

        :param show: If True, prints the accuracy score to the console.
        """
        y_predict = self._lr.predict(self.X_test)
        if show:
            lr_accuracy = accuracy_score(self.y_test, y_predict)
            print("Accuracy: {:.5f}".format(lr_accuracy))

    def predict_new(self, url):
        """
        Predicts if a new mail is spam.

        :param url: Email file's directory.
        :return: Prediction string ('spam' or 'ham').

        :raises FileNotFoundError: If model 'spam_model.pkl' not founded.
        :raises ValueError: If users mail can't be read or vectorized.
        """

        try:
            self._lr = joblib.load('spam_model.pkl')
        except FileNotFoundError:
            raise FileNotFoundError("Model file 'spam_model.pkl' not found. Model must be trained first.")

        user_data = read_user_data(url)
        if user_data is None:
            raise ValueError("Could not process user email. The file might be empty or unreadable.")

        X_user = transform_user_input(user_data)
        if X_user is None:
            raise ValueError("Could not vectorize user email. Aborting prediction.")

        y_user_predict = self._lr.predict(X_user)
        print(f"Prediction: {y_user_predict}")