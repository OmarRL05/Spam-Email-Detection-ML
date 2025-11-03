# Spam-Email-Detection-ML
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

A machine learning project to build an email spam detection system using Python. This repository contains the code and process for classifying emails from the TREC 2007 Public Spam Corpus as either 'Spam' or 'Ham'.

This model uses Scikit-learn's `LogisticRegression` with a `CountVectorizer` and a custom NLP pipeline (built with NLTK) to clean and process raw email data.

## Features
* **End-to-End NLP Pipeline:** Cleans raw emails by handling multipart messages, stripping URLs, stripping HTML tags, removing stopwords (while preserving negations), and performing stemming.
* **Train/Predict Modes:** A simple CLI to either train a new model or predict on a new, unseen file.
* **Model Persistence:** Saves the fitted `LogisticRegression` model (`spam_model.pkl`) and `CountVectorizer` (`vectorizer.pkl`) during training.
* **Stateless Prediction:** Loads the saved `.pkl` files for prediction, ensuring a correct and stateless workflow.
* **Robust Error Handling:** Uses `raise` and `try...except` to gracefully handle missing models or bad file paths.

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### 1. Prerequisites
* Python 3.8+
* pip

### 2. Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/omarrl05/spam-email-detection-ml.git](https://github.com/omarrl05/spam-email-detection-ml.git)
    cd spam-email-detection-ml
    ```

2.  **Install Python dependencies:**
    Use `requirements.txt` to install all necessary packages.
    ```bash
    pip install -r requirements.txt
    ```

3.  **Download NLTK data:**
    The project requires 'stopwords' and 'punkt' from NLTK. Run the following Python commands:
    ```python
    import nltk
    nltk.download('stopwords')
    nltk.download('punkt')
    ```

4.  **Download the Dataset:**
    This project uses the **TREC 2007 Public Spam Corpus**. Download the `email-dataset.zip` file from the link below and unzip it.
    
    **Link:** [Download TREC 2007 Dataset (email-dataset.zip)](https://drive.google.com/file/d/1qm66GCTQkgwc8wl1aXAhobcmAqGIh1BR/view?usp=sharing)
    
    **Important:** Place the unzipped `email-dataset` folder inside the project's root directory. The final structure should look like this:

    ```
    spam-email-detection-ml/
    ├── email-dataset/     <-- The unzipped folder
    ├── main.py
    ├── spam_model.py
    ├── requirements.txt
    └── ...
    ```

## Usage

The `main.py` script is the single entry point for all operations.

### 1. Training the Model
To train, test, and save the model, run `main.py` and type **`start`** when prompted.

```bash
python main.py
```
**This will:**

1- Load and process the dataset (default: 500 emails)
2- Split the data (default: 80% train / 20% test)
3- Train the LogisticRegression model
4- Print the accuracy score on the test set
5- Save vectorizer.pkl and spam_model.pkl to your disk

### 2. Predicting a New Email
To predict a single email, run main.py and type anything other than "start".

The script will prompt you for the file path of the email you want to analyze.

**Example:**
```
Type 'start' to train & test the model, otherwise type any other thing to predict you own email
- p
Introduce the directory url of your file
Example: '../email-dataset/data/inmail.1'
- ../email-dataset/data/inmail.1
```
The model will load the saved ```.pkl files```, process the new email, and print its prediction.

## Project Structure

| File / Folder       | Description                                                                 |
|---------------------|-----------------------------------------------------------------------------|
| main.py             | Main entry point with CLI for training and prediction.                      |
| spam_model.py       | Contains the SpamModel class that manages model lifecycle (train, test, predict, save). |
| email_parser.py     | Defines the MyEmailParser class for the full NLP cleaning pipeline.         |
| html_parser.py      | Implements MyHTMLParser to strip HTML tags from emails.                     |
| load_dataset.py     | Functions to load and vectorize the full training dataset.                  |
| load_user_data.py   | Loads and vectorizes a single email for prediction using saved vectorizer.  |
| requirements.txt    | Lists all required Python dependencies.                                     |
| .gitignore          | Ensures Git ignores model files (.pkl) and dataset archives (.zip).         |

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change

## License
This project is licensed under the MIT License. See the LICENSE file for details.
