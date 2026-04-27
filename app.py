import os
import streamlit as st

st.set_page_config(
    page_title="EduStat L2 Informatique",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text

# ================= CUSTOM CSS =================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
}

/* === DARK THEME BASE === */
.stApp {
    background: #0a0a0f;
    color: #e8e8f0;
}

/* === SIDEBAR === */
[data-testid="stSidebar"] {
    background: #0f0f1a !important;
    border-right: 1px solid #1e1e3a;
}
[data-testid="stSidebar"] * {
    color: #c8c8e0 !important;
}
[data-testid="stSidebar"] .stTextInput input,
[data-testid="stSidebar"] .stNumberInput input {
    background: #1a1a2e !important;
    border: 1px solid #2a2a4a !important;
    color: #e8e8f0 !important;
    border-radius: 6px !important;
}

/* === HEADER === */
.edu-header {
    background: linear-gradient(135deg, #0d0d1f 0%, #1a0a2e 50%, #0a1a2e 100%);
    border: 1px solid #2a1a4a;
    border-radius: 16px;
    padding: 2.5rem 2rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.edu-header::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(ellipse at 30% 50%, rgba(120,60,220,0.15) 0%, transparent 60%),
                radial-gradient(ellipse at 70% 50%, rgba(60,120,220,0.10) 0%, transparent 60%);
    pointer-events: none;
}
.edu-header h1 {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 2.8rem;
    background: linear-gradient(90deg, #a855f7, #3b82f6, #06b6d4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0 0 0.3rem 0;
    line-height: 1.1;
}
.edu-header p {
    font-family: 'Space Mono', monospace;
    font-size: 0.85rem;
    color: #6060a0;
    margin: 0;
    letter-spacing: 0.08em;
}

/* === METRIC CARDS === */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin-bottom: 2rem;
}
.metric-card {
    background: #0f0f1e;
    border: 1px solid #1e1e3a;
    border-radius: 12px;
    padding: 1.4rem 1.6rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s;
}
.metric-card::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    border-radius: 12px 12px 0 0;
}
.metric-card.purple::after { background: linear-gradient(90deg, #a855f7, #6d28d9); }
.metric-card.blue::after   { background: linear-gradient(90deg, #3b82f6, #1d4ed8); }
.metric-card.cyan::after   { background: linear-gradient(90deg, #06b6d4, #0891b2); }
.metric-card:hover { border-color: #3a3a6a; }
.metric-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    color: #6060a0;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}
.metric-value {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 2.2rem;
    color: #e8e8f0;
    line-height: 1;
}
.metric-sub {
    font-size: 0.78rem;
    color: #5050a0;
    margin-top: 0.3rem;
    font-family: 'Space Mono', monospace;
}

/* === SECTION TITLES === */
.section-title {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 1.1rem;
    color: #a855f7;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin: 2rem 0 1rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #1e1e3a;
}

/* === DATAFRAME === */
[data-testid="stDataFrame"] {
    border: 1px solid #1e1e3a;
    border-radius: 10px;
    overflow: hidden;
}

/* === BUTTONS === */
.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #4f46e5) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    padding: 0.6rem 1.5rem !important;
    width: 100% !important;
    transition: opacity 0.2s !important;
    letter-spacing: 0.05em !important;
}
.stButton > button:hover { opacity: 0.85 !important; }

/* === ALERTS === */
.stSuccess { background: #0a1f0a !important; border-left: 3px solid #22c55e !important; }
.stWarning { background: #1f1a0a !important; border-left: 3px solid #f59e0b !important; }

/* === CHARTS === */
[data-testid="stVegaLiteChart"] {
    background: #0f0f1e !important;
    border-radius: 10px;
    border: 1px solid #1e1e3a;
    padding: 1rem;
}

/* === RANK TABLE === */
.rank-row {
    display: flex;
    align-items: center;
    padding: 0.75rem 1rem;
    border-radius: 8px;
    margin-bottom: 0.4rem;
    background: #0f0f1e;
    border: 1px solid #1e1e3a;
    transition: border-color 0.2s;
}
.rank-row:hover { border-color: #3a3a6a; }
.rank-pos {
    font-family: 'Space Mono', monospace;
    font-weight: 700;
    font-size: 1.1rem;
    width: 2.5rem;
    color: #6060a0;
}
.rank-pos.gold   { color: #f59e0b; }
.rank-pos.silver { color: #94a3b8; }
.rank-pos.bronze { color: #b45309; }
.rank-name {
    flex: 1;
    font-weight: 600;
    font-size: 0.95rem;
    color: #e8e8f0;
}
.rank-score {
    font-family: 'Space Mono', monospace;
    font-weight: 700;
    font-size: 1rem;
    color: #a855f7;
}
.rank-bar-wrap {
    width: 100px;
    height: 4px;
    background: #1e1e3a;
    border-radius: 2px;
    margin: 0 1rem;
}
.rank-bar {
    height: 4px;
    border-radius: 2px;
    background: linear-gradient(90deg, #7c3aed, #06b6d4);
}

/* === BADGE === */
.badge {
    display: inline-block;
    padding: 0.2rem 0.7rem;
    border-radius: 999px;
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.05em;
}
.badge-pass { background: #052e16; color: #4ade80; border: 1px solid #166534; }
.badge-fail { background: #2d0a0a; color: #f87171; border: 1px solid #7f1d1d; }
</style>
""", unsafe_allow_html=True)

# ================= DATABASE =================
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./edustat.db")

@st.cache_resource
def get_engine():
    return create_engine(DATABASE_URL)

engine = get_engine()

# ================= CREATE TABLE =================
def create_table():
    if "postgresql" in DATABASE_URL:
        pk = "SERIAL PRIMARY KEY"
    else:
        pk = "INTEGER PRIMARY KEY AUTOINCREMENT"
    query = f"""
    CREATE TABLE IF NOT EXISTS students (
        id {pk},
        name TEXT,
        age INT,
        prog1 FLOAT, structures FLOAT, maths FLOAT,
        architecture FLOAT, systeme FLOAT, moyenne_s1 FLOAT,
        prog2 FLOAT, bdd FLOAT, reseaux FLOAT,
        genie_logiciel FLOAT, stats FLOAT,
        moyenne_s2 FLOAT, moyenne_generale FLOAT
    );
    """
    with engine.connect() as conn:
        conn.execute(text(query))
        conn.commit()

create_table()

# ================= LOAD DATA =================
@st.cache_data(ttl=5)
def load_data():
    try:
        return pd.read_sql("SELECT * FROM students ORDER BY id", engine)
    except:
        return pd.DataFrame()

# ================= DELETE =================
def delete_student(student_id):
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM students WHERE id = :id"), {"id": int(student_id)})
        conn.commit()

# ================= HEADER =================
st.markdown("""
<div class="edu-header">
    <h1>🎓 EduStat</h1>
    <p>L2 INFORMATIQUE · ANALYSE DES PERFORMANCES S1 & S2</p>
</div>
""", unsafe_allow_html=True)

# ================= SIDEBAR FORM =================
st.sidebar.markdown("## ➕ Ajouter un étudiant")
name = st.sidebar.text_input("Nom complet")
age  = st.sidebar.number_input("Âge", 15, 40, 20)

st.sidebar.markdown("**— Semestre 1 —**")
prog1        = st.sidebar.number_input("Programmation",  0.0, 20.0, step=0.5, key="p1")
structures   = st.sidebar.number_input("Structures",     0.0, 20.0, step=0.5, key="st")
maths        = st.sidebar.number_input("Maths",          0.0, 20.0, step=0.5, key="ma")
architecture = st.sidebar.number_input("Architecture",   0.0, 20.0, step=0.5, key="ar")
systeme      = st.sidebar.number_input("Système",        0.0, 20.0, step=0.5, key="sy")

st.sidebar.markdown("**— Semestre 2 —**")
prog2         = st.sidebar.number_input("Prog avancée",    0.0, 20.0, step=0.5, key="p2")
bdd           = st.sidebar.number_input("Base de données", 0.0, 20.0, step=0.5, key="bd")
reseaux       = st.sidebar.number_input("Réseaux",         0.0, 20.0, step=0.5, key="re")
genie_logiciel= st.sidebar.number_input("Génie logiciel",  0.0, 20.0, step=0.5, key="gl")
stats         = st.sidebar.number_input("Statistiques",    0.0, 20.0, step=0.5, key="sa")

st.sidebar.markdown("---")

if st.sidebar.button("✅ Enregistrer l'étudiant"):
    if name.strip() == "":
        st.sidebar.error("Le nom est obligatoire.")
    else:
        moy_s1  = round(np.mean([prog1, structures, maths, architecture, systeme]), 2)
        moy_s2  = round(np.mean([prog2, bdd, reseaux, genie_logiciel, stats]), 2)
        moy_gen = round(np.mean([moy_s1, moy_s2]), 2)
        new_data = pd.DataFrame([[
            name.strip(), age, prog1, structures, maths, architecture, systeme,
            moy_s1, prog2, bdd, reseaux, genie_logiciel, stats, moy_s2, moy_gen
        ]], columns=[
            "name","age","prog1","structures","maths","architecture","systeme",
            "moyenne_s1","prog2","bdd","reseaux","genie_logiciel","stats",
            "moyenne_s2","moyenne_generale"
        ])
        new_data.to_sql("students", engine, if_exists="append", index=False)
        st.cache_data.clear()
        st.sidebar.success(f"✅ {name} enregistré·e !")
        st.rerun()

# ================= LOAD =================
df = load_data()

if df.empty:
    st.markdown("""
    <div style="text-align:center; padding:4rem; color:#3a3a6a;">
        <div style="font-size:4rem">📭</div>
        <div style="font-family:'Space Mono',monospace; margin-top:1rem; font-size:0.9rem;">
            AUCUN ÉTUDIANT ENREGISTRÉ<br>
            <span style="font-size:0.75rem; color:#2a2a4a;">
                Utilisez le formulaire dans la barre latérale
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ================= METRICS =================
moy_filiere = df["moyenne_generale"].mean()
meilleur    = df.loc[df["moyenne_generale"].idxmax()]
nb_admis    = (df["moyenne_generale"] >= 10).sum()
taux        = round(nb_admis / len(df) * 100, 1)

st.markdown(f"""
<div class="metric-grid">
  <div class="metric-card purple">
    <div class="metric-label">Moyenne filière</div>
    <div class="metric-value">{moy_filiere:.2f}</div>
    <div class="metric-sub">/ 20 · {len(df)} étudiants</div>
  </div>
  <div class="metric-card blue">
    <div class="metric-label">Meilleur étudiant</div>
    <div class="metric-value">{meilleur['moyenne_generale']:.2f}</div>
    <div class="metric-sub">{meilleur['name']}</div>
  </div>
  <div class="metric-card cyan">
    <div class="metric-label">Taux de réussite</div>
    <div class="metric-value">{taux}%</div>
    <div class="metric-sub">{nb_admis} admis sur {len(df)}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ================= CLASSEMENT =================
st.markdown('<div class="section-title">🏅 Classement général</div>', unsafe_allow_html=True)

classement = df.sort_values("moyenne_generale", ascending=False).reset_index(drop=True)
max_score  = classement["moyenne_generale"].max()

medals = {0: ("gold","🥇"), 1: ("silver","🥈"), 2: ("bronze","🥉")}

for i, row in classement.iterrows():
    cls, emoji = medals.get(i, ("", f"#{i+1}"))
    pct = (row["moyenne_generale"] / max_score) * 100
    badge = '<span class="badge badge-pass">ADMIS</span>' if row["moyenne_generale"] >= 10 else '<span class="badge badge-fail">AJOURNÉ</span>'
    st.markdown(f"""
    <div class="rank-row">
        <div class="rank-pos {cls}">{emoji if cls else f'#{i+1}'}</div>
        <div class="rank-name">{row['name']}</div>
        {badge}
        <div class="rank-bar-wrap" style="margin-left:1rem">
            <div class="rank-bar" style="width:{pct:.0f}%"></div>
        </div>
        <div class="rank-score">{row['moyenne_generale']:.2f}</div>
    </div>
    """, unsafe_allow_html=True)

# ================= GRAPHIQUES =================
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="section-title">📈 Moyennes générales</div>', unsafe_allow_html=True)
    chart_data = classement.set_index("name")["moyenne_generale"]
    st.bar_chart(chart_data, color="#7c3aed")

with col2:
    st.markdown('<div class="section-title">📊 S1 vs S2</div>', unsafe_allow_html=True)
    chart_s = classement.set_index("name")[["moyenne_s1","moyenne_s2"]]
    st.bar_chart(chart_s)

# ================= MATIÈRES =================
st.markdown('<div class="section-title">📚 Détail par matière (moyennes)</div>', unsafe_allow_html=True)

matieres = {
    "Prog S1": df["prog1"].mean(), "Structures": df["structures"].mean(),
    "Maths": df["maths"].mean(), "Architecture": df["architecture"].mean(),
    "Système": df["systeme"].mean(), "Prog S2": df["prog2"].mean(),
    "BDD": df["bdd"].mean(), "Réseaux": df["reseaux"].mean(),
    "Génie Log.": df["genie_logiciel"].mean(), "Statistiques": df["stats"].mean(),
}
mat_df = pd.DataFrame({"Matière": list(matieres.keys()), "Moyenne": list(matieres.values())})
mat_df = mat_df.sort_values("Moyenne", ascending=False)

cols = st.columns(5)
for i, (_, row) in enumerate(mat_df.iterrows()):
    color = "#22c55e" if row["Moyenne"] >= 12 else "#f59e0b" if row["Moyenne"] >= 10 else "#f87171"
    with cols[i % 5]:
        st.markdown(f"""
        <div style="background:#0f0f1e;border:1px solid #1e1e3a;border-radius:8px;
                    padding:0.9rem;text-align:center;margin-bottom:0.5rem;">
            <div style="font-family:'Space Mono',monospace;font-size:0.65rem;
                        color:#6060a0;text-transform:uppercase;margin-bottom:0.3rem;">
                {row['Matière']}
            </div>
            <div style="font-size:1.4rem;font-weight:800;color:{color}">
                {row['Moyenne']:.1f}
            </div>
        </div>
        """, unsafe_allow_html=True)

# ================= TABLEAU COMPLET =================
st.markdown('<div class="section-title">📋 Données complètes</div>', unsafe_allow_html=True)
st.dataframe(
    df.drop(columns=["id"]),
    use_container_width=True,
    hide_index=True,
    column_config={
        "name": "Nom", "age": "Âge",
        "prog1": "Prog S1", "structures": "Structures", "maths": "Maths",
        "architecture": "Architecture", "systeme": "Système", "moyenne_s1": "Moy. S1",
        "prog2": "Prog S2", "bdd": "BDD", "reseaux": "Réseaux",
        "genie_logiciel": "Génie Log.", "stats": "Stats", "moyenne_s2": "Moy. S2",
        "moyenne_generale": st.column_config.NumberColumn("Moy. Générale", format="%.2f"),
    }
)

# ================= SUPPRESSION =================
with st.expander("🗑️ Supprimer un étudiant"):
    if not df.empty:
        options = {f"{row['name']} (id={row['id']})": row['id'] for _, row in df.iterrows()}
        choix = st.selectbox("Choisir un étudiant", list(options.keys()))
        if st.button("Supprimer", type="secondary"):
            delete_student(options[choix])
            st.cache_data.clear()
            st.success("Supprimé.")
            st.rerun()

# ================= FOOTER =================
st.markdown("""
<div style="text-align:center;padding:2rem 0;margin-top:2rem;
            border-top:1px solid #1e1e3a;font-family:'Space Mono',monospace;
            font-size:0.7rem;color:#2a2a4a;letter-spacing:0.1em;">
    EDUSTAT · L2 INFORMATIQUE · BUILT WITH STREAMLIT
</div>
""", unsafe_allow_html=True)
