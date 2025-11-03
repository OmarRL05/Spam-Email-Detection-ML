from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from html_parser import MyHTMLParser
import email
import string
import re

class MyEmailParser:
    """
    Manages the end-to-end processing and cleaning of a raw email string.

    This class acts as a pipeline. It is initialized with a raw email
    string and provides methods to progressively extract, clean, and
    normalize its content.

    It handles multipart messages (using .walk()), strips URLs, removes
    HTML tags, and performs NLP normalization (stemming, stopwords).

    Attributes:
        email (str): The raw email string provided at initialization.
        body (str): The internal string that is modified by each
                    processing step.
        stemmer (PorterStemmer): An instance of the NLTK stemmer.
        stop_words (set): A modified set of English stopwords that
                          *excludes* common negations.
        """

    def __init__(self, email):
        """
        Initializes the parser, the raw email, and pre-loads NLP tools.

        This constructor pre-loads the stemmer and stopwords set for
        efficiency. It also modifies the standard stopwords list to
        remove "not" and "n't" to preserve negations.

        :param email: The raw email string to be processed.
        """

        self.email = email
        self.body = ""
        self.stemmer = PorterStemmer()
        stop_words_set = set(stopwords.words('english'))
        stop_words_set.remove("not")
        self.punc = list(string.punctuation) + ["\n", "\t", "/", "`"]
        self.stop_words = stop_words_set

    def get_email_body(self):
        """
        Parses the raw email string to extract the text body.

        Uses `email.message_from_string` and `.walk()` to navigate
        all parts of the email, including multipart messages. It
        extracts and combines all 'text/plain' and 'text/html'
        parts into `self.body`.
        """
        msg = email.message_from_string(self.email)

        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == 'text/plain' or content_type == 'text/html':
                try:
                    payload = part.get_payload(decode=True)
                    self.body += payload.decode('latin-1')
                except:
                    pass

    def strip_urls(self):
        """
        Removes all URLs (starting with http or www) from `self.body`.

        Uses a regular expression to find and replace URLs with a
        single space to prevent words from merging.
        """
        url_pattern = r"(http[s]?://\S+|www\.\S+)"
        self.body = re.sub(url_pattern, " ", self.body)

    def strip_tags(self):
        """
        Strips all HTML tags from `self.body`.

        Uses the custom `MyHTMLParser` to feed the current `self.body`
        and extract only the plain-text data, which then
        overwrites `self.body`.
        """
        html_stripper = MyHTMLParser()
        html_stripper.feed(self.body)
        self.body = html_stripper.return_data()

    def nlp_filter(self):
        """
        Applies NLP normalization to `self.body`.

        This process includes:
        1. Converting text to lowercase.
        2. Tokenizing the text (splitting into words).
        3. Removing stopwords (using the modified set).
        4. Removing punctuation-only tokens.
        5. Stemming each word to its root.

        The cleaned tokens are then re-joined into `self.body`.
        """
        tokens = word_tokenize(self.body.lower())
        filtered_tokens = [word for word in tokens if word not in self.stop_words]
        filtered_punc = [ch for ch in filtered_tokens if ch not in self.punc]
        filtered_singles = [self.stemmer.stem(word) for word in filtered_punc]
        self.body = " ".join(filtered_singles)

    def parser_email(self):
        """
        Runs the complete processing pipeline in the correct order.

        This master method calls all the individual processing steps
        and returns the final, cleaned, and normalized text.

        :return: The fully processed email body as a single string.
        """
        self.get_email_body()
        self.strip_urls()
        self.strip_tags()
        self.nlp_filter()
        return self.body