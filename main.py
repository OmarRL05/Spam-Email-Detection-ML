import os
from html_parser import MyHTMLParser

def read_data(file='../email-dataset/full/index', amount=50):
    """
    Reads the Dataset Files

    :param file: The dataset file direction
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
                        content = MyHTMLParser() # HTML tags filter
                        content.feed(email_file.read())
                        clean_content = content.return_data()
                    emails_ds.append((label, clean_content))
                except FileNotFoundError:
                    print("Error: File {} not founded".format(full_content))
                except Exception as e:
                    print("Couldn't read {} file: {}".format(full_content, e))
    return emails_ds

ds = read_data()

