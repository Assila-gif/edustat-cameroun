import os
import streamlit as st
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text

# Configuration de la page
st.set_page_config(
    page_title="EduStat L2 Informatique",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================= CUSTOM CSS (L'aspect "Réel/HTML") =================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=Space+Mono&display=swap');

/* Style global pour ressembler à une App Web */
html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
}

.stApp {
    background-color: #07071a;
    background-image: 
        radial-gradient(at 0% 0%, rgba(124, 58, 237, 0.1) 0, transparent 50%), 
        radial-gradient(at 100% 100%, rgba(6, 182, 212, 0.1) 0, transparent 50%);
}

/* Personnalisation de la Sidebar (Navigation latérale) */
[data-testid="stSidebar"] {
    background-color: #0c0c20 !important;
    border-right: 1px solid #1e1e40 !important;
}

/* Header stylisé en HTML Pur */
.main-header {
    background: linear-gradient(90deg, #1e1e40 0%, #0c0c20 100%);
    padding: 30px;
    border-radius: 15px;
    border: 1px solid #2a2a5a;
    margin-bottom: 30px;
    display: flex;
    align-items: center;
    gap: 20px;
}

.logo-container {
    background: #7c3aed;
    width: 60px;
    height: 60px;
    border-radius: 12px;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 30px;
    box-shadow: 0 0 20px rgba(124, 58, 237, 0.4);
}

.title-text h1 {
    margin: 0;
    color: #ffffff;
    font-size: 2.2rem;
    font-weight: 800;
}

.title-text p {
    margin: 0;
    color: #a855f7;
    font-family: 'Space Mono', monospace;
    font-size: 0.8rem;
    letter-spacing: 2px;
}

/* Cartes de statistiques (Dashboard) */
.stat-card {
    background: #0f0f2d;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #1e1e40;
    text-align: center;
    transition: transform 0.3s ease;
}
.stat-card:hover {
    transform: translateY(-5px);
    border-color: #7c3aed;
}

/* Inputs de la sidebar */
.stTextInput input, .stNumberInput input {
    background-color: #121235 !important;
    color: white !important;
    border: 1px solid #2a2a5a !important;
}

/* Badge Admis/Ajourné */
.badge {
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 10px;
    font-weight: bold;
    text-transform: uppercase;
}
.badge-admis { background: rgba(34, 197, 94, 0.2); color: #22c55e; border: 1px solid #22c55e; }
.badge-ajourne { background: rgba(239, 68, 68, 0.2); color: #ef4444; border: 1px solid #ef4444; }

</style>
""", unsafe_allow_html=True)

# ================= DATABASE & LOGIC =================
DATABASE_URL = "sqlite:///./edustat.db"
engine = create_engine(DATABASE_URL)

def init_db():
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                matricule TEXT, name TEXT, prenom TEXT, age INTEGER,
                prog1 FLOAT, structures FLOAT, maths FLOAT,
                moyenne_s1 FLOAT, moyenne_s2 FLOAT, moyenne_generale FLOAT
            )
        """))
        conn.commit()

init_db()

# ================= SIDEBAR (FORMULAIRE) =================
with st.sidebar:
    st.markdown("### ➕ Ajouter un étudiant")
    with st.form("add_student_form", clear_on_submit=True):
        nom_complet = st.text_input("Nom complet")
        matricule = st.text_input("Matricule", value="2026-L2-")
        age = st.number_input("Âge", 16, 50, 20)
        
        st.markdown("---")
        st.markdown("**Semestre 1**")
        p1 = st.number_input("Programmation", 0.0, 20.0, 0.0)
        s1 = st.number_input("Structures", 0.0, 20.0, 0.0)
        m1 = st.number_input("Mathématiques", 0.0, 20.0, 0.0)
        
        submitted = st.form_submit_button("ENREGISTRER L'ÉTUDIANT")
        
        if submitted:
            moy_s1 = round((p1 + s1 + m1) / 3, 2)
            # Pour l'exemple, on simule une moyenne S2 aléatoire si non saisie
            moy_s2 = 0.0 
            moy_gen = round((moy_s1 + moy_s2) / 2, 2) if moy_s2 > 0 else moy_s1
            
            with engine.connect() as conn:
                conn.execute(text("""
                    INSERT INTO students (matricule, name, prenom, age, prog1, structures, maths, moyenne_s1, moyenne_s2, moyenne_generale)
                    VALUES (:m, :n, :p, :a, :p1, :s1, :m1, :ms1, :ms2, :mg)
                """), {"m": matricule, "n": nom_complet, "p": "", "a": age, "p1": p1, "s1": s1, "m1": m1, "ms1": moy_s1, "ms2": 0.0, "mg": moy_s1})
                conn.commit()
            st.success("Étudiant ajouté !")
            st.rerun()

# ================= MAIN UI =================

# Header HTML
st.markdown("""
<div class="main-header">
    <div class="logo-container">🎓</div>
    <div class="title-text">
        <h1>EduStat</h1>
        <p>L2 INFORMATIQUE • ANALYSE DES PERFORMANCES</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Récupération des données
df = pd.read_sql("SELECT * FROM students", engine)

if df.empty:
    st.markdown("""
    <div style="text-align:center; padding:100px;">
        <img src="https://cdn-icons-png.flaticon.com/512/6598/6598519.png" width="100" style="opacity:0.2">
        <h3 style="color:#3a3a5a; margin-top:20px;">AUCUN ÉTUDIANT ENREGISTRÉ</h3>
        <p style="color:#2a2a4a;">Utilisez le formulaire à gauche pour commencer.</p>
    </div>
    """, unsafe_allow_html=True)
else:
    # Dashboard Metrics en colonnes HTML
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f"""<div class="stat-card">
            <p style="color:#6060a0; font-size:0.8rem;">MOYENNE CLASSE</p>
            <h2 style="color:white; margin:0;">{df['moyenne_generale'].mean():.2f}</h2>
        </div>""", unsafe_allow_html=True)
    with m2:
        st.markdown(f"""<div class="stat-card">
            <p style="color:#6060a0; font-size:0.8rem;">TOTAL ÉTUDIANTS</p>
            <h2 style="color:white; margin:0;">{len(df)}</h2>
        </div>""", unsafe_allow_html=True)
    with m3:
        taux = (df['moyenne_generale'] >= 10).sum() / len(df) * 100
        st.markdown(f"""<div class="stat-card">
            <p style="color:#6060a0; font-size:0.8rem;">TAUX RÉUSSITE</p>
            <h2 style="color:#22c55e; margin:0;">{taux:.1f}%</h2>
        </div>""", unsafe_allow_html=True)

    st.write("###")

    # Tableau des résultats
    st.markdown("#### 📋 Liste des étudiants")
    
    # Formatage pour l'affichage "Réel"
    display_df = df.copy()
    display_df['Status'] = display_df['moyenne_generale'].apply(
        lambda x: "✅ ADMIS" if x >= 10 else "❌ AJOURNÉ"
    )
    
    st.dataframe(
        display_df[['matricule', 'name', 'age', 'moyenne_s1', 'moyenne_generale', 'Status']],
        use_container_width=True,
        hide_index=True,
        column_config={
            "moyenne_generale": st.column_config.NumberColumn("Moy. Générale", format="%.2f / 20"),
            "Status": st.column_config.TextColumn("Résultat")
        }
    )

    # Graphique de performance
    st.write("###")
    st.markdown("#### 📈 Distribution des notes")
    st.area_chart(df.set_index('name')['moyenne_generale'], color="#7c3aed")

# Suppression (Optionnel)
with st.expander("⚙️ Paramètres avancés"):
    if st.button("Réinitialiser la base de données"):
        with engine.connect() as conn:
            conn.execute(text("DROP TABLE IF EXISTS students"))
            conn.commit()
        init_db()
        st.rerun()
