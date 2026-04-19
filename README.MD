# 📊 PFA - Automatisation des Ventes

Projet de Fin d'Année - Automatisation et Analyse de Données Commerciales

## 🎯 Objectif
Automatiser l'analyse des ventes d'une entreprise e-commerce en remplaçant les tableurs Excel par un script Python performant avec dashboard mobile interactif.

## ✨ Fonctionnalités
- ✅ Génération automatique de 550+ produits avec 8 features
- ✅ Calculs: CA Brut, CA Net, TVA (20%), Marge
- ✅ Identification du produit top performance
- ✅ Dashboard mobile interactif (Streamlit + Plotly)
- ✅ Export CSV des résultats
- ✅ Recommandations stratégiques automatiques

## 📁 Structure du Projet
- 📁 PFA_VENTES
    - 📁 analyse_vente.py
    - 📁 generate_csv.py
    - 📁 app_mobile.py
    - 📁 README.MD
    - 📁 .gitignore
    - 📁 ventes.csv

## 🚀 Installation

1. Cloner le projet:
```bash
git clone https://github.com/102-rou/pfa_ventes.git
cd pfa_ventes

#créer environnement virtuel#
python -m venv venv
.venv\Scripts\activate  
```

2. Installer les dépendances:
```bash
pip install -r requirements.txt

```

3. Lancer le script:
```bash
python generate_csv.py
python app_mobile.py
```
4. Résultats:

Dashboard mobile interactif
Graphiques statistiques (histogramme, camembert, barres)
Export CSV automatique
Recommandations stratégiques

5. Technologies:
Python 3.14
Pandas, Faker, Streamlit, Plotly
Git & GitHub

## 👨‍💻 Auteur
Roudayna Marweni - Projet de Fin d'Année

## 📝 Licence
MIT
