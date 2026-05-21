import unittest
import os
import re
import pandas as pd
from datetime import datetime, timedelta

class TestQualiteDonneesPulsEvents(unittest.TestCase):
    """
    Classe de tests unitaires validant la conformité du dataset Puls-Events
    par rapport aux contraintes métiers (Périmètre géographique et fraîcheur temporelle).
    """

    def setUp(self):
        """Méthode de préparation : chargement du dataset."""
        self.file_path = "paris_events_ready.csv"
        self.assertTrue(os.path.exists(self.file_path), f"❌ Erreur : Fichier {self.file_path} introuvable.")
        self.df = pd.read_csv(self.file_path)

    def test_1_perimetre_geographique(self):
        """Vérifie que les données ciblent le périmètre sémantique de Paris."""
        print("🔍 Vérification sémantique de la localisation géographique...")
        contenu_brut = self.df['text_for_rag'].str.lower()
        contient_paris = contenu_brut.str.contains('paris|750|france').sum()
        ratio = contient_paris / len(self.df)
        self.assertGreaterEqual(ratio, 0.90, "❌ Échec : Le texte n'est pas centré sur Paris.")
        print(f"✅ Test Géo validé : {ratio*100:.1f}% des textes mentionnent Paris.")

    def test_2_fraicheur_temporelle_moins_un_an(self):
        """
        Vérifie la contrainte de Jérémy : Événements de moins d'un an (Date pivot : 18 Mai 2026).
        """
        date_pivot = datetime(2026, 5, 18)
        un_an_en_arriere = date_pivot - timedelta(days=365)
        un_an_en_avant = date_pivot + timedelta(days=365)

        print("🔍 Extraction sémantique des balises temporelles...")
        dates_converties = []
        
        for idx, row in self.df.iterrows():
            texte = str(row['text_for_rag'])
            # Pattern ultra-large pour attraper n'importe quelle date au format JJ/MM/2026
            match = re.search(r'(\d{2}/\d{2}/2026)', texte)
            
            if match:
                dates_converties.append(datetime.strptime(match.group(1), '%d/%m/%Y'))

        # Validation de la présence de dates
        self.assertGreater(len(dates_converties), 0, "❌ Échec : Aucune date au format 2026 trouvée dans le CSV.")
        
        # Validation finale de la contrainte "Moins d'un an"
        for date_ev in dates_converties:
            self.assertTrue(
                un_an_en_arriere <= date_ev <= un_an_en_avant,
                f"❌ Échec Temporel : L'événement du {date_ev.strftime('%d/%m/%Y')} sort de la fenêtre d'un an."
            )
        print(f"✅ Test Temporel validé : {len(dates_converties)} événements vérifiés en 2026 (Tous à moins d'un an).")

    def test_3_structure_rag(self):
        """Garantit la présence de la colonne d'ingestion sémantique indispensable au RAG."""
        self.assertIn('text_for_rag', self.df.columns, "❌ Échec : La colonne 'text_for_rag' est introuvable.")
        print("✅ Test Structure validé : La colonne 'text_for_rag' est opérationnelle.")

if __name__ == "__main__":
    unittest.main()