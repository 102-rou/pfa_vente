# 📊 PFA - Automatisation des Ventes

## 🎯 Objectif
Automatiser l'analyse des ventes d'une entreprise e-commerce en remplaçant les tableurs Excel par un script Python performant avec dashboard mobile interactif.

## ✨ Fonctionnalités
- ✅ Génération automatique de 500+ produits avec 8 features
- ✅ Calculs: CA Brut, CA Net, TVA (20%), Marge
- ✅ Identification du produit top performance
- ✅ Dashboard mobile interactif (Streamlit + Plotly)
- ✅ Export CSV des résultats
- ✅ Recommandations stratégiques automatiques

## 📁 Structure du Projet
- 📁 PFA_VENTES
    - 📁 .github\workflows
        - 📄 deploy.yml
    - 📁 .vscode
        - 📄 generate_csv.py
        - 📄 analyse_vente.py
        - 📄 mobile_app.py  
        - 📄 README.md
        - 📄 requirement.txt
        - 📄 .gitignore
        - 📄 ventes.csv
        - 📄 status.html
## 📌 Application Web

- [Dashboard PFA_VENTES](https://pfavente-gyx58qbzl3yrvg6m59yz65.streamlit.app/)
- [Application SalesFlow](https://salesflow-app-nqms9juetgm5u2x4wgqr95.streamlit.app/)


## 🚀 Installation

### **Prérequis**
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- Git

### **Étapes d'Installation**
 1. **Cloner:**
 - git clone https://github.com/102-rou/pfa_ventes.git
 - cd pfa_ventes

 2. **Environnement virtuel:**
 - python -m venv venv
 - venv\Scripts\activate   

 3. **Dépendances:**
 - pip install -r requirements.txt

 4. **Générer les données:**
 - python generate_csv.py

 5. **Lancer:**
 - streamlit run app_mobile.py

## 📊 Résultats:

- Dashboard mobile interactif
- Graphiques statistiques (histogramme, barres,..)
- Export CSV automatique
- Recommandations stratégiques

## 🛠️ Technologies:
- Python 3.14
- Pandas 
- Faker
- Streamlit 
- Plotly
- Git & GitHub

## 👨‍💻 Auteur
Roudayna Marweni
Amal chaali
Mohammed amine Saadallah

## 📝 Licence
MIT
