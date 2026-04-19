import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from analyse_vente import analyser_ventes, exporter_resultats, generer_rapport_texte

# Configuration mobile
st.set_page_config(
    page_title="PFA Dashboard 8 Variables",
    layout="centered",
    page_icon="📊"
)

# Style CSS mobile
st.markdown("""
<style>
    .main { background-color: #0a0c10; max-width: 500px; margin: 0 auto; }
    .kpi-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 15px;
        border-radius: 15px;
        margin: 8px 0;
        text-align: center;
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .kpi-small { background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); font-size: 14px; }
    .warning { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }
    h1, h2, h3, h4 { color: white; }
    .stButton button { width: 100%; background: #667eea; color: white; border-radius: 10px; padding: 10px; }
    .report-box {
        background: #1e1e2e;
        padding: 15px;
        border-radius: 10px;
        font-family: monospace;
        font-size: 12px;
        overflow-x: auto;
    }
</style>
""", unsafe_allow_html=True)

st.title("📱 PFA - Analyse Ventes")
st.caption("8 variables | Dashboard Mobile Interactif")

# Sidebar
with st.sidebar:
    st.header("📁 Importation")
    uploaded_file = st.file_uploader("Choisir ventes.csv", type=['csv'])
    
    if uploaded_file:
        with open("ventes.csv", "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success("✅ Fichier chargé !")
    
    st.divider()
    st.caption("🎯 **8 Variables disponibles :**")
    st.caption("ID | Prix | Quantité | Remise | Catégorie | Région | Date | Canal")

# SI fichier chargé
if uploaded_file is not None:
    # Analyse complète
    df, stats = analyser_ventes("ventes.csv")
    
    # ========== KPIS PRINCIPAUX ==========
    st.subheader("💰 INDICATEURS CLÉS")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <h4>CA Total Net</h4>
            <h2>{stats['ca_total']:,.0f} €</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="kpi-card kpi-small">
            <h4>TVA 20%</h4>
            <h2>{stats['tva_totale']:,.0f} €</h2>
        </div>
        """, unsafe_allow_html=True)
    
    col3, col4 = st.columns(2)
    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <h4>💰 Marge 30%</h4>
            <h2>{stats['marge_totale']:,.0f} €</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="kpi-card warning">
            <h4>🏆 Top Produit</h4>
            <h2>{stats['meilleur_produit']['id']}</h2>
            <small>{stats['meilleur_produit']['ca']:,.0f} €</small>
        </div>
        """, unsafe_allow_html=True)
    
    # ========== FILTRES INTERACTIFS ==========
    st.subheader("🔍 Filtres d'analyse")
    
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        categories = ['Toutes'] + list(df['Categorie'].unique())
        categorie_filtre = st.selectbox("Catégorie", categories)
    
    with col_f2:
        regions = ['Toutes'] + list(df['Region'].unique())
        region_filtre = st.selectbox("Région", regions)
    
    # Application des filtres
    df_filtre = df.copy()
    if categorie_filtre != 'Toutes':
        df_filtre = df_filtre[df_filtre['Categorie'] == categorie_filtre]
    if region_filtre != 'Toutes':
        df_filtre = df_filtre[df_filtre['Region'] == region_filtre]
    
    # ========== GRAPHIQUE 1 : CA par Catégorie ==========
    st.subheader("📊 CA Net par Catégorie")
    ca_categorie = df_filtre.groupby('Categorie')['CA_Net'].sum().reset_index()
    fig1 = px.bar(ca_categorie, x='Categorie', y='CA_Net', 
                  title="Chiffre d'Affaires par Catégorie",
                  color='CA_Net',
                  color_continuous_scale='Viridis',
                  text_auto='.2s')
    fig1.update_layout(template='plotly_dark', height=350, xaxis_tickangle=-45)
    st.plotly_chart(fig1, use_container_width=True)
    
    # ========== GRAPHIQUE 2 : CA par Région (carte choroplèthe simplifiée) ==========
    st.subheader("🗺️ CA Net par Région")
    ca_region = df_filtre.groupby('Region')['CA_Net'].sum().reset_index()
    fig2 = px.bar(ca_region, x='Region', y='CA_Net', 
                  title="Performance par Région",
                  color='CA_Net',
                  color_continuous_scale='Plasma')
    fig2.update_layout(template='plotly_dark', height=350)
    st.plotly_chart(fig2, use_container_width=True)
    
    # ========== GRAPHIQUE 3 : CA par Canal ==========
    st.subheader("📱 CA Net par Canal de vente")
    ca_canal = df_filtre.groupby('Canal')['CA_Net'].sum().reset_index()
    fig3 = px.pie(ca_canal, values='CA_Net', names='Canal',
                  title="Répartition du CA par Canal",
                  hole=0.3)
    fig3.update_layout(template='plotly_dark', height=350)
    st.plotly_chart(fig3, use_container_width=True)
    
    # ========== GRAPHIQUE 4 : Évolution mensuelle ==========
    st.subheader("📈 Évolution mensuelle du CA")
    fig4 = px.line(stats['evolution_mensuelle'], x='Mois', y='CA_Net',
                   title="Tendance des ventes sur 12 mois",
                   markers=True)
    fig4.update_layout(template='plotly_dark', height=350)
    st.plotly_chart(fig4, use_container_width=True)
    
    # ========== GRAPHIQUE 5 : Distribution des prix ==========
    st.subheader("📊 Distribution des prix")
    fig5 = px.histogram(df_filtre, x='Prix', nbins=30,
                        title="Répartition des prix des produits",
                        color_discrete_sequence=['#667eea'])
    fig5.update_layout(template='plotly_dark', height=300)
    st.plotly_chart(fig5, use_container_width=True)
    
    # ========== GRAPHIQUE 6 : Impact des remises ==========
    st.subheader("🎯 Impact des remises sur le CA")
    remise_stats = df_filtre.groupby('Remise')['CA_Net'].sum().reset_index()
    fig6 = px.bar(remise_stats, x='Remise', y='CA_Net',
                  title="CA Net selon le taux de remise",
                  color='CA_Net')
    fig6.update_layout(template='plotly_dark', height=350)
    st.plotly_chart(fig6, use_container_width=True)
    
    # ========== TABLEAUX STATISTIQUES ==========
    with st.expander("📋 Statistiques détaillées par Catégorie"):
        st.dataframe(stats['stats_categorie'], use_container_width=True)
    
    with st.expander("🗺️ Statistiques par Région"):
        st.dataframe(stats['stats_region'], use_container_width=True)
    
    with st.expander("📱 Statistiques par Canal"):
        st.dataframe(stats['stats_canal'], use_container_width=True)
    
    # ========== CONCLUSION ET SOLUTION ==========
    st.subheader("💡 CONCLUSION & SOLUTION")
    
    # Analyse intelligente
    meilleure_categorie = stats['stats_categorie']['CA_Net']['sum'].idxmax()
    meilleure_region = stats['stats_region']['CA_Net'].idxmax()
    meilleur_canal = stats['stats_canal']['CA_Net'].idxmax()
    
    conclusion = f"""
    ✅ **Diagnostic :**
    - Le CA Total est de **{stats['ca_total']:,.0f} €**
    - La catégorie **{meilleure_categorie}** est la plus performante
    - La région **{meilleure_region}** génère le plus de ventes
    - Le canal **{meilleur_canal}** est le plus rentable
    """
    
    solution = f"""
    🎯 **Recommandations stratégiques :**
    
    1. **Augmenter les investissements** sur la catégorie {meilleure_categorie}
    2. **Développer la présence** dans la région {meilleure_region}
    3. **Optimiser le canal** {meilleur_canal} avec plus de budget marketing
    4. **Produit star** {stats['meilleur_produit']['id']} à mettre en avant
    5. **Réduire les remises** sur les produits à forte demande
    """
    
    st.info(conclusion)
    st.success(solution)
    
    # Avertissement si besoin
    if stats['remise_moyenne'] > 20:
        st.warning(f"⚠️ **Attention** : La remise moyenne est élevée ({stats['remise_moyenne']:.0f}%). Envisagez de la réduire pour améliorer la marge.")
    
    # ========== RAPPORT TEXTE ==========
    with st.expander("📄 Voir le rapport complet"):
        rapport = generer_rapport_texte(stats)
        st.markdown(f'<div class="report-box"><pre>{rapport}</pre></div>', unsafe_allow_html=True)
    
    # ========== EXPORT ==========
    st.divider()
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("📥 Exporter resultats_final.csv"):
            exporter_resultats(df)
            st.success("Export réussi !")
    with col_btn2:
        if st.button("🔄 Réinitialiser"):
            st.rerun()
    
    st.balloons()

else:
    # État initial
    st.info("👈 **Bienvenue !**\n\n1. Clique sur la flèche **←** en haut à gauche\n2. Uploade ton fichier **ventes.csv**\n3. Découvre ton dashboard 8 variables")
    
    st.markdown("""
    ### 📋 Exemple de structure attendue :
                """)

print("✅ Application prête - Lance avec: streamlit run app_mobile.py")