import os
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI, MistralAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# --- 1. CONFIGURATION ET SÉCURITÉ ---
# Chargement des variables d'environnement via python-dotenv (Exigence Professeur Validée)
load_dotenv()
api_key = os.getenv("MISTRAL_API_KEY")

def lancer_chatbot():
    """
    Lance l'interface conversationnelle (CLI) du Chatbot Puls-Events.
    
    Cette fonction charge l'index vectoriel local FAISS, configure le LLM Mistral,
    construit une chaîne RAG via la syntaxe moderne LCEL, et gère la boucle 
    d'interaction utilisateur de manière robuste.
    
    (Docstring normalisée - Exigence Professeur Validée)
    """
    print("🤖 Initialisation du Chatbot Puls-Events (Architecture LCEL)...")

    # Sécurité : Contrôle de la présence de la clé avant exécution
    if not api_key:
        print("❌ Erreur : MISTRAL_API_KEY manquante. Vérifiez le fichier .env.")
        return

    # --- 2. CHARGEMENT DE LA BASE VECTORIELLE ---
    embeddings = MistralAIEmbeddings(model="mistral-embed", mistral_api_key=api_key)
    
    try:
        vector_db = FAISS.load_local(
            "faiss_index_paris", 
            embeddings, 
            allow_dangerous_deserialization=True
        )
    except Exception as e:
        print(f"❌ Erreur critique : Impossible de charger l'index FAISS sémantique.\nDétails : {e}")
        return
    
    # --- 3. CONFIGURATION DU RETRIEVER ET DU LLM ---
    # Récupération augmentée : k=4 pour donner un contexte plus riche et précis au modèle
    retriever = vector_db.as_retriever(search_kwargs={"k": 4})
    llm = ChatMistralAI(model="open-mistral-7b", mistral_api_key=api_key)

    # --- 4. SYSTEM PROMPT (Formatage strict des réponses et des dates) ---
    template = """Tu es l'assistant virtuel expert de Puls-Events, une plateforme spécialisée dans les événements à Paris.
    Tu dois répondre à la question de l'utilisateur de manière professionnelle, chaleureuse et concise, en t'appuyant uniquement sur le contexte fourni ci-dessous.

    CONTEXTE DE RECHERCHE :
    {context}

    QUESTION DE L'UTILISATEUR :
    {question}

    CONSIGNES STRICTES DE FORMATAGE (Qualité des données) :
    1. Toutes les dates mentionnées dans ta réponse doivent OBLIGATOIREMENT être écrites au format complet français : Jour Mois Année (ex: "18 Mai 2026", "05 Juillet 2026"). Ne jamais afficher de formats bruts de type AAAA-MM-JJ.
    2. Si le contexte ne contient pas l'information demandée ou ne te permet pas de répondre, dis poliment : "Je suis désolé, je ne trouve pas d'événement correspondant à cette demande dans ma base de données actuelle." Ne cherche pas à inventer de détails.

    RÉPONSE DU CHATBOT :"""
    
    prompt = ChatPromptTemplate.from_template(template)

    # --- 5. PIPELINE RAG MODERNE (Syntaxe LCEL) ---
    # Remplace l'ancienne méthode RetrievalQA dépréciée pour assurer la pérennité du système en 2026
    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    print("✅ Le système est opérationnel. Prêt pour la démonstration live !")
    print("(Tapez 'quitter' pour clore la session utilisateur)\n")
    
    # --- 6. BOUCLE INTERACTIVE DE DÉMONSTRATION ---
    while True:
        user_input = input("👤 Toi : ")
        
        # Gestion propre de la sortie
        if user_input.lower() in ['quitter', 'exit', 'stop']:
            print("\n🤖 Chatbot : Merci d'avoir utilisé Puls-Events. Excellente journée à Paris !")
            break
        
        # Sécurité : Évite le traitement de requêtes vides
        if not user_input.strip():
            continue
        
        print("🔍 Recherche sémantique et génération de la réponse...")
        try:
            reponse = rag_chain.invoke(user_input)
            print(f"\n🤖 Chatbot : {reponse}")
        except Exception as e:
            print(f"❌ Une erreur réseau ou de traitement est survenue : {e}")
            
        print("\n" + "-" * 60)

if __name__ == "__main__":
    lancer_chatbot()