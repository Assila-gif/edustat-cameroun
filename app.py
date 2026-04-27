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
import hashlib

# ================= CUSTOM CSS =================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
}

/* === DARK THEME BASE === */
.stApp {
    background: #07071a;
    background-image:
        radial-gradient(ellipse at 20% 0%, rgba(120,60,220,0.18) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 100%, rgba(60,120,220,0.12) 0%, transparent 50%),
        repeating-linear-gradient(
            0deg,
            transparent,
            transparent 60px,
            rgba(255,255,255,0.012) 60px,
            rgba(255,255,255,0.012) 61px
        ),
        repeating-linear-gradient(
            90deg,
            transparent,
            transparent 60px,
            rgba(255,255,255,0.012) 60px,
            rgba(255,255,255,0.012) 61px
        );
    color: #e8e8f0;
}

/* === SIDEBAR === */
[data-testid="stSidebar"] {
    background: #0c0c20 !important;
    border-right: 3px solid #2a1a5a !important;
    box-shadow: 4px 0 30px rgba(120,60,220,0.12);
}
[data-testid="stSidebar"] * {
    color: #c8c8e0 !important;
}
[data-testid="stSidebar"] .stTextInput input,
[data-testid="stSidebar"] .stNumberInput input {
    background: #12122e !important;
    border: 2px solid #2a2a5a !important;
    color: #e8e8f0 !important;
    border-radius: 8px !important;
    transition: border-color 0.25s ease, box-shadow 0.25s ease, transform 0.15s ease !important;
}
[data-testid="stSidebar"] .stTextInput input:focus,
[data-testid="stSidebar"] .stNumberInput input:focus {
    border-color: #7c3aed !important;
    box-shadow: 0 0 0 3px rgba(124,58,237,0.25) !important;
    transform: scale(1.01) !important;
    outline: none !important;
}
[data-testid="stSidebar"] .stTextInput input:hover,
[data-testid="stSidebar"] .stNumberInput input:hover {
    border-color: #4a3a8a !important;
}

