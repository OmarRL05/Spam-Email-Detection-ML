import os
from email_parser import MyEmailParser
from sklearn.feature_extraction.text import CountVectorizer

def read_data(file='../email-dataset/full/index', amount=50):
    """
    Reads the Dataset Files

    :param file: The dataset's index file.
    :param amount: The amount of data to be read
    :return: List with spam/ham labels and emails content
    """
    emails_ds = []
    base_dir = os.path.dirname(file)
    with open(file, 'r', encoding='latin-1') as ds:
        email = ds.readlines()[:amount]
        for line in email:
            parts = line.split()
            if len(parts) == 2:
                label = parts[0] #Label: 'spam' | 'ham'
                relative_content = parts[1] # ../data/inmail.1
                full_content = os.path.join(base_dir, relative_content) #Solves route error

                print("Opening: {}".format(full_content))
                try:
                    with open(full_content, 'r', encoding='latin-1') as email_file:
                        dirty_content = email_file.read()
                        parser = MyEmailParser(dirty_content) # Init DataSet
                        clean_content = parser.parser_email()
                    emails_ds.append((label, clean_content))
                except FileNotFoundError:
                    print("Error: File {} not founded".format(full_content))
                except Exception as e:
                    print("Couldn't read {} file: {}".format(full_content, e))
    return emails_ds

def init_dataset(data):
    """
    Prepares and vectorizes the raw email dataset for machine learning.

    This function takes the list of (label, text) tuples, separates
    it into features (X) and labels (y), and then converts the
    raw text features into a numeric bag-of-words matrix using
    CountVectorizer.

    :param data: A list of (label, clean_text) tuples.
    :return: A tuple of (y_labels, X_vectorized), where:
             y_labels (list): The list of labels ('spam' or 'ham').
             X_vectorized (scipy.sparse.csr_matrix): The sparse matrix of numeric features.
    """
    print("Data Loaded. Vectorizing...")
    X_texts = [tupla[1] for tupla in data]
    y_labels = [tupla[0] for tupla in data]

    # Transform email content with CountVectorizer
    vectorizer = CountVectorizer()
    X_vectorized = vectorizer.fit_transform(X_texts)
    return y_labels, X_vectorized

if __name__ == "__main__":
    data = read_data()
    y, x = init_dataset(data)