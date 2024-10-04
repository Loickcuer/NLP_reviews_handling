import streamlit as st
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle

st.title ('Project: Data Exploration and NLP Modeling - Nicolas Berlioz et Loick Cuer')
st.header('Predire si un avis un positif ou non.')

with open('tokenizer3.pkl', 'rb') as handle:
    tokenizer3 = pickle.load(handle)
model3 = tf.keras.models.load_model('model3.h5')

# Fonction pour préparer le texte de l'utilisateur pour la prédiction
def prepare_text(text):
    sequence = tokenizer3.texts_to_sequences([text])
    padded_sequence = pad_sequences(sequence, maxlen=50, padding='post')
    return padded_sequence

st.title('Prédiction de "Liked"')
user_input = st.text_input("Entrez un avis à analyser.")

if st.button('Prédire'):
    prepared_input = prepare_text(user_input)
    prediction = model3.predict(prepared_input)
    if prediction > 0.5:
        st.write('Cet avis est positif !')
    else:
        st.write('Cet avis est négatif !')