/* === HEADER === */
.edu-header {
    background: linear-gradient(135deg, #0d0d1f 0%, #1a0a2e 50%, #0a1a2e 100%);
    border: 3px solid #2a1a5a;
    border-radius: 20px;
    padding: 2.5rem 2rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 8px 40px rgba(120,60,220,0.15), inset 0 1px 0 rgba(255,255,255,0.05);
}
.edu-header::before {
    content: '';
    position: absolute;
    top: -50%; left: -50%;
    width: 200%; height: 200%;
    background: radial-gradient(ellipse at 30% 50%, rgba(120,60,220,0.18) 0%, transparent 60%),
                radial-gradient(ellipse at 70% 50%, rgba(60,120,220,0.12) 0%, transparent 60%);
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
    gap: 1.2rem;
    margin-bottom: 2rem;
}
.metric-card {
    background: #0f0f22;
    border: 3px solid #1e1e40;
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s, transform 0.2s, box-shadow 0.3s;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
}
.metric-card::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 16px 16px 0 0;
}
.metric-card.purple::after { background: linear-gradient(90deg, #a855f7, #6d28d9); }
.metric-card.blue::after   { background: linear-gradient(90deg, #3b82f6, #1d4ed8); }
.metric-card.cyan::after   { background: linear-gradient(90deg, #06b6d4, #0891b2); }
.metric-card:hover {
    border-color: #3a3a7a;
    transform: translateY(-3px);
    box-shadow: 0 8px 30px rgba(120,60,220,0.2);
}
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
    border-bottom: 3px solid #2a1a5a;
}

/* === DATAFRAME === */
[data-testid="stDataFrame"] {
    border: 3px solid #1e1e40;
    border-radius: 14px;
    overflow: hidden;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
}

/* === BUTTONS === */
.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #4f46e5) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    padding: 0.6rem 1.5rem !important;
    width: 100% !important;
    transition: opacity 0.2s, transform 0.15s, box-shadow 0.2s !important;
    letter-spacing: 0.05em !important;
    box-shadow: 0 4px 15px rgba(124,58,237,0.3) !important;
}
.stButton > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-2px) scale(1.01) !important;
    box-shadow: 0 8px 25px rgba(124,58,237,0.45) !important;
}
.stButton > button:active {
    transform: scale(0.97) !important;
    box-shadow: 0 2px 8px rgba(124,58,237,0.3) !important;
}

/* === ALERTS === */
.stSuccess { background: #0a1f0a !important; border-left: 4px solid #22c55e !important; border-radius: 8px !important; }
.stWarning { background: #1f1a0a !important; border-left: 4px solid #f59e0b !important; border-radius: 8px !important; }
.stError   { background: #1f0a0a !important; border-left: 4px solid #ef4444 !important; border-radius: 8px !important; }

/* === CHARTS === */
[data-testid="stVegaLiteChart"] {
    background: #0f0f22 !important;
    border-radius: 14px;
    border: 3px solid #1e1e40;
    padding: 1rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.25);
}

/* === RANK TABLE === */
.rank-row {
    display: flex;
    align-items: center;
    padding: 0.85rem 1.2rem;
    border-radius: 10px;
    margin-bottom: 0.5rem;
    background: #0f0f22;
    border: 3px solid #1e1e40;
    transition: border-color 0.2s, transform 0.2s, box-shadow 0.2s;
}
.rank-row:hover {
    border-color: #3a3a7a;
    transform: translateX(4px);
    box-shadow: 0 4px 20px rgba(120,60,220,0.15);
}
.rank-pos { font-family: 'Space Mono', monospace; font-weight: 700; font-size: 1.1rem; width: 2.5rem; color: #6060a0; }
.rank-pos.gold   { color: #f59e0b; }
.rank-pos.silver { color: #94a3b8; }
.rank-pos.bronze { color: #b45309; }
.rank-name { flex: 1; font-weight: 600; font-size: 0.95rem; color: #e8e8f0; }
.rank-score { font-family: 'Space Mono', monospace; font-weight: 700; font-size: 1rem; color: #a855f7; }
.rank-bar-wrap { width: 100px; height: 5px; background: #1e1e3a; border-radius: 3px; margin: 0 1rem; }
.rank-bar { height: 5px; border-radius: 3px; background: linear-gradient(90deg, #7c3aed, #06b6d4); }

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
.badge-pass { background: #052e16; color: #4ade80; border: 2px solid #166534; }
.badge-fail { background: #2d0a0a; color: #f87171; border: 2px solid #7f1d1d; }

/* === LOGIN CARD === */
.login-card {
    max-width: 420px;
    margin: 5rem auto;
    background: #0f0f22;
    border: 3px solid #2a1a5a;
    border-radius: 20px;
    padding: 2.5rem;
    box-shadow: 0 20px 60px rgba(120,60,220,0.2);
    text-align: center;
}
.login-card h2 {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 1.6rem;
    background: linear-gradient(90deg, #a855f7, #3b82f6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.4rem;
}
.login-card p {
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    color: #4040a0;
    margin-bottom: 2rem;
}

/* === ABOUT CARD === */
.about-card {
    background: #0f0f22;
    border: 3px solid #2a1a5a;
    border-radius: 16px;
    padding: 2rem;
    margin-top: 1rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    line-height: 1.8;
}
.about-card h3 {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 1.1rem;
    color: #a855f7;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.7rem;
}
.about-card p, .about-card li {
    font-size: 0.92rem;
    color: #a0a0c8;
    font-family: 'Syne', sans-serif;
}
.about-card ul { padding-left: 1.2rem; margin-top: 0.5rem; }
.about-card li { margin-bottom: 0.4rem; }

/* === SELECTBOX & EXPANDER === */
[data-testid="stSelectbox"] > div > div {
    background: #12122e !important;
    border: 2px solid #2a2a5a !important;
    border-radius: 8px !important;
    transition: border-color 0.25s ease !important;
}
[data-testid="stSelectbox"] > div > div:focus-within {
    border-color: #7c3aed !important;
    box-shadow: 0 0 0 3px rgba(124,58,237,0.2) !important;
}
[data-testid="stExpander"] {
    border: 3px solid #1e1e40 !important;
    border-radius: 14px !important;
    background: #0f0f22 !important;
}

/* === TABS === */
[data-testid="stTabs"] [role="tablist"] {
    border-bottom: 3px solid #1e1e40 !important;
}
[data-testid="stTabs"] [role="tab"] {
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    color: #6060a0 !important;
    transition: color 0.2s !important;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    color: #a855f7 !important;
    border-bottom: 3px solid #a855f7 !important;
}

/* Align sidebar top with main content */
[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.5rem;
}
section[data-testid="stSidebarContent"] {
    padding-top: 0 !important;
}
</style>
""", unsafe_allow_html=True)

# ================= DATABASE =================
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./edustat.db")

@st.cache_resource
def get_engine():
    return create_engine(DATABASE_URL)

engine = get_engine()

# ================= CREATE TABLES =================
def create_tables():
    if "postgresql" in DATABASE_URL:
        pk = "SERIAL PRIMARY KEY"
    else:
        pk = "INTEGER PRIMARY KEY AUTOINCREMENT"

    students_query = f"""
    CREATE TABLE IF NOT EXISTS students (
        id {pk},
        matricule TEXT,
        name TEXT,
        prenom TEXT,
        age INT,
        prog1 FLOAT, structures FLOAT, maths FLOAT,
        architecture FLOAT, systeme FLOAT, moyenne_s1 FLOAT,
        prog2 FLOAT, bdd FLOAT, reseaux FLOAT,
        genie_logiciel FLOAT, stats FLOAT,
        moyenne_s2 FLOAT, moyenne_generale FLOAT
    );
    """
    admin_query = f"""
    CREATE TABLE IF NOT EXISTS admins (
        id {pk},
        username TEXT UNIQUE,
        password_hash TEXT
    );
    """
    with engine.connect() as conn:
        conn.execute(text(students_query))
        conn.execute(text(admin_query))
        # Insert default admin if not exists
        existing = conn.execute(text("SELECT COUNT(*) FROM admins")).fetchone()[0]
        if existing == 0:
            default_hash = hashlib.sha256("admin123".encode()).hexdigest()
            conn.execute(
                text("INSERT INTO admins (username, password_hash) VALUES (:u, :p)"),
                {"u": "admin", "p": default_hash}
            )
        conn.commit()

create_tables()

# ================= AUTH =================
def check_login(username, password):
    pw_hash = hashlib.sha256(password.encode()).hexdigest()
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT id FROM admins WHERE username=:u AND password_hash=:p"),
            {"u": username, "p": pw_hash}
        ).fetchone()
    return result is not None

def change_password(username, old_pw, new_pw):
    if check_login(username, old_pw):
        new_hash = hashlib.sha256(new_pw.encode()).hexdigest()
        with engine.connect() as conn:
            conn.execute(
                text("UPDATE admins SET password_hash=:p WHERE username=:u"),
                {"p": new_hash, "u": username}
            )
            conn.commit()
        return True
    return False

# ================= SESSION STATE =================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "admin_user" not in st.session_state:
    st.session_state.admin_user = ""

# ================= LOGIN PAGE =================
if not st.session_state.logged_in:
    st.markdown("""
    <div class="edu-header" style="max-width:500px;margin:3rem auto 0 auto;text-align:center;">
        <h1>🎓 EduStat</h1>
        <p>L2 INFORMATIQUE · ACCÈS ADMINISTRATEUR</p>
    </div>
    """, unsafe_allow_html=True)

    col_c, col_m, col_c2 = st.columns([1,2,1])
    with col_m:
        st.markdown('<div class="section-title">🔐 Connexion</div>', unsafe_allow_html=True)
        login_user = st.text_input("Identifiant", placeholder="admin")
        login_pw   = st.text_input("Mot de passe", type="password", placeholder="••••••••")
        if st.button("✅ Se connecter"):
            if check_login(login_user, login_pw):
                st.session_state.logged_in = True
                st.session_state.admin_user = login_user
                st.rerun()
            else:
                st.error("Identifiant ou mot de passe incorrect.")
        st.markdown("""
        <p style="text-align:center;font-family:'Space Mono',monospace;font-size:0.72rem;
                  color:#3a3a7a;margin-top:1.2rem;">
            Compte par défaut : admin / admin123
        </p>
        """, unsafe_allow_html=True)
    st.stop()

# ================= LOAD DATA =================
@st.cache_data(ttl=5)
def load_data():
    try:
        return pd.read_sql("SELECT * FROM students ORDER BY id", engine)
    except:
        return pd.DataFrame()

def delete_student(student_id):
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM students WHERE id = :id"), {"id": int(student_id)})
        conn.commit()

def update_student(student_id, fields: dict):
    set_clause = ", ".join([f"{k}=:{k}" for k in fields])
    fields["id"] = student_id
    with engine.connect() as conn:
        conn.execute(text(f"UPDATE students SET {set_clause} WHERE id=:id"), fields)
        conn.commit()

# ================= SIDEBAR =================
with st.sidebar:
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:0.6rem;margin-bottom:1.2rem;
                padding:0.8rem 1rem;background:#12122e;border-radius:10px;
                border:2px solid #2a2a5a;">
        <div style="font-size:1.3rem">👤</div>
        <div>
            <div style="font-family:'Syne',sans-serif;font-weight:700;font-size:0.9rem;color:#a855f7;">
                {st.session_state.admin_user}
            </div>
            <div style="font-family:'Space Mono',monospace;font-size:0.65rem;color:#4040a0;">ADMINISTRATEUR</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🔓 Déconnexion"):
        st.session_state.logged_in = False
        st.session_state.admin_user = ""
        st.rerun()

    st.markdown("---")
    st.markdown("## ➕ Ajouter un étudiant")

    matricule = st.text_input("Matricule", placeholder="EX: 22G0001")
    name      = st.text_input("Nom de famille")
    prenom    = st.text_input("Prénom")
    age       = st.number_input("Âge", 15, 40, 20)

    st.markdown("**— Semestre 1 —**")
    prog1        = st.number_input("Programmation",  0.0, 20.0, step=0.5, key="p1")
    structures   = st.number_input("Structures",     0.0, 20.0, step=0.5, key="st")
    maths        = st.number_input("Maths",          0.0, 20.0, step=0.5, key="ma")
    architecture = st.number_input("Architecture",   0.0, 20.0, step=0.5, key="ar")
    systeme      = st.number_input("Système",        0.0, 20.0, step=0.5, key="sy")

    st.markdown("**— Semestre 2 —**")
    prog2          = st.number_input("Prog avancée",    0.0, 20.0, step=0.5, key="p2")
    bdd            = st.number_input("Base de données", 0.0, 20.0, step=0.5, key="bd")
    reseaux        = st.number_input("Réseaux",         0.0, 20.0, step=0.5, key="re")
    genie_logiciel = st.number_input("Génie logiciel",  0.0, 20.0, step=0.5, key="gl")
    stats_note     = st.number_input("Statistiques",    0.0, 20.0, step=0.5, key="sa")

    st.markdown("---")
    if st.button("✅ Enregistrer l'étudiant"):
        if name.strip() == "" or prenom.strip() == "" or matricule.strip() == "":
            st.error("Matricule, nom et prénom sont obligatoires.")
        else:
            moy_s1  = round(np.mean([prog1, structures, maths, architecture, systeme]), 2)
            moy_s2  = round(np.mean([prog2, bdd, reseaux, genie_logiciel, stats_note]), 2)
            moy_gen = round(np.mean([moy_s1, moy_s2]), 2)
            new_data = pd.DataFrame([[
                matricule.strip(), name.strip(), prenom.strip(), age,
                prog1, structures, maths, architecture, systeme, moy_s1,
                prog2, bdd, reseaux, genie_logiciel, stats_note, moy_s2, moy_gen
            ]], columns=[
                "matricule","name","prenom","age",
                "prog1","structures","maths","architecture","systeme","moyenne_s1",
                "prog2","bdd","reseaux","genie_logiciel","stats","moyenne_s2","moyenne_generale"
            ])
            new_data.to_sql("students", engine, if_exists="append", index=False)
            st.cache_data.clear()
            st.success(f"✅ {prenom} {name} enregistré·e !")
            st.rerun()

    # Change password
    st.markdown("---")
    with st.expander("🔑 Changer le mot de passe"):
        old_pw  = st.text_input("Ancien mot de passe", type="password", key="old_pw")
        new_pw  = st.text_input("Nouveau mot de passe", type="password", key="new_pw")
        new_pw2 = st.text_input("Confirmer",            type="password", key="new_pw2")
        if st.button("Modifier"):
            if new_pw != new_pw2:
                st.error("Les mots de passe ne correspondent pas.")
            elif len(new_pw) < 6:
                st.error("Minimum 6 caractères.")
            elif change_password(st.session_state.admin_user, old_pw, new_pw):
                st.success("Mot de passe modifié !")
            else:
                st.error("Ancien mot de passe incorrect.")

# ================= HEADER =================
st.markdown("""
<div class="edu-header">
    <h1>🎓 EduStat</h1>
    <p>L2 INFORMATIQUE · ANALYSE DES PERFORMANCES S1 & S2</p>
</div>
""", unsafe_allow_html=True)

# ================= LOAD =================
df = load_data()

# ================= TABS =================
tab_dash, tab_analyse, tab_regression, tab_about = st.tabs([
    "📊 Tableau de bord",
    "🔍 Analyse détaillée",
    "📈 Régression & Stats",
    "ℹ️ À propos"
])

# ============================================================
# TAB 1 — TABLEAU DE BORD
# ============================================================
with tab_dash:
    if df.empty:
        st.markdown("""
        <div style="text-align:center;padding:4rem;color:#3a3a6a;">
            <div style="font-size:4rem">📭</div>
            <div style="font-family:'Space Mono',monospace;margin-top:1rem;font-size:0.9rem;">
                AUCUN ÉTUDIANT ENREGISTRÉ<br>
                <span style="font-size:0.75rem;color:#2a2a4a;">
                    Utilisez le formulaire dans la barre latérale
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
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
            <div class="metric-sub">{meilleur['prenom']} {meilleur['name']}</div>
          </div>
          <div class="metric-card cyan">
            <div class="metric-label">Taux de réussite</div>
            <div class="metric-value">{taux}%</div>
            <div class="metric-sub">{nb_admis} admis sur {len(df)}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Classement
        st.markdown('<div class="section-title">🏅 Classement général</div>', unsafe_allow_html=True)
        classement = df.sort_values("moyenne_generale", ascending=False).reset_index(drop=True)
        max_score  = classement["moyenne_generale"].max()
        medals = {0: ("gold","🥇"), 1: ("silver","🥈"), 2: ("bronze","🥉")}

        for i, row in classement.iterrows():
            cls, emoji = medals.get(i, ("", f"#{i+1}"))
            pct   = (row["moyenne_generale"] / max_score) * 100
            badge = '<span class="badge badge-pass">ADMIS</span>' if row["moyenne_generale"] >= 10 \
                    else '<span class="badge badge-fail">AJOURNÉ</span>'
            st.markdown(f"""
            <div class="rank-row">
                <div class="rank-pos {cls}">{emoji if cls else f'#{i+1}'}</div>
                <div class="rank-name">{row['prenom']} {row['name']}
                    <span style="font-family:'Space Mono',monospace;font-size:0.7rem;color:#4040a0;margin-left:0.5rem;">
                        {row['matricule']}
                    </span>
                </div>
                {badge}
                <div class="rank-bar-wrap" style="margin-left:1rem">
                    <div class="rank-bar" style="width:{pct:.0f}%"></div>
                </div>
                <div class="rank-score">{row['moyenne_generale']:.2f}</div>
            </div>
            """, unsafe_allow_html=True)

        # Graphiques
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="section-title">📈 Moyennes générales</div>', unsafe_allow_html=True)
            chart_data = classement.set_index("name")["moyenne_generale"]
            st.bar_chart(chart_data, color="#7c3aed")
        with col2:
            st.markdown('<div class="section-title">📊 S1 vs S2</div>', unsafe_allow_html=True)
            chart_s = classement.set_index("name")[["moyenne_s1","moyenne_s2"]]
            st.bar_chart(chart_s)

        # Matières
        st.markdown('<div class="section-title">📚 Détail par matière (moyennes)</div>', unsafe_allow_html=True)
        matieres = {
            "Prog S1": df["prog1"].mean(), "Structures": df["structures"].mean(),
            "Maths": df["maths"].mean(), "Architecture": df["architecture"].mean(),
            "Système": df["systeme"].mean(), "Prog S2": df["prog2"].mean(),
            "BDD": df["bdd"].mean(), "Réseaux": df["reseaux"].mean(),
            "Génie Log.": df["genie_logiciel"].mean(), "Stats": df["stats"].mean(),
        }
        mat_df = pd.DataFrame({"Matière": list(matieres.keys()), "Moyenne": list(matieres.values())})
        mat_df = mat_df.sort_values("Moyenne", ascending=False)
        cols = st.columns(5)
        for i, (_, row) in enumerate(mat_df.iterrows()):
            color = "#22c55e" if row["Moyenne"] >= 12 else "#f59e0b" if row["Moyenne"] >= 10 else "#f87171"
            with cols[i % 5]:
                st.markdown(f"""
                <div style="background:#0f0f22;border:3px solid #1e1e40;border-radius:10px;
                            padding:0.9rem;text-align:center;margin-bottom:0.5rem;
                            box-shadow:0 4px 15px rgba(0,0,0,0.25);">
                    <div style="font-family:'Space Mono',monospace;font-size:0.65rem;
                                color:#6060a0;text-transform:uppercase;margin-bottom:0.3rem;">
                        {row['Matière']}
                    </div>
                    <div style="font-size:1.4rem;font-weight:800;color:{color}">
                        {row['Moyenne']:.1f}
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # Tableau complet
        st.markdown('<div class="section-title">📋 Données complètes</div>', unsafe_allow_html=True)
        st.dataframe(
            df.drop(columns=["id"]),
            use_container_width=True,
            hide_index=True,
            column_config={
                "matricule": "Matricule",
                "name": "Nom", "prenom": "Prénom", "age": "Âge",
                "prog1": "Prog S1", "structures": "Structures", "maths": "Maths",
                "architecture": "Architecture", "systeme": "Système", "moyenne_s1": "Moy. S1",
                "prog2": "Prog S2", "bdd": "BDD", "reseaux": "Réseaux",
                "genie_logiciel": "Génie Log.", "stats": "Stats", "moyenne_s2": "Moy. S2",
                "moyenne_generale": st.column_config.NumberColumn("Moy. Générale", format="%.2f"),
            }
        )

        # Suppression
        with st.expander("🗑️ Supprimer un étudiant"):
            options = {f"{row['prenom']} {row['name']} — {row['matricule']} (id={row['id']})": row['id']
                       for _, row in df.iterrows()}
            choix = st.selectbox("Choisir un étudiant", list(options.keys()))
            if st.button("Supprimer", type="secondary"):
                delete_student(options[choix])
                st.cache_data.clear()
                st.success("Supprimé.")
                st.rerun()

# ============================================================
# TAB 2 — ANALYSE DÉTAILLÉE
# ============================================================
with tab_analyse:
    if df.empty:
        st.info("Aucune donnée disponible.")
    else:
        st.markdown('<div class="section-title">🔍 Profil individuel</div>', unsafe_allow_html=True)
        student_options = {f"{r['prenom']} {r['name']} ({r['matricule']})": i for i, r in df.iterrows()}
        chosen = st.selectbox("Sélectionner un étudiant", list(student_options.keys()))
        s = df.iloc[student_options[chosen]]

        # Profil card
        badge_txt = "✅ ADMIS" if s["moyenne_generale"] >= 10 else "❌ AJOURNÉ"
        badge_col = "#4ade80" if s["moyenne_generale"] >= 10 else "#f87171"
        st.markdown(f"""
        <div style="background:#0f0f22;border:3px solid #2a1a5a;border-radius:16px;
                    padding:1.5rem 2rem;margin-bottom:1.5rem;
                    box-shadow:0 8px 30px rgba(120,60,220,0.15);">
            <div style="display:flex;align-items:center;gap:1.5rem;flex-wrap:wrap;">
                <div style="font-size:3rem">🎓</div>
                <div style="flex:1">
                    <div style="font-family:'Syne',sans-serif;font-weight:800;font-size:1.4rem;color:#e8e8f0;">
                        {s['prenom']} {s['name']}
                    </div>
                    <div style="font-family:'Space Mono',monospace;font-size:0.75rem;color:#6060a0;margin-top:0.2rem;">
                        Matricule: {s['matricule']} · Âge: {int(s['age'])} ans
                    </div>
                </div>
                <div style="text-align:right;">
                    <div style="font-family:'Syne',sans-serif;font-weight:800;font-size:2rem;color:#a855f7;">
                        {s['moyenne_generale']:.2f}/20
                    </div>
                    <div style="font-family:'Space Mono',monospace;font-size:0.8rem;color:{badge_col};">
                        {badge_txt}
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Notes par matière
        notes_s1 = {
            "Programmation": s["prog1"], "Structures": s["structures"],
            "Maths": s["maths"], "Architecture": s["architecture"], "Système": s["systeme"]
        }
        notes_s2 = {
            "Prog Avancée": s["prog2"], "BDD": s["bdd"],
            "Réseaux": s["reseaux"], "Génie Logiciel": s["genie_logiciel"], "Stats": s["stats"]
        }

        c1, c2 = st.columns(2)
        for col, notes, sem, moy in [
            (c1, notes_s1, "Semestre 1", s["moyenne_s1"]),
            (c2, notes_s2, "Semestre 2", s["moyenne_s2"])
        ]:
            with col:
                st.markdown(f'<div class="section-title">📘 {sem} — Moy: {moy:.2f}</div>', unsafe_allow_html=True)
                for mat, note in notes.items():
                    color = "#22c55e" if note >= 12 else "#f59e0b" if note >= 10 else "#f87171"
                    pct = (note / 20) * 100
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:0.8rem;margin-bottom:0.6rem;">
                        <div style="width:110px;font-size:0.8rem;color:#a0a0c8;">{mat}</div>
                        <div style="flex:1;height:8px;background:#1e1e40;border-radius:4px;">
                            <div style="width:{pct:.0f}%;height:8px;background:{color};border-radius:4px;
                                        transition:width 0.5s ease;"></div>
                        </div>
                        <div style="font-family:'Space Mono',monospace;font-weight:700;
                                    font-size:0.9rem;color:{color};width:2.5rem;text-align:right;">
                            {note:.1f}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

        # Comparaison avec la moyenne de la filière
        st.markdown('<div class="section-title">📊 Comparaison avec la filière</div>', unsafe_allow_html=True)
        comp_data = pd.DataFrame({
            "Matière": list(notes_s1.keys()) + list(notes_s2.keys()),
            "Étudiant": list(notes_s1.values()) + list(notes_s2.values()),
            "Filière": [df[c].mean() for c in
                ["prog1","structures","maths","architecture","systeme",
                 "prog2","bdd","reseaux","genie_logiciel","stats"]]
        }).set_index("Matière")
        st.bar_chart(comp_data)

        # Distribution des moyennes générales
        st.markdown('<div class="section-title">📉 Distribution des moyennes générales</div>', unsafe_allow_html=True)
        hist_data = pd.cut(df["moyenne_generale"],
                           bins=[0,5,8,10,12,14,16,20],
                           labels=["0-5","5-8","8-10","10-12","12-14","14-16","16-20"])
        hist_df = hist_data.value_counts().sort_index().rename_axis("Tranche").reset_index(name="Effectif")
        st.bar_chart(hist_df.set_index("Tranche"), color="#06b6d4")

# ============================================================
# TAB 3 — RÉGRESSION & STATISTIQUES
# ============================================================
with tab_regression:
    if df.empty or len(df) < 2:
        st.info("Minimum 2 étudiants nécessaires pour les analyses statistiques.")
    else:
        st.markdown('<div class="section-title">📈 Régression linéaire</div>', unsafe_allow_html=True)

        num_cols = ["prog1","structures","maths","architecture","systeme",
                    "prog2","bdd","reseaux","genie_logiciel","stats",
                    "moyenne_s1","moyenne_s2","age"]
        col_labels = {
            "prog1":"Prog S1","structures":"Structures","maths":"Maths",
            "architecture":"Architecture","systeme":"Système","prog2":"Prog S2",
            "bdd":"BDD","reseaux":"Réseaux","genie_logiciel":"Génie Log.",
            "stats":"Stats","moyenne_s1":"Moy. S1","moyenne_s2":"Moy. S2","age":"Âge"
        }
        col_r1, col_r2 = st.columns(2)
        with col_r1:
            x_var = st.selectbox("Variable X (prédicteur)", num_cols,
                                 format_func=lambda c: col_labels[c], index=11)
        with col_r2:
            y_var = st.selectbox("Variable Y (cible)", ["moyenne_generale"] + num_cols,
                                 format_func=lambda c: col_labels.get(c, "Moy. Générale"))

        x = df[x_var].values
        y = df[y_var].values

        # Régression linéaire manuelle
        n = len(x)
        x_mean, y_mean = x.mean(), y.mean()
        cov   = np.sum((x - x_mean) * (y - y_mean))
        var_x = np.sum((x - x_mean) ** 2)
        b1    = cov / var_x if var_x != 0 else 0
        b0    = y_mean - b1 * x_mean
        y_pred = b0 + b1 * x

        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - y_mean) ** 2)
        r2     = 1 - ss_res / ss_tot if ss_tot != 0 else 0
        r      = np.corrcoef(x, y)[0, 1]

        # Résultats
        mc1, mc2, mc3 = st.columns(3)
        for col, label, val, sub in [
            (mc1, "R² (Coeff. détermination)", f"{r2:.4f}", f"{r2*100:.1f}% variance expliquée"),
            (mc2, "Corrélation r", f"{r:.4f}", "Pearson"),
            (mc3, "Équation", f"y = {b1:.3f}x + {b0:.3f}", f"{col_labels.get(y_var,'Y')} = f({col_labels[x_var]})"),
        ]:
            with col:
                st.markdown(f"""
                <div class="metric-card purple" style="margin-bottom:1rem;">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value" style="font-size:1.5rem;">{val}</div>
                    <div class="metric-sub">{sub}</div>
                </div>
                """, unsafe_allow_html=True)

        # Interprétation
        interp_r = ("forte positive" if r > 0.7 else "modérée positive" if r > 0.3
                    else "faible positive" if r > 0 else "forte négative" if r < -0.7
                    else "modérée négative" if r < -0.3 else "faible négative")
        st.markdown(f"""
        <div style="background:#0f0f22;border:3px solid #2a1a5a;border-radius:12px;
                    padding:1.2rem 1.5rem;margin:1rem 0;font-size:0.9rem;color:#a0a0c8;">
            📌 <strong style="color:#a855f7;">Interprétation :</strong>
            La corrélation entre <em>{col_labels[x_var]}</em> et <em>{col_labels.get(y_var,'Moy. Générale')}</em>
            est <strong style="color:#e8e8f0;">{interp_r}</strong> (r = {r:.3f}).
            Le modèle explique <strong style="color:#e8e8f0;">{r2*100:.1f}%</strong> de la variance de Y.
            Pour chaque point gagné en {col_labels[x_var]}, {col_labels.get(y_var,'Moy. Générale')}
            augmente de <strong style="color:#e8e8f0;">{b1:.3f} point(s)</strong>.
        </div>
        """, unsafe_allow_html=True)

        # Nuage de points avec droite de régression
        scatter_df = pd.DataFrame({
            col_labels[x_var]: x,
            col_labels.get(y_var, "Moy. Générale"): y,
            "Régression": y_pred
        })
        st.line_chart(scatter_df.set_index(col_labels[x_var])["Régression"])
        st.scatter_chart(scatter_df, x=col_labels[x_var], y=col_labels.get(y_var, "Moy. Générale"),
                         color="#7c3aed")

        # Statistiques descriptives
        st.markdown('<div class="section-title">📊 Statistiques descriptives</div>', unsafe_allow_html=True)
        stat_cols = ["prog1","structures","maths","architecture","systeme",
                     "prog2","bdd","reseaux","genie_logiciel","stats",
                     "moyenne_s1","moyenne_s2","moyenne_generale"]
        stats_df = df[stat_cols].describe().round(2)
        stats_df.index = ["Effectif","Moyenne","Écart-type","Min","Q1","Médiane","Q3","Max"]
        stats_df.columns = [col_labels.get(c, c) for c in stat_cols]
        st.dataframe(stats_df, use_container_width=True)

        # Matrice de corrélation
        st.markdown('<div class="section-title">🔗 Matrice de corrélation</div>', unsafe_allow_html=True)
        corr_matrix = df[stat_cols].corr().round(3)
        corr_matrix.columns = [col_labels.get(c, c) for c in stat_cols]
        corr_matrix.index   = [col_labels.get(c, c) for c in stat_cols]
        st.dataframe(
            corr_matrix.style.background_gradient(cmap="RdYlGn", vmin=-1, vmax=1),
            use_container_width=True
        )

        # Top/Flop matières
        st.markdown('<div class="section-title">🏆 Points forts & faiblesses (filière)</div>', unsafe_allow_html=True)
        mat_means = {col_labels[c]: df[c].mean() for c in
                     ["prog1","structures","maths","architecture","systeme",
                      "prog2","bdd","reseaux","genie_logiciel","stats"]}
        sorted_mat = sorted(mat_means.items(), key=lambda x: x[1], reverse=True)

        tf1, tf2 = st.columns(2)
        with tf1:
            st.markdown("**🟢 Top 3 — meilleures matières**")
            for mat, moy in sorted_mat[:3]:
                st.markdown(f"""
                <div style="background:#052e16;border:2px solid #166534;border-radius:8px;
                            padding:0.7rem 1rem;margin-bottom:0.4rem;display:flex;
                            justify-content:space-between;align-items:center;">
                    <span style="color:#4ade80;font-weight:600;">{mat}</span>
                    <span style="font-family:'Space Mono',monospace;color:#4ade80;font-weight:700;">{moy:.2f}</span>
                </div>
                """, unsafe_allow_html=True)
        with tf2:
            st.markdown("**🔴 Flop 3 — matières à améliorer**")
            for mat, moy in sorted_mat[-3:]:
                st.markdown(f"""
                <div style="background:#2d0a0a;border:2px solid #7f1d1d;border-radius:8px;
                            padding:0.7rem 1rem;margin-bottom:0.4rem;display:flex;
                            justify-content:space-between;align-items:center;">
                    <span style="color:#f87171;font-weight:600;">{mat}</span>
                    <span style="font-family:'Space Mono',monospace;color:#f87171;font-weight:700;">{moy:.2f}</span>
                </div>
                """, unsafe_allow_html=True)

# ============================================================
# TAB 4 — À PROPOS
# ============================================================
with tab_about:
    st.markdown("""
    <div class="about-card">
        <h3>🎓 Qu'est-ce qu'EduStat ?</h3>
        <p>
            <strong style="color:#e8e8f0;">EduStat</strong> est une application de gestion et d'analyse
            des performances académiques conçue spécifiquement pour la filière
            <strong style="color:#a855f7;">L2 Informatique</strong>.
            Elle centralise toutes les données de notation des étudiants sur les deux semestres
            et fournit des outils statistiques avancés pour aider les enseignants et responsables
            pédagogiques à prendre des décisions éclairées.
        </p>
    </div>

    <div class="about-card" style="margin-top:1rem;">
        <h3>⚙️ Fonctionnalités principales</h3>
        <ul>
            <li><strong style="color:#e8e8f0;">Gestion des étudiants</strong> — Ajout, suppression et consultation
                des dossiers avec matricule, nom, prénom, âge et toutes les notes.</li>
            <li><strong style="color:#e8e8f0;">Calcul automatique des moyennes</strong> — Semestre 1, Semestre 2
                et moyenne générale calculées automatiquement à l'enregistrement.</li>
            <li><strong style="color:#e8e8f0;">Classement dynamique</strong> — Tableau de classement général
                avec médailles, barres de progression et statut Admis/Ajourné.</li>
            <li><strong style="color:#e8e8f0;">Visualisations graphiques</strong> — Graphiques de comparaison
                S1 vs S2, moyennes par matière, distribution des résultats.</li>
            <li><strong style="color:#e8e8f0;">Profil individuel</strong> — Vue détaillée par étudiant avec
                comparaison à la moyenne de la filière.</li>
            <li><strong style="color:#e8e8f0;">Régression linéaire</strong> — Analyse de corrélation entre
                n'importe quelles deux variables avec interprétation automatique.</li>
            <li><strong style="color:#e8e8f0;">Statistiques descriptives</strong> — Moyenne, écart-type,
                médiane, quartiles pour toutes les matières.</li>
            <li><strong style="color:#e8e8f0;">Matrice de corrélation</strong> — Visualisation des liens
                entre toutes les matières et moyennes.</li>
            <li><strong style="color:#e8e8f0;">Authentification sécurisée</strong> — Accès protégé par
                login administrateur avec hachage SHA-256 des mots de passe.</li>
        </ul>
    </div>

    <div class="about-card" style="margin-top:1rem;">
        <h3>📚 Matières couvertes</h3>
        <p><strong style="color:#3b82f6;">Semestre 1 :</strong>
            Programmation, Structures de données, Mathématiques, Architecture des ordinateurs, Système d'exploitation.
        </p>
        <p><strong style="color:#06b6d4;">Semestre 2 :</strong>
            Programmation avancée, Bases de données, Réseaux informatiques, Génie logiciel, Statistiques.
        </p>
    </div>

    <div class="about-card" style="margin-top:1rem;">
        <h3>🔐 Sécurité & Accès</h3>
        <p>
            L'application est protégée par un système de login administrateur.
            Les mots de passe sont stockés sous forme de hash SHA-256 dans la base de données.
            Seuls les administrateurs authentifiés peuvent ajouter, modifier ou supprimer des données.
            Le compte par défaut est <strong style="color:#a855f7;">admin / admin123</strong> —
            il est fortement recommandé de le changer dès la première connexion via le panneau latéral.
        </p>
    </div>

    <div class="about-card" style="margin-top:1rem;">
        <h3>🛠️ Stack technique</h3>
        <ul>
            <li><strong style="color:#e8e8f0;">Frontend :</strong> Streamlit (Python)</li>
            <li><strong style="color:#e8e8f0;">Backend/BDD :</strong> SQLite (local) ou PostgreSQL (production)</li>
            <li><strong style="color:#e8e8f0;">Analyse :</strong> Pandas, NumPy</li>
            <li><strong style="color:#e8e8f0;">Hébergement :</strong> Railway.app</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ================= FOOTER =================
st.markdown("""
<div style="text-align:center;padding:2rem 0;margin-top:2rem;
            border-top:3px solid #1e1e40;font-family:'Space Mono',monospace;
            font-size:0.7rem;color:#2a2a4a;letter-spacing:0.1em;">
    EDUSTAT · L2 INFORMATIQUE · BUILT WITH STREAMLIT · 2024-2025
</div>
""", unsafe_allow_html=True)
