import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text


def train_model():
    data = {
        "text": [
            "you won lottery claim now",
            "bank account blocked update kyc",
            "otp is 1234 do not share",
            "hello are you free today",
            "amazon refund department calling",
            "lets play football tonight",
            "urgent verify your account",
            "meeting at 5 pm"
        ] * 3,
        "label": [
            "spam","spam","spam","ham",
            "spam","ham","spam","ham"
        ] * 3
    }

    df = pd.DataFrame(data)
    df["clean"] = df["text"].apply(preprocess_text)

    model = make_pipeline(
        TfidfVectorizer(),
        LogisticRegression()
    )
    model.fit(df["clean"], df["label"])
    return model

model = train_model()

def predict_text(text):
    clean = preprocess_text(text)
    prediction = model.predict([clean])[0]
    confidence = model.predict_proba([clean]).max()
    return prediction, round(confidence, 2)
