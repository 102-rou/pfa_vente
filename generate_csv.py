import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker('fr_FR')
random.seed(42)  # Pour résultats reproductibles

# ========== CONFIGURATION ==========
NB_PRODUITS = 5000

# ========== LISTES POUR VARIABLES ==========
CATEGORIES = ['Électronique', 'Vêtements', 'Maison', 'Sport', 'Beauté', 'Alimentation', 'Jouets', 'Livres']
REGIONS = ['Nord', 'Sud', 'Est', 'Ouest', 'Centre', 'Île-de-France', 'Normandie', 'Bretagne', 'PACA']
CANAUX = ['Boutique', 'Site Web', 'Application Mobile']

# ========== GÉNÉRATION DES DONNÉES ==========
print(" Génération des données en cours...")

data = {
    # Variable 1: ID unique
    'ID': [f'PRD-{i:04d}' for i in range(1, NB_PRODUITS + 1)],
    
    # Variable 2: Prix (entre 10€ et 1000€)
    'Prix': [round(random.uniform(10, 1000), 2) for _ in range(NB_PRODUITS)],
    
    # Variable 3: Quantité (entre 1 et 200)
    'Quantite': [random.randint(1, 200) for _ in range(NB_PRODUITS)],
    
    # Variable 4: Remise (0%, 5%, 10%, 15%, 20%, 30%, 50%)
    'Remise': [random.choice([0, 5, 10, 15, 20, 30, 50]) for _ in range(NB_PRODUITS)],
    
    # Variable 5: Catégorie (8 catégories)
    'Categorie': [random.choice(CATEGORIES) for _ in range(NB_PRODUITS)],
    
    # Variable 6: Région (9 régions)
    'Region': [random.choice(REGIONS) for _ in range(NB_PRODUITS)],
    
    # Variable 7: Date de vente (dernière année)
    'Date_Vente': [fake.date_between(start_date='-1y', end_date='today') for _ in range(NB_PRODUITS)],
    
    # Variable 8: Canal de vente (6 canaux)
    'Canal': [random.choice(CANAUX) for _ in range(NB_PRODUITS)]
}

# Création du DataFrame
df = pd.DataFrame(data)

# Trier par date (optionnel, plus réaliste)
df = df.sort_values('Date_Vente').reset_index(drop=True)

# ========== SAUVEGARDE ==========
df.to_csv('ventes.csv', index=False, encoding='utf-8-sig')

print(f"\n ventes.csv généré avec succès!")
print(f" {NB_PRODUITS} produits créés")
print(f" Colonnes: {list(df.columns)}")
print(f"\n APERÇU DES DONNÉES :")
print(df.head(10))
print(f"\n STATISTIQUES RAPIDES :")
print(f"   - Prix moyen: {df['Prix'].mean():.2f} €")
print(f"   - Quantité moyenne: {df['Quantite'].mean():.1f}")
print(f"   - Remise moyenne: {df['Remise'].mean():.1f}%")
print(f"   - Catégories: {df['Categorie'].nunique()}")
print(f"   - Régions: {df['Region'].nunique()}")
print(f"   - Canaux: {df['Canal'].nunique()}")