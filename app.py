import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine, text
from sklearn.linear_model import LinearRegression

# Configuration de la page
st.set_page_config(
    page_title="EduStat Pro - L2 Informatique",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================= DESIGN & ANIMATIONS (CSS AVANCÉ) =================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=Space+Mono&display=swap');

/* Fond plus épais et texturé */
.stApp {
    background-color: #050514;
    background-image: 
        linear-gradient(rgba(124, 58, 237, 0.05) 2px, transparent 2px),
        linear-gradient(90deg, rgba(124, 58, 237, 0.05) 2px, transparent 2px);
    background-size: 50px 50px;
}

/* Bordures épaisses pour séparer les sections */
[data-testid="stSidebar"] {
    background-color: #0a0a1f !important;
    border-right: 5px solid #1e1e40 !important;
}

.main-header {
    background: #0f0f2d;
    border: 4px solid #2a2a5a;
    border-radius: 20px;
    padding: 2rem;
    margin-bottom: 2rem;
    box-shadow: 10px 10px 0px #1e1e40;
}

/* Animations au clic sur boutons et champs */
button, input, select, textarea {
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

button:active {
    transform: scale(0.95) !important;
    background: #a855f7 !important;
}

input:focus {
    border: 3px solid #7c3aed !important;
    box-shadow: 0 0 15px rgba(124, 58, 237, 0.4) !important;
    transform: translateY(-2px);
}

/* Cartes statistiques */
.stat-card {
    background: #0f0f2d;
    padding: 20px;
    border-radius: 15px;
    border: 3px solid #1e1e40;
    box-shadow: 5px 5px 0px #1e1e40;
}
</style>
""", unsafe_allow_html=True)

# ================= BASE DE DONNÉES =================
DATABASE_URL = "sqlite:///./edustat_pro.db"
engine = create_engine(DATABASE_URL)

def init_db():
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS students_v2 (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                matricule TEXT, nom TEXT, prenom TEXT, age INTEGER,
                maths_fond FLOAT, proba_stats FLOAT, 
                archi_syst FLOAT, reseaux FLOAT,
                algorigthmique FLOAT, bdd_sql FLOAT,
                genie_logiciel FLOAT, anglais FLOAT,
                moy_s1 FLOAT, moy_s2 FLOAT, moy_gen FLOAT
            )
        """))
        conn.commit()

init_db()

# ================= SIDEBAR : FORMULAIRE COMPLET L2 =================
with st.sidebar:
    st.markdown("### 📝 DOSSIER ÉTUDIANT L2")
    with st.form("form_l2", clear_on_submit=True):
        st.markdown("**Identité**")
        col_id1, col_id2 = st.columns(2)
        nom = col_id1.text_input("Nom")
        prenom = col_id2.text_input("Prénom")
        mat = st.text_input("Matricule (ex: 24L2000)")
        age = st.number_input("Âge", 16, 45, 20)

        st.markdown("---")
        st.markdown("**Bloc Scientifique**")
        c1, c2 = st.columns(2)
        m_fond = c1.number_input("Maths Fond.", 0.0, 20.0, 10.0)
        proba = c2.number_input("Proba / Stats", 0.0, 20.0, 10.0)

        st.markdown("**Bloc Technique & Système**")
        c3, c4 = st.columns(2)
        archi = c3.number_input("Archi / Syst.", 0.0, 20.0, 10.0)
        res = c4.number_input("Réseaux", 0.0, 20.0, 10.0)

        st.markdown("**Bloc Développement**")
        c5, c6 = st.columns(2)
        algo = c5.number_input("Algorithmique", 0.0, 20.0, 10.0)
        bdd = c6.number_input("BDD / SQL", 0.0, 20.0, 10.0)

        st.markdown("**Transversal**")
        c7, c8 = st.columns(2)
        gl = c7.number_input("Génie Log.", 0.0, 20.0, 10.0)
        ang = c8.number_input("Anglais Tech.", 0.0, 20.0, 10.0)

        submit = st.form_submit_button("VALIDER L'INSCRIPTION")

        if submit:
            # Calcul automatique des moyennes
            s1 = (m_fond + archi + algo + ang) / 4
            s2 = (proba + res + bdd + gl) / 4
            gen = (s1 + s2) / 2
            
            with engine.connect() as conn:
                conn.execute(text("""
                    INSERT INTO students_v2 (matricule, nom, prenom, age, maths_fond, proba_stats, archi_syst, reseaux, algorigthmique, bdd_sql, genie_logiciel, anglais, moy_s1, moy_s2, moy_gen)
                    VALUES (:m, :n, :p, :a, :m1, :m2, :m3, :m4, :m5, :m6, :m7, :m8, :s1, :s2, :gen)
                """), {"m": mat, "n": nom, "p": prenom, "a": age, "m1": m_fond, "m2": proba, "m3": archi, "m4": res, "m5": algo, "m6": bdd, "m7": gl, "m8": ang, "s1": s1, "s2": s2, "gen": gen})
                conn.commit()
            st.success("Données synchronisées !")
            st.rerun()

# ================= DASHBOARD PRINCIPAL =================
df = pd.read_sql("SELECT * FROM students_v2", engine)

# Header
st.markdown("""
<div class="main-header">
    <div style="display: flex; align-items: center; gap: 25px;">
        <div style="font-size: 50px; background: #7c3aed; padding: 15px; border-radius: 15px;">📊</div>
        <div>
            <h1 style="margin:0; color:white; font-family: 'Syne', sans-serif;">EduStat PRO <span style="color:#7c3aed;">L2</span></h1>
            <p style="margin:0; color:#6060a0; font-family: 'Space Mono';">CENTRE DE GESTION ACADÉMIQUE AVANCÉ</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

if df.empty:
    st.warning("En attente de données... Veuillez remplir le formulaire à gauche.")
else:
    tab1, tab2, tab3 = st.tabs(["📉 Tableau de Bord", "🔍 Analyse Prédictive", "📋 Registre"])

    with tab1:
        # Metrics
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Moyenne Générale", f"{df['moy_gen'].mean():.2f}")
        m2.metric("Meilleure Note", f"{df['moy_gen'].max():.2f}")
        m3.metric("Effectif", len(df))
        taux = (df['moy_gen'] >= 10).sum() / len(df) * 100
        m4.metric("Taux de Réussite", f"{taux:.1f}%")

        st.markdown("---")
        
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.markdown("#### 📊 Comparaison S1 vs S2")
            fig_compare = px.bar(df, x="nom", y=["moy_s1", "moy_s2"], barmode="group",
                                color_discrete_sequence=['#7c3aed', '#06b6d4'],
                                template="plotly_dark")
            st.plotly_chart(fig_compare, use_container_width=True)

        with col_right:
            st.markdown("#### 🥧 Répartition des niveaux")
            bins = [0, 10, 12, 14, 20]
            labels = ['Ajourné', 'Passable', 'Assez Bien', 'Bien/Très Bien']
            df['Mention'] = pd.cut(df['moy_gen'], bins=bins, labels=labels)
            fig_pie = px.pie(df, names="Mention", color_discrete_sequence=px.colors.sequential.Purp_r,
                             hole=0.4, template="plotly_dark")
            st.plotly_chart(fig_pie, use_container_width=True)

    with tab2:
        st.markdown("### 🤖 Régression Linéaire & Prédictions")
        st.write("Analyse de la corrélation entre les **Mathématiques** et la **Moyenne Générale**.")
        
        if len(df) > 1:
            X = df[['maths_fond']].values
            y = df['moy_gen'].values
            model = LinearRegression().fit(X, y)
            prediction = model.predict(X)

            fig_reg = go.Figure()
            fig_reg.add_trace(go.Scatter(x=df['maths_fond'], y=df['moy_gen'], mode='markers', name='Étudiants', marker=dict(color='#06b6d4', size=10)))
            fig_reg.add_trace(go.Scatter(x=df['maths_fond'], y=prediction, mode='lines', name='Ligne de Régression', line=dict(color='#7c3aed', width=3)))
            fig_reg.update_layout(template="plotly_dark", xaxis_title="Note en Mathématiques Fond.", yaxis_title="Moyenne Générale")
            st.plotly_chart(fig_reg, use_container_width=True)
            
            st.info(f"💡 Coefficient de corrélation : **{model.score(X, y):.2f}**. Plus ce score est proche de 1, plus les maths influencent la réussite générale.")
        else:
            st.info("Besoin d'au moins 2 étudiants pour calculer la régression.")

    with tab3:
        st.markdown("#### 📋 Liste complète des résultats")
        st.dataframe(df.style.highlight_max(axis=0, color='#1e1e40'), use_container_width=True)

# Bouton de nettoyage
if st.sidebar.button("🗑️ Vider la base"):
    with engine.connect() as conn:
        conn.execute(text("DROP TABLE students_v2"))
        conn.commit()
    st.rerun()
