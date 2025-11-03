from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    """
    A custom HTML parser that strips all HTML tags from a given string.

    This class inherits from HTMLParser and overrides the handle_data
    method to collect only the text content, ignoring all tags,
    attributes, and comments.

    Usage:
        parser = MyHTMLParser()
        parser.feed(html_string)
        clean_text = parser.return_data()
    """

    def __init__(self):
        super().__init__()
        self.lista = []

    def handle_data(self, data):
        """Called for every piece of text data found."""
        self.lista.append(data)

    def return_data(self):
        """
        Joins all collected text fragments into a single string.

        :return: A single string containing all the cleaned text.
        """
        return "".join(self.lista)