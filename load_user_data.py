import os
from email_parser import MyEmailParser
import joblib

def read_user_data(file):
    """
    Reads the Dataset Files

    :param file: The dataset's index file.
    :param amount: The amount of data to be read
    :return: List with spam/ham labels and emails content
    """
    email_ds = []
    with open(file, 'r', encoding='latin-1') as email_file:
        print(f"Opening file...")
        try:
            dirty_content = email_file.read()
            parser = MyEmailParser(dirty_content) # Init DataSet
            clean_content = parser.parser_email()
            email_ds.append(clean_content)
        except FileNotFoundError:
            print("Error: File {} not founded".format(email_file))
        except Exception as e:
            print("Couldn't read {} file: {}".format(email_file, e))
    return email_ds

def transform_user_input(data, vectorizer_path='vectorizer.pkl'):
    """
    Reads a single raw email file from the specified path for prediction.

    :param file: The full path to the user's email file.
    :return: A list containing the single, cleaned email string,
             or an empty list if processing fails.
    """
    print("Data Loaded! Vectorizing...")
    X_texts = data

    # Transform email content with CountVectorizer
    try:
        vectorizer = joblib.load(vectorizer_path)
    except FileNotFoundError:
        print(f'Error: Vectorizer File nof founded on {vectorizer_path}')
        print('You must load the dataset and train the model')
        return None
    X_vectorized = vectorizer.transform(X_texts)
    return X_vectorized

if __name__ == "__main__":
    data = read_user_data(file="../email-dataset/data/inmail.1")
    if data:
        x = transform_user_input(data)
        if data is not None:
            print("¡Mail vectorized correctly!")