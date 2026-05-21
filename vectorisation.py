from dotenv import load_dotenv
import pandas as pd
from langchain_mistralai import MistralAIEmbeddings
from langchain_community.vectorstores import FAISS
import os

# --- CONFIGURATION load_dotenv()
load_dotenv()
api_key = os.getenv("MISTRAL_API_KEY")

def creer_base_vectorielle():
    print(" Chargement des données propres...")
    # On charge ton petit fichier de 300 events
    df = pd.read_csv("paris_events_ready.csv")
    
    # On prépare le modèle d'Embedding de Mistral
    embeddings = MistralAIEmbeddings(model="mistral-embed")
    
    print(" Envoi des données à Mistral pour vectorisation (Embedding)...")
    # On transforme la colonne 'text_for_rag' en vecteurs et on stocke dans FAISS
    # FAISS est une bibliothèque qui permet de chercher très vite dans des vecteurs
    vector_db = FAISS.from_texts(df['text_for_rag'].tolist(), embeddings)
    
    # On sauvegarde cette "base de données de vecteurs" sur ton PC
    vector_db.save_local("faiss_index_paris")
    
    print(" Étape 3 terminée ! Ton index vectoriel est sauvegardé dans le dossier 'faiss_index_paris'.")

if __name__ == "__main__":
    creer_base_vectorielle()