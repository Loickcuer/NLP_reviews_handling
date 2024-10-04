import streamlit as st
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM

st.title ('Project: Data Exploration and NLP Modeling - Nicolas Berlioz et Loick Cuer')
st.header('Résumer un texte en français avec BARThez.')

# Charger le tokenizer et le modèle
barthez_tokenizer = AutoTokenizer.from_pretrained("moussaKam/barthez")
barthez_model = AutoModelForSeq2SeqLM.from_pretrained("moussaKam/barthez-orangesum-abstract")

# Utilisez le modèle BARThez pour la sommation
summarizer = pipeline(task="summarization", model=barthez_model, tokenizer=barthez_tokenizer, framework="pt", truncation=True)

# Fonction pour appliquer la sommation et gérer NaN
def summarize_and_handle_nan(text):
    if text:
        return summarizer(text, max_length=150, min_length=20, length_penalty=2, num_beams=4)[0]['summary_text']
    else:
        return ""

st.title('Résumé de l\'avis')
user_input = st.text_area("Veuillez écrire votre avis ici:")

if st.button('Résumer'):
    summary = summarize_and_handle_nan(user_input)
    st.write('Résumé de l\'avis :', summary)