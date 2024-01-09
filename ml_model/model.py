import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.layers import Bidirectional, Dense, Dropout, Embedding, LSTM
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers.legacy import Adam
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
from keras.callbacks import EarlyStopping
from statistics import mean
from statistics import median_low
from text_cleaner import clean_text
import pickle

# Load data into a Pandas DataFrame
data = pd.read_csv('data/Suicide_Detection.csv') # Big data
# Ensure that 'Tweet' column is of string type
data['text'] = data['text'].astype(str)
# Clean text
data['text'] = data['text'].apply(clean_text)
# Split data into text and labels
texts = data['text']
labels = data['class']

# Label encoding: 'Potential Suicide post' -> 1, 'Not Suicide post' -> 0
label_encoder = LabelEncoder()
labels = label_encoder.fit_transform(labels)

# Create class weights
class_weights = {0: 1.0, 1: 1.0}

# Tokenization and padding
max_words = 20000  # Maximum number of words to keep in the vocabulary
max_sequence_length = 150  # Maximum length of a sequence

tokenizer = Tokenizer(num_words=max_words)
tokenizer.fit_on_texts(texts)
sequences = tokenizer.texts_to_sequences(texts)
X = pad_sequences(sequences, maxlen=max_sequence_length)

# Save the tokenizer using pickle
with open('tokenizer.pickle', 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size=0.15, random_state=9)

# Build the bidirectional LSTM model
model = Sequential()
model.add(Embedding(input_dim=max_words, output_dim=128, input_length=max_sequence_length, mask_zero=True))
model.add(Bidirectional(LSTM(84, return_sequences=True, recurrent_dropout=0.2)))  # Return sequences for stacking LSTM layers
model.add(Dropout(0.3))
model.add(Bidirectional(LSTM(84, recurrent_dropout=0.2)))
model.add(Dropout(0.3))
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.3))
model.add(Dense(2, activation='softmax'))  # Two output units with softmax activation

# Compile the model
model.compile(optimizer=Adam(learning_rate=0.01), loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Define Early Stopping callback
early_stopping = EarlyStopping(monitor='val_loss', patience=1, restore_best_weights=True)


# Train the model with Early Stopping
history = model.fit(
    X_train, y_train,
    epochs=12,
    batch_size=256,
    validation_split=0.1,
    class_weight=class_weights,
    callbacks=[early_stopping]  # Include the Early Stopping callback
)


# Evaluate the model
loss, accuracy = model.evaluate(X_test, y_test)
print(f"Test loss: {loss:.4f}, Test accuracy: {accuracy * 100:.4f}%")

# Plot the history of accuracy vs. epochs
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.show()

# Make predictions on new data
new_texts = ["making some lunch.", "SOMEBODY PLEASE KILL ME IM SO IN LOVE.", "I want to die.", "I want to kill myself"]
new_sequences = tokenizer.texts_to_sequences(new_texts)
new_X = pad_sequences(new_sequences, maxlen=max_sequence_length)

# Convert predictions to labels
predictions = model.predict(new_X)
predicted_labels = np.argmax(predictions, axis=1)  # Get the index of the class with the highest probability
decoded_labels = label_encoder.inverse_transform(predicted_labels)

for label, prediction in zip(decoded_labels, predictions):
    print(f"Predicted Label: {label}, Confidence: {prediction[predicted_labels][0] * 100:.2f}%")

# Save the trained model.
model.save('trained_models/bidirectional_lstm_classifier_model4.h5')
