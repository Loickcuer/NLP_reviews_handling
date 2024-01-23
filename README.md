# NLP_reviews_handling
Project: Data Exploration and NLP Modeling

Rendu de second projet NLP ESILV par Nicolas BERLIOZ et Loick CUER

Scraping_script.ipynb contient le code utilisé pour scrapper notre base de données à partir du site trustpilot.

Scraped_data.csv est la base de données utilisée lors des travaux. C'est le produit du code de Scraping_script.

Rendu Projet 2 NLP.ipynb contient tout le code qui exploite cette base de donnée, la nettoie, créé des résumes, des traductions et des modèles de prédiction.

data.csv contient la base de données des prénoms et du genre qui leur est associé.

model3.h5 contient le modèle avec la meilleure accuracy parmi ceux créé. C'est ce modèle que nous avons utilisé pour l'application streamlit streamlit_prediction.py

streamlit_prediction.py contient l'application streamlit qui prédit si un avsi est positif ou non.

streamlit_summarization contient l'application streamlit qui résume un texte.

tokenizer3.pkl contient le tokenizer utilisé dans streamlit_prediction.py
