from flask import Flask, render_template, request
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from statistics import mean
import numpy as np
import pandas as pd
from text_cleaner import clean_text
import pickle

app = Flask(__name__)

with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

# Load the trained model
clf = load_model('trained_models/big_data_seq_150.h5', compile=True)
output = open("model_output.csv", "w")

@app.route("/")
def home():
    return render_template("deploy.html")

@app.route("/predict", methods=["POST"])
def predict():
    text_message = request.form.get('text')
    if text_message is not None and isinstance(text_message, str):
        cleaned_text = clean_text(text_message)
        tokenized_message = tokenizer.texts_to_sequences([cleaned_text])
        tokenized_message = pad_sequences(tokenized_message, maxlen=150)

        prediction = clf.predict(tokenized_message)
        predicted_label = np.argmax(prediction)
        output = open("model_output.csv", "a")
        if predicted_label == 1:
            print("Predicted Label = 1")
            output.write("BAD, " + str((prediction[0][1] * 100)) + "\n")
        else:
            print("Predicted Label = 0")
            output.write("GOOD, " + str((prediction[0][0] * 100)) + "\n")
        output.close()
        return render_template("deploy.html", prediction=predicted_label, text_message=text_message)
    else:
        return render_template("deploy.html", prediction=None, text_message=None)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081, debug=True)
