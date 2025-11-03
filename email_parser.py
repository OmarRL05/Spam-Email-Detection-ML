# Prueba para NLP
from curses.ascii import isalpha
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from html_parser import MyHTMLParser
import email
import string

class MyEmailParser:
    """
    Manages the end-to-end processing and cleaning of a raw email string.

    This class acts as a pipeline. It is initialized with a raw email
    string and provides methods to progressively extract, clean, and
    (eventually) normalize its content.

    It handles multipart messages (using .walk()) and strips HTML tags.
    Future methods will add NLP processing (stemming, stopwords, etc.).

    Attributes:
        email (str): The raw email string provided at initialization.
        body (str): The extracted text content, populated after
        `get_email_body()` is called.
    """

    def __init__(self, email):
        self.email = email
        self.body = ""

    def get_email_body(self):
        msg = email.message_from_string(self.email)

        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == 'text/plain' or content_type == 'text/html':
                try:
                    payload = part.get_payload(decode=True)
                    self.body += payload.decode('latin-1')
                except:
                    pass

    def strip_tags(self):
        """Cleans a raw email string by extracting and stripping its content.

            This function acts as a pipeline that first uses `get_email_body`
            to parse the raw email (handling multipart messages) and then
            uses `MyHTMLParser` to strip any remaining HTML tags.

            :param c_mail: The raw email content as a string.
            :return: A single string of cleaned, plain-text.
        """
        self.get_email_body()
        html_stripper = MyHTMLParser()
        html_stripper.feed(self.body)
        return html_stripper.return_data()

# text = "This is? a sample sentence! don't showing stopword removal."
# stemmer = PorterStemmer()
# stop_words = set(stopwords.words('english'))
# tokens = word_tokenize(text.lower())
#
# filtered_tokens = [word for word in tokens if word not in stop_words]
# filtered_punc = [ch for ch in filtered_tokens if ch not in string.punctuation]
# filtered_singles = [stemmer.stem(word) for word in filtered_punc]
# return_text = " ".join(filtered_singles)
# print(return_text)
