import pandas as pd
import numpy as np

def analyser_ventes(fichier_csv):
    """
    Analyse complète des ventes avec 8 variables
    """
    # Lecture du fichier
    df = pd.read_csv(fichier_csv)
    
    # Conversion de la date
    df['Date_Vente'] = pd.to_datetime(df['Date_Vente'])
    
    # 1. CA Brut (Prix × Quantité)
    df['CA_Brut'] = df['Prix'] * df['Quantite']
    
    # 2. Montant de la remise
    df['Montant_Remise'] = df['CA_Brut'] * (df['Remise'] / 100)
    
    # 3. CA Net (après remise)
    df['CA_Net'] = df['CA_Brut'] - df['Montant_Remise']
    
    # 4. TVA (20% du CA Net)
    df['TVA'] = df['CA_Net'] * 0.20
    
    # 5. Marge (estimation 30% sur CA Net)
    df['Marge'] = df['CA_Net'] * 0.30
    
    ca_total = df['CA_Net'].sum()
    tva_totale = df['TVA'].sum()
    marge_totale = df['Marge'].sum()
    
    # ========== PRODUIT TOP BÉNÉFICE ==========
    meilleur_produit = df.loc[df['CA_Net'].idxmax()]
    
    # ========== STATISTIQUES PAR CATÉGORIE ==========
    stats_categorie = df.groupby('Categorie').agg({
        'CA_Net': ['sum', 'mean', 'count'],
        'Quantite': 'sum',
        'Remise': 'mean'
    }).round(2)
    
    # ========== STATISTIQUES PAR RÉGION ==========
    stats_region = df.groupby('Region').agg({
        'CA_Net': 'sum',
        'Quantite': 'sum'
    }).round(2)
    
    # ========== STATISTIQUES PAR CANAL ==========
    stats_canal = df.groupby('Canal').agg({
        'CA_Net': 'sum',
        'Quantite': 'sum'
    }).round(2)
    
    # ========== ÉVOLUTION TEMPORELLE ==========
    df['Mois'] = df['Date_Vente'].dt.to_period('M')
    evolution_mensuelle = df.groupby('Mois')['CA_Net'].sum().reset_index()
    evolution_mensuelle['Mois'] = evolution_mensuelle['Mois'].astype(str)
    
    # ========== PACK DES RÉSULTATS ==========
    stats = {
        'ca_total': ca_total,
        'tva_totale': tva_totale,
        'marge_totale': marge_totale,
        'nb_produits': len(df),
        'nb_transactions': df['ID'].nunique(),
        'meilleur_produit': {
            'id': meilleur_produit['ID'],
            'ca': meilleur_produit['CA_Net'],
            'categorie': meilleur_produit['Categorie'],
            'region': meilleur_produit['Region'],
            'canal': meilleur_produit['Canal']
        },
        'stats_categorie': stats_categorie,
        'stats_region': stats_region,
        'stats_canal': stats_canal,
        'evolution_mensuelle': evolution_mensuelle,
        'prix_moyen': df['Prix'].mean(),
        'quantite_moyenne': df['Quantite'].mean(),
        'remise_moyenne': df['Remise'].mean()
    }
    
    return df, stats

def exporter_resultats(df):
    df.to_csv('resultats_final.csv', index=False, encoding='utf-8-sig')
    print(" resultats_final.csv exporté !")

def generer_rapport_texte(stats):
    rapport = f"""
    • Chiffre d'Affaires Total Net : {stats['ca_total']:,.2f} €
    • TVA Totale (20%) : {stats['tva_totale']:,.2f} €
    • Marge Totale Estimée (30%) : {stats['marge_totale']:,.2f} €
    • Nombre de transactions : {stats['nb_transactions']}
    • ID Produit : {stats['meilleur_produit']['id']}
    • CA Généré : {stats['meilleur_produit']['ca']:,.2f} €
    • Catégorie : {stats['meilleur_produit']['categorie']}
    • Région : {stats['meilleur_produit']['region']}
    • Canal de vente : {stats['meilleur_produit']['canal']}
    """
    
    top_categories = stats['stats_categorie']['CA_Net']['sum'].nlargest(3)
    for cat, ca in top_categories.items():
        rapport += f"    • {cat} : {ca:,.2f} €\n"
    
    rapport += f"""
    🗺️ STATISTIQUES PAR RÉGION (Top 3) :
    ───────────────────────────────────────────────────────────
    """
    
    top_regions = stats['stats_region']['CA_Net'].nlargest(3)
    for reg, ca in top_regions.items():
        rapport += f"    • {reg} : {ca:,.2f} €\n"
    
    rapport += f"""
    📱 STATISTIQUES PAR CANAL (Top 3) :
    ───────────────────────────────────────────────────────────
    """
    
    top_canaux = stats['stats_canal']['CA_Net'].nlargest(3)
    for canal, ca in top_canaux.items():
        rapport += f"    • {canal} : {ca:,.2f} €\n"
    
    rapport += """
    ═══════════════════════════════════════════════════════════
    """
    
    return rapport

# Test rapide
if __name__ == "__main__":
    df, stats = analyser_ventes('ventes.csv')
    print(generer_rapport_texte(stats))