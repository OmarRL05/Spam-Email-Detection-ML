import os
from html_parser import MyHTMLParser
import email

def get_email_body(email_message):
    msg = email.message_from_string(email_message)
    body = ""
    for part in msg.walk():
        content_type = part.get_content_type()
        if content_type == 'text/plain' or content_type == 'text/html':
            try:
                payload = part.get_payload(decode=True)
                body += payload.decode('latin-1')
            except:
                pass
    return  body

def strip_tags(c_mail):
    """Cleans a raw email string by extracting and stripping its content.

        This function acts as a pipeline that first uses `get_email_body`
        to parse the raw email (handling multipart messages) and then
        uses `MyHTMLParser` to strip any remaining HTML tags.

        :param c_mail: The raw email content as a string.
        :return: A single string of cleaned, plain-text.
    """
    email_body = get_email_body(c_mail)
    html_stripper = MyHTMLParser()
    html_stripper.feed(email_body)
    return html_stripper.return_data()

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
                        clean_content = strip_tags(dirty_content)
                    emails_ds.append((label, clean_content))
                except FileNotFoundError:
                    print("Error: File {} not founded".format(full_content))
                except Exception as e:
                    print("Couldn't read {} file: {}".format(full_content, e))
    return emails_ds

ds = read_data()

