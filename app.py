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

# ─────────────────────────────────────────────────────────────
# CSS GLOBAL
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;700;800&display=swap');

*, html, body, [class*="css"] { font-family: 'Syne', sans-serif; box-sizing: border-box; }

/* ── FOND ── */
.stApp {
    background-color: #06061a;
    background-image:
        radial-gradient(ellipse at 15% 10%,  rgba(139,92,246,.22)  0%, transparent 45%),
        radial-gradient(ellipse at 85% 90%,  rgba(59,130,246,.16)  0%, transparent 45%),
        radial-gradient(ellipse at 50% 50%,  rgba(6,182,212,.06)   0%, transparent 70%),
        url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' stroke='rgba(255,255,255,0.025)' stroke-width='1'%3E%3Cpath d='M60 0L0 0 0 60'/%3E%3C/g%3E%3C/svg%3E");
    color: #e2e2f0;
    min-height: 100vh;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a0a22 0%, #0d0d20 100%) !important;
    border-right: 3px solid #1e1560 !important;
    box-shadow: 6px 0 40px rgba(100,60,240,.14) !important;
}
[data-testid="stSidebar"] * { color: #c4c4e0 !important; }
[data-testid="stSidebar"] .stTextInput input,
[data-testid="stSidebar"] .stNumberInput input {
    background: #10102a !important;
    border: 2px solid #252560 !important;
    color: #e2e2f0 !important;
    border-radius: 10px !important;
    transition: border-color .25s, box-shadow .25s, transform .15s !important;
    padding: .5rem .8rem !important;
}
[data-testid="stSidebar"] .stTextInput input:focus,
[data-testid="stSidebar"] .stNumberInput input:focus {
    border-color: #7c3aed !important;
    box-shadow: 0 0 0 3px rgba(124,58,237,.28) !important;
    transform: scale(1.015) !important;
}

/* ── HEADER ── */
.edu-header {
    background: linear-gradient(135deg,#0c0c20 0%,#140824 50%,#081424 100%);
    border: 3px solid #1e1560;
    border-radius: 22px;
    padding: 2.8rem 2.5rem 2.4rem;
    margin-bottom: 2rem;
    position: relative; overflow: hidden;
    box-shadow: 0 12px 50px rgba(100,60,240,.18), inset 0 1px 0 rgba(255,255,255,.06);
}
.edu-header::before {
    content:''; position:absolute; inset:0;
    background: radial-gradient(ellipse at 25% 50%,rgba(139,92,246,.2) 0%,transparent 60%),
                radial-gradient(ellipse at 75% 50%,rgba(59,130,246,.14) 0%,transparent 60%);
    pointer-events:none;
}
.edu-header h1 {
    font-weight:800; font-size:3rem;
    background:linear-gradient(100deg,#c084fc,#60a5fa,#22d3ee);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    margin:0 0 .4rem; line-height:1.05;
}
.edu-header .sub {
    font-family:'Space Mono',monospace; font-size:.8rem;
    color:#5050a0; letter-spacing:.12em;
}
.edu-header .stats-pill {
    display:inline-flex; align-items:center; gap:.4rem;
    background:rgba(124,58,237,.15); border:1.5px solid rgba(124,58,237,.35);
    border-radius:999px; padding:.25rem .9rem;
    font-family:'Space Mono',monospace; font-size:.72rem; color:#a78bfa;
    margin-top:.8rem; margin-right:.4rem;
}

/* ── METRIC CARDS ── */
.metric-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:1.2rem; margin-bottom:2rem; }
.metric-card {
    background:linear-gradient(145deg,#0e0e26,#111128);
    border: 3px solid #1a1a40;
    border-radius:18px; padding:1.6rem 1.8rem;
    position:relative; overflow:hidden;
    transition:border-color .3s, transform .25s, box-shadow .3s;
    box-shadow:0 6px 28px rgba(0,0,0,.35);
}
.metric-card::after {
    content:''; position:absolute; top:0; left:0; right:0;
    height:3px; border-radius:18px 18px 0 0;
}
.metric-card.purple::after { background:linear-gradient(90deg,#a855f7,#6d28d9); }
.metric-card.blue::after   { background:linear-gradient(90deg,#3b82f6,#1d4ed8); }
.metric-card.cyan::after   { background:linear-gradient(90deg,#06b6d4,#0891b2); }
.metric-card.green::after  { background:linear-gradient(90deg,#22c55e,#15803d); }
.metric-card:hover { border-color:#3a2a80; transform:translateY(-4px); box-shadow:0 14px 40px rgba(100,60,240,.22); }
.metric-label { font-family:'Space Mono',monospace; font-size:.68rem; color:#5858a0; letter-spacing:.12em; text-transform:uppercase; margin-bottom:.55rem; }
.metric-value { font-weight:800; font-size:2.3rem; color:#e8e8f8; line-height:1; }
.metric-sub   { font-size:.76rem; color:#4848a0; margin-top:.35rem; font-family:'Space Mono',monospace; }

/* ── SECTION TITLES ── */
.section-title {
    font-weight:700; font-size:1.05rem; color:#a855f7; letter-spacing:.06em;
    text-transform:uppercase; margin:2.2rem 0 1rem;
    padding-bottom:.55rem; border-bottom:3px solid #1e1560;
}

/* ── INTERPRET BOX ── */
.interpret-box {
    background:linear-gradient(135deg,#0d0d28,#0f0f22);
    border:2px solid #2a1a5a; border-left:4px solid #a855f7;
    border-radius:12px; padding:1.1rem 1.5rem;
    margin:1rem 0 1.5rem; font-size:.88rem; line-height:1.75;
    color:#9090c0;
}
.interpret-box strong { color:#e2e2f0; }

/* ── RANK ROW ── */
.rank-row {
    display:flex; align-items:center; padding:.9rem 1.3rem;
    border-radius:12px; margin-bottom:.5rem;
    background:linear-gradient(135deg,#0e0e26,#111128);
    border:3px solid #1a1a40;
    transition:border-color .2s, transform .2s, box-shadow .2s;
}
.rank-row:hover { border-color:#3a2a80; transform:translateX(5px); box-shadow:0 6px 24px rgba(100,60,240,.18); }
.rank-pos { font-family:'Space Mono',monospace; font-weight:700; font-size:1.1rem; width:2.8rem; color:#5050a0; }
.rank-pos.gold   { color:#f59e0b; }
.rank-pos.silver { color:#94a3b8; }
.rank-pos.bronze { color:#b45309; }
.rank-name { flex:1; font-weight:600; font-size:.95rem; color:#e2e2f0; }
.rank-mat  { font-family:'Space Mono',monospace; font-size:.68rem; color:#4848a0; margin-left:.5rem; }
.rank-score{ font-family:'Space Mono',monospace; font-weight:700; font-size:1.05rem; color:#a855f7; }
.rank-bar-wrap { width:110px; height:6px; background:#1a1a3a; border-radius:3px; margin:0 1.1rem; }
.rank-bar { height:6px; border-radius:3px; background:linear-gradient(90deg,#7c3aed,#06b6d4); }

/* ── BADGE ── */
.badge { display:inline-block; padding:.22rem .75rem; border-radius:999px; font-family:'Space Mono',monospace; font-size:.68rem; font-weight:700; letter-spacing:.05em; }
.badge-pass { background:#052e16; color:#4ade80; border:2px solid #166534; }
.badge-fail { background:#2d0a0a; color:#f87171; border:2px solid #7f1d1d; }

/* ── SUBJECT MINI CARD ── */
.sub-card { background:linear-gradient(145deg,#0e0e26,#111128); border:3px solid #1a1a40; border-radius:12px; padding:1rem; text-align:center; margin-bottom:.6rem; transition:border-color .2s, transform .2s; }
.sub-card:hover { border-color:#3a2a80; transform:scale(1.03); }
.sub-card-label { font-family:'Space Mono',monospace; font-size:.62rem; color:#5050a0; text-transform:uppercase; margin-bottom:.3rem; }
.sub-card-val { font-size:1.5rem; font-weight:800; }

/* ── ABOUT ── */
.about-card { background:linear-gradient(145deg,#0e0e26,#111128); border:3px solid #1e1560; border-radius:18px; padding:2rem 2.2rem; margin-top:1.2rem; box-shadow:0 6px 28px rgba(0,0,0,.3); line-height:1.85; }
.about-card h3 { font-weight:800; font-size:1.05rem; color:#a855f7; text-transform:uppercase; letter-spacing:.08em; margin-bottom:.7rem; }
.about-card p, .about-card li { font-size:.91rem; color:#8888b8; }
.about-card ul { padding-left:1.3rem; margin-top:.4rem; }
.about-card li { margin-bottom:.4rem; }

/* ── DATAFRAME ── */
[data-testid="stDataFrame"] { border:3px solid #1a1a40 !important; border-radius:14px !important; box-shadow:0 6px 28px rgba(0,0,0,.3) !important; overflow:hidden !important; }

/* ── BUTTONS ── */
.stButton > button {
    background:linear-gradient(135deg,#7c3aed,#4f46e5) !important;
    color:#fff !important; border:none !important; border-radius:12px !important;
    font-family:'Syne',sans-serif !important; font-weight:700 !important;
    font-size:.9rem !important; padding:.65rem 1.5rem !important; width:100% !important;
    transition:opacity .2s, transform .15s, box-shadow .2s !important;
    box-shadow:0 5px 20px rgba(124,58,237,.35) !important;
}
.stButton > button:hover { opacity:.87 !important; transform:translateY(-2px) scale(1.012) !important; box-shadow:0 10px 30px rgba(124,58,237,.5) !important; }
.stButton > button:active { transform:scale(.97) !important; }

/* ── ALERTS ── */
.stSuccess { background:#051a05 !important; border-left:4px solid #22c55e !important; border-radius:10px !important; }
.stWarning { background:#1a140a !important; border-left:4px solid #f59e0b !important; border-radius:10px !important; }
.stError   { background:#1a0505 !important; border-left:4px solid #ef4444 !important; border-radius:10px !important; }

/* ── TABS ── */
[data-testid="stTabs"] [role="tablist"] { border-bottom:3px solid #1a1a40 !important; }
[data-testid="stTabs"] [role="tab"] { font-family:'Syne',sans-serif !important; font-weight:700 !important; color:#505090 !important; transition:color .2s !important; font-size:.92rem !important; }
[data-testid="stTabs"] [role="tab"][aria-selected="true"] { color:#a855f7 !important; border-bottom:3px solid #a855f7 !important; }

/* ── SELECT / EXPANDER ── */
[data-testid="stSelectbox"] > div > div { background:#10102a !important; border:2px solid #252560 !important; border-radius:10px !important; transition:border-color .25s !important; }
[data-testid="stSelectbox"] > div > div:focus-within { border-color:#7c3aed !important; box-shadow:0 0 0 3px rgba(124,58,237,.2) !important; }
[data-testid="stExpander"] { border:3px solid #1a1a40 !important; border-radius:14px !important; background:#0e0e26 !important; }

/* ── CHARTS WRAPPER ── */
[data-testid="stVegaLiteChart"] { background:#0e0e26 !important; border-radius:14px !important; border:3px solid #1a1a40 !important; padding:.8rem !important; box-shadow:0 6px 28px rgba(0,0,0,.25) !important; }

/* ── NOTE BARS ── */
.note-bar-row { display:flex; align-items:center; gap:.8rem; margin-bottom:.65rem; }
.note-bar-label { width:130px; font-size:.8rem; color:#8888b8; }
.note-bar-track { flex:1; height:9px; background:#181838; border-radius:5px; }
.note-bar-fill  { height:9px; border-radius:5px; transition:width .5s ease; }
.note-bar-val   { font-family:'Space Mono',monospace; font-weight:700; font-size:.88rem; width:2.6rem; text-align:right; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# DATABASE — robuste SQLite + PostgreSQL
# ─────────────────────────────────────────────────────────────
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./edustat.db")

@st.cache_resource
def get_engine():
    return create_engine(DATABASE_URL, pool_pre_ping=True)

engine = get_engine()

MATIERE_COLS = ["prog1","structures","maths","architecture","systeme",
                "prog2","bdd","reseaux","genie_logiciel","stats"]
COL_LABELS = {
    "prog1":"Prog S1","structures":"Structures","maths":"Maths",
    "architecture":"Architecture","systeme":"Système","prog2":"Prog S2",
    "bdd":"BDD","reseaux":"Réseaux","genie_logiciel":"Génie Log.",
    "stats":"Stats","moyenne_s1":"Moy. S1","moyenne_s2":"Moy. S2",
    "moyenne_generale":"Moy. Générale","age":"Âge"
}

def create_table():
    is_pg = "postgresql" in DATABASE_URL
    pk_def = "SERIAL PRIMARY KEY" if is_pg else "INTEGER PRIMARY KEY AUTOINCREMENT"
    with engine.connect() as conn:
        conn.execute(text(f"""
            CREATE TABLE IF NOT EXISTS students (
                id {pk_def},
                matricule TEXT DEFAULT '',
                name      TEXT DEFAULT '',
                prenom    TEXT DEFAULT '',
                age       INTEGER DEFAULT 20,
                prog1          REAL DEFAULT 0,
                structures     REAL DEFAULT 0,
                maths          REAL DEFAULT 0,
                architecture   REAL DEFAULT 0,
                systeme        REAL DEFAULT 0,
                moyenne_s1     REAL DEFAULT 0,
                prog2          REAL DEFAULT 0,
                bdd            REAL DEFAULT 0,
                reseaux        REAL DEFAULT 0,
                genie_logiciel REAL DEFAULT 0,
                stats          REAL DEFAULT 0,
                moyenne_s2     REAL DEFAULT 0,
                moyenne_generale REAL DEFAULT 0
            )
        """))
        # Migration douce : ajoute les colonnes manquantes si ancienne DB
        if is_pg:
            for col in ["matricule TEXT DEFAULT ''", "prenom TEXT DEFAULT ''"]:
                try:
                    conn.execute(text(f"ALTER TABLE students ADD COLUMN IF NOT EXISTS {col}"))
                except Exception:
                    pass
        conn.commit()

create_table()

# ─────────────────────────────────────────────────────────────
# DATA HELPERS
# ─────────────────────────────────────────────────────────────
@st.cache_data(ttl=4)
def load_data() -> pd.DataFrame:
    try:
        df = pd.read_sql("SELECT * FROM students ORDER BY id", engine)
    except Exception as e:
        st.error(f"Erreur base de données : {e}")
        return pd.DataFrame()
    # Colonnes de compatibilité
    for c in ["matricule","prenom","name"]:
        if c not in df.columns:
            df[c] = ""
    for c in MATIERE_COLS + ["moyenne_s1","moyenne_s2","moyenne_generale"]:
        if c not in df.columns:
            df[c] = 0.0
    if "age" not in df.columns:
        df["age"] = 20
    return df

def save_student(row: dict):
    cols = ", ".join(row.keys())
    vals = ", ".join([f":{k}" for k in row.keys()])
    with engine.connect() as conn:
        conn.execute(text(f"INSERT INTO students ({cols}) VALUES ({vals})"), row)
        conn.commit()
    st.cache_data.clear()

def delete_student(sid: int):
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM students WHERE id=:id"), {"id": sid})
        conn.commit()
    st.cache_data.clear()

def calc_moyennes(s1_notes, s2_notes):
    m1 = round(float(np.mean(s1_notes)), 2)
    m2 = round(float(np.mean(s2_notes)), 2)
    mg = round(float(np.mean([m1, m2])), 2)
    return m1, m2, mg

# ─────────────────────────────────────────────────────────────
# SIDEBAR — FORMULAIRE
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:.8rem 0 1.4rem;">
        <div style="font-size:2.2rem;">🎓</div>
        <div style="font-weight:800;font-size:1.15rem;
                    background:linear-gradient(90deg,#c084fc,#60a5fa);
                    -webkit-background-clip:text;-webkit-text-fill-color:transparent;">EduStat</div>
        <div style="font-family:'Space Mono',monospace;font-size:.62rem;color:#303080;margin-top:.2rem;">
            PANNEAU DE GESTION
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### ➕ Ajouter un étudiant")
    matricule = st.text_input("Matricule *",  placeholder="Ex: 22G0001")
    prenom    = st.text_input("Prénom *",     placeholder="Ex: Jean")
    name      = st.text_input("Nom *",        placeholder="Ex: MBARGA")
    age       = st.number_input("Âge", 15, 45, 20)

    st.markdown("**— Semestre 1 —**")
    prog1        = st.number_input("Programmation",  0.0, 20.0, 0.0, .5, key="p1")
    structures   = st.number_input("Structures",     0.0, 20.0, 0.0, .5, key="st")
    maths        = st.number_input("Maths",          0.0, 20.0, 0.0, .5, key="ma")
    architecture = st.number_input("Architecture",   0.0, 20.0, 0.0, .5, key="ar")
    systeme      = st.number_input("Système",        0.0, 20.0, 0.0, .5, key="sy")

    st.markdown("**— Semestre 2 —**")
    prog2          = st.number_input("Prog. avancée",    0.0, 20.0, 0.0, .5, key="p2")
    bdd            = st.number_input("Base de données",  0.0, 20.0, 0.0, .5, key="bd")
    reseaux        = st.number_input("Réseaux",          0.0, 20.0, 0.0, .5, key="re")
    genie_logiciel = st.number_input("Génie logiciel",   0.0, 20.0, 0.0, .5, key="gl")
    stats_note     = st.number_input("Statistiques",     0.0, 20.0, 0.0, .5, key="sa")

    st.markdown("---")
    if st.button("✅ Enregistrer l'étudiant"):
        errors = []
        if not matricule.strip(): errors.append("Matricule manquant")
        if not prenom.strip():    errors.append("Prénom manquant")
        if not name.strip():      errors.append("Nom manquant")
        if errors:
            for e in errors: st.error(e)
        else:
            s1 = [prog1, structures, maths, architecture, systeme]
            s2 = [prog2, bdd, reseaux, genie_logiciel, stats_note]
            m1, m2, mg = calc_moyennes(s1, s2)
            save_student({
                "matricule": matricule.strip(),
                "name":      name.strip().upper(),
                "prenom":    prenom.strip(),
                "age":       int(age),
                "prog1": prog1, "structures": structures, "maths": maths,
                "architecture": architecture, "systeme": systeme, "moyenne_s1": m1,
                "prog2": prog2, "bdd": bdd, "reseaux": reseaux,
                "genie_logiciel": genie_logiciel, "stats": stats_note,
                "moyenne_s2": m2, "moyenne_generale": mg,
            })
            status = "✅ ADMIS" if mg >= 10 else "❌ AJOURNÉ"
            st.success(f"{prenom} {name} enregistré·e ! Moy. : {mg}/20 — {status}")
            st.rerun()

# ─────────────────────────────────────────────────────────────
# CHARGEMENT DES DONNÉES
# ─────────────────────────────────────────────────────────────
df = load_data()
n_students = len(df)
n_admis    = int((df["moyenne_generale"] >= 10).sum()) if n_students else 0
taux_str   = f"{n_admis/n_students*100:.0f}%" if n_students else "—"

# ─────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="edu-header">
    <h1>🎓 EduStat</h1>
    <p class="sub">L2 INFORMATIQUE · ANALYSE DES PERFORMANCES ACADÉMIQUES S1 & S2</p>
    <div>
        <span class="stats-pill">📋 {n_students} étudiants</span>
        <span class="stats-pill">✅ {n_admis} admis</span>
        <span class="stats-pill">📈 Réussite : {taux_str}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────────────
tab_dash, tab_profil, tab_stats, tab_about = st.tabs([
    "📊  Tableau de bord",
    "🔍  Profil étudiant",
    "📈  Statistiques & Régression",
    "ℹ️  À propos",
])

# ═══════════════════════════════════════════════════════════════
# TAB 1 — TABLEAU DE BORD
# ═══════════════════════════════════════════════════════════════
with tab_dash:
    if df.empty:
        st.markdown("""
        <div style="text-align:center;padding:5rem 0;color:#2a2a6a;">
            <div style="font-size:5rem;">📭</div>
            <div style="font-family:'Space Mono',monospace;font-size:.9rem;margin-top:1.2rem;">
                AUCUN ÉTUDIANT ENREGISTRÉ<br>
                <span style="font-size:.75rem;">Utilisez le formulaire dans la barre latérale.</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.stop()

    # KPIs
    moy_gen   = float(df["moyenne_generale"].mean())
    ecart_typ = float(df["moyenne_generale"].std()) if n_students > 1 else 0.0
    meilleur  = df.loc[df["moyenne_generale"].idxmax()]
    moy_s1    = float(df["moyenne_s1"].mean())
    moy_s2    = float(df["moyenne_s2"].mean())

    st.markdown(f"""
    <div class="metric-grid">
      <div class="metric-card purple">
        <div class="metric-label">Moyenne filière</div>
        <div class="metric-value">{moy_gen:.2f}</div>
        <div class="metric-sub">/ 20 · {n_students} étudiant(s)</div>
      </div>
      <div class="metric-card blue">
        <div class="metric-label">Meilleur score</div>
        <div class="metric-value">{meilleur['moyenne_generale']:.2f}</div>
        <div class="metric-sub">{meilleur['prenom']} {meilleur['name']}</div>
      </div>
      <div class="metric-card cyan">
        <div class="metric-label">Taux de réussite</div>
        <div class="metric-value">{n_admis/n_students*100:.1f}%</div>
        <div class="metric-sub">{n_admis} admis · {n_students-n_admis} ajourné(s)</div>
      </div>
      <div class="metric-card green">
        <div class="metric-label">Écart-type</div>
        <div class="metric-value">{ecart_typ:.2f}</div>
        <div class="metric-sub">Dispersion des notes</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Interprétation KPIs
    kpi_q = "satisfaisante" if moy_gen >= 12 else "acceptable" if moy_gen >= 10 else "insuffisante"
    disp_q = "homogène" if ecart_typ < 3 else "hétérogène" if ecart_typ < 5 else "très hétérogène"
    prog_glob = moy_s2 - moy_s1
    prog_sign = "+" if prog_glob >= 0 else ""
    st.markdown(f"""
    <div class="interpret-box">
        📌 <strong>Lecture des indicateurs :</strong> La filière affiche une moyenne de
        <strong>{moy_gen:.2f}/20</strong> ({kpi_q}). L'écart-type de <strong>{ecart_typ:.2f}</strong>
        indique un groupe <strong>{disp_q}</strong>. La progression moyenne S1→S2 est de
        <strong>{prog_sign}{prog_glob:.2f} point(s)</strong>
        ({'amélioration globale' if prog_glob >= 0 else 'régression globale à surveiller'}).
        💡 Un taux de réussite ≥ 70 % est la référence dans l'enseignement supérieur.
    </div>
    """, unsafe_allow_html=True)

    # Classement
    st.markdown('<div class="section-title">🏅 Classement général</div>', unsafe_allow_html=True)
    classement = df.sort_values("moyenne_generale", ascending=False).reset_index(drop=True)
    max_sc = float(classement["moyenne_generale"].max())
    medals = {0:("gold","🥇"), 1:("silver","🥈"), 2:("bronze","🥉")}

    for i, row in classement.iterrows():
        cls, emoji = medals.get(i, ("", f"#{i+1}"))
        pct = (float(row["moyenne_generale"]) / max_sc * 100) if max_sc > 0 else 0
        badge = '<span class="badge badge-pass">ADMIS</span>' \
                if float(row["moyenne_generale"]) >= 10 \
                else '<span class="badge badge-fail">AJOURNÉ</span>'
        st.markdown(f"""
        <div class="rank-row">
            <div class="rank-pos {cls}">{emoji if cls else f'#{i+1}'}</div>
            <div class="rank-name">
                {row['prenom']} {row['name']}
                <span class="rank-mat">{row['matricule']}</span>
            </div>
            {badge}
            <div class="rank-bar-wrap">
                <div class="rank-bar" style="width:{pct:.0f}%"></div>
            </div>
            <div class="rank-score">{float(row['moyenne_generale']):.2f}</div>
        </div>
        """, unsafe_allow_html=True)

    # Graphiques
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.markdown('<div class="section-title">📊 Moyennes générales</div>', unsafe_allow_html=True)
        cg = classement.set_index("name")["moyenne_generale"].rename("Moyenne générale")
        st.bar_chart(cg, color="#a855f7")
        st.markdown("""
        <div class="interpret-box">
            📌 Chaque barre = moyenne générale (S1+S2)/2 d'un étudiant.
            La limite de passage est à <strong>10/20</strong>.
            Les écarts visuels reflètent la <strong>dispersion du groupe</strong>.
        </div>
        """, unsafe_allow_html=True)

    with col_g2:
        st.markdown('<div class="section-title">📊 S1 vs S2 par étudiant</div>', unsafe_allow_html=True)
        cs = classement.set_index("name")[["moyenne_s1","moyenne_s2"]].rename(
            columns={"moyenne_s1":"Semestre 1","moyenne_s2":"Semestre 2"})
        st.bar_chart(cs)
        st.markdown("""
        <div class="interpret-box">
            📌 Comparez S1 (bleu) et S2 (rouge). Une barre S2 plus haute = <strong>progression</strong> ;
            plus basse = <strong>régression</strong>. Identifiez facilement les étudiants en difficulté croissante.
        </div>
        """, unsafe_allow_html=True)

    # Distribution
    st.markdown('<div class="section-title">📉 Distribution des moyennes (histogramme)</div>', unsafe_allow_html=True)
    bins   = [0, 5, 8, 10, 12, 14, 16, 20]
    labels = ["0–5","5–8","8–10","10–12","12–14","14–16","16–20"]
    hist   = pd.cut(df["moyenne_generale"], bins=bins, labels=labels, include_lowest=True)
    hist_df = hist.value_counts().sort_index().rename_axis("Tranche").reset_index(name="Effectif")
    st.bar_chart(hist_df.set_index("Tranche"), color="#06b6d4")
    mode_tranche = hist_df.loc[hist_df["Effectif"].idxmax(), "Tranche"] if not hist_df.empty else "N/A"
    st.markdown(f"""
    <div class="interpret-box">
        📌 <strong>Histogramme de distribution :</strong> montre combien d'étudiants se trouvent dans chaque
        tranche de notes. La tranche la plus peuplée est <strong>{mode_tranche}</strong>.
        Une concentration dans les tranches ≥ 10 = bonne santé académique.
        Une concentration dans 0–8 signale un problème structurel nécessitant une intervention.
    </div>
    """, unsafe_allow_html=True)

    # Matières
    st.markdown('<div class="section-title">📚 Moyennes par matière</div>', unsafe_allow_html=True)
    matieres = {COL_LABELS[c]: float(df[c].mean()) for c in MATIERE_COLS}
    mat_df   = pd.DataFrame({"Matière": list(matieres.keys()), "Moyenne": list(matieres.values())}).sort_values("Moyenne", ascending=False)
    cols5    = st.columns(5)
    for i, (_, row) in enumerate(mat_df.iterrows()):
        c = "#22c55e" if row["Moyenne"] >= 12 else "#f59e0b" if row["Moyenne"] >= 10 else "#f87171"
        with cols5[i % 5]:
            st.markdown(f"""
            <div class="sub-card">
                <div class="sub-card-label">{row['Matière']}</div>
                <div class="sub-card-val" style="color:{c}">{row['Moyenne']:.1f}</div>
            </div>
            """, unsafe_allow_html=True)

    best_mat  = mat_df.iloc[0]
    worst_mat = mat_df.iloc[-1]
    st.markdown(f"""
    <div class="interpret-box">
        📌 <span style="color:#22c55e;font-weight:700;">Vert</span> ≥ 12/20 (maîtrisé) ·
        <span style="color:#f59e0b;font-weight:700;">Jaune</span> ≥ 10 (passable) ·
        <span style="color:#f87171;font-weight:700;">Rouge</span> &lt; 10 (insuffisant).<br>
        ✅ Meilleure matière : <strong>{best_mat['Matière']}</strong> ({best_mat['Moyenne']:.2f}/20) —
        ⚠️ Matière la plus faible : <strong>{worst_mat['Matière']}</strong> ({worst_mat['Moyenne']:.2f}/20).
        Cette dernière mérite une attention pédagogique prioritaire.
    </div>
    """, unsafe_allow_html=True)

    # Tableau complet
    st.markdown('<div class="section-title">📋 Données complètes</div>', unsafe_allow_html=True)
    st.dataframe(
        df.drop(columns=["id"]),
        use_container_width=True, hide_index=True,
        column_config={
            "matricule":"Matricule","name":"Nom","prenom":"Prénom","age":"Âge",
            "prog1":"Prog S1","structures":"Structures","maths":"Maths",
            "architecture":"Architecture","systeme":"Système","moyenne_s1":"Moy. S1",
            "prog2":"Prog S2","bdd":"BDD","reseaux":"Réseaux",
            "genie_logiciel":"Génie Log.","stats":"Stats","moyenne_s2":"Moy. S2",
            "moyenne_generale": st.column_config.NumberColumn("Moy. Générale", format="%.2f"),
        }
    )

    with st.expander("🗑️ Supprimer un étudiant"):
        options = {f"{r['prenom']} {r['name']} — {r['matricule']}": int(r['id'])
                   for _, r in df.iterrows()}
        choix = st.selectbox("Étudiant à supprimer", list(options.keys()))
        if st.button("⚠️ Supprimer définitivement", type="secondary"):
            delete_student(options[choix])
            st.success("Étudiant supprimé.")
            st.rerun()

# ═══════════════════════════════════════════════════════════════
# TAB 2 — PROFIL ÉTUDIANT
# ═══════════════════════════════════════════════════════════════
with tab_profil:
    if df.empty:
        st.info("Aucun étudiant enregistré.")
    else:
        opts = {f"{r['prenom']} {r['name']} ({r['matricule']})": i for i, r in df.iterrows()}
        chosen_key = st.selectbox("Sélectionner un étudiant", list(opts.keys()), key="profil_sel")
        s = df.iloc[opts[chosen_key]]

        admis     = float(s["moyenne_generale"]) >= 10
        badge_col = "#4ade80" if admis else "#f87171"
        badge_lbl = "✅ ADMIS" if admis else "❌ AJOURNÉ"
        rang = int(df["moyenne_generale"].rank(ascending=False, method="min")[s.name])

        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#0e0e26,#111128);
                    border:3px solid #1e1560;border-radius:20px;padding:1.8rem 2.2rem;
                    margin-bottom:1.5rem;box-shadow:0 12px 40px rgba(100,60,240,.18);">
            <div style="display:flex;align-items:center;gap:1.8rem;flex-wrap:wrap;">
                <div style="font-size:3.5rem;">🎓</div>
                <div style="flex:1;">
                    <div style="font-weight:800;font-size:1.5rem;color:#e2e2f0;">
                        {s['prenom']} {s['name']}
                    </div>
                    <div style="font-family:'Space Mono',monospace;font-size:.75rem;color:#5050a0;margin-top:.3rem;">
                        Matricule : {s['matricule']} · Âge : {int(s['age'])} ans · Rang : #{rang}/{n_students}
                    </div>
                </div>
                <div style="text-align:right;">
                    <div style="font-weight:800;font-size:2.2rem;color:#a855f7;">
                        {float(s['moyenne_generale']):.2f}<span style="font-size:1rem;color:#5050a0;">/20</span>
                    </div>
                    <div style="font-family:'Space Mono',monospace;font-size:.8rem;color:{badge_col};margin-top:.2rem;">{badge_lbl}</div>
                    <div style="font-family:'Space Mono',monospace;font-size:.7rem;color:#4040a0;margin-top:.1rem;">
                        S1 : {float(s['moyenne_s1']):.2f} · S2 : {float(s['moyenne_s2']):.2f}
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        notes_s1 = {"Programmation":s["prog1"],"Structures":s["structures"],"Maths":s["maths"],"Architecture":s["architecture"],"Système":s["systeme"]}
        notes_s2 = {"Prog. Avancée":s["prog2"],"BDD":s["bdd"],"Réseaux":s["reseaux"],"Génie Logiciel":s["genie_logiciel"],"Statistiques":s["stats"]}

        c_s1, c_s2 = st.columns(2)
        for col, notes, sem, moy_val in [(c_s1, notes_s1, "Semestre 1", s["moyenne_s1"]),
                                          (c_s2, notes_s2, "Semestre 2", s["moyenne_s2"])]:
            with col:
                moy_f = float(moy_val)
                col_m = "#22c55e" if moy_f >= 12 else "#f59e0b" if moy_f >= 10 else "#f87171"
                st.markdown(f'<div class="section-title">📘 {sem} — <span style="color:{col_m}">{moy_f:.2f}/20</span></div>', unsafe_allow_html=True)
                for mat, note in notes.items():
                    nf = float(note)
                    c  = "#22c55e" if nf >= 12 else "#f59e0b" if nf >= 10 else "#f87171"
                    st.markdown(f"""
                    <div class="note-bar-row">
                        <div class="note-bar-label">{mat}</div>
                        <div class="note-bar-track">
                            <div class="note-bar-fill" style="width:{nf/20*100:.0f}%;background:{c};"></div>
                        </div>
                        <div class="note-bar-val" style="color:{c}">{nf:.1f}</div>
                    </div>
                    """, unsafe_allow_html=True)

        delta = float(s["moyenne_s2"]) - float(s["moyenne_s1"])
        prog_col  = "#22c55e" if delta >= 0 else "#f87171"
        prog_word = "progression" if delta >= 0 else "régression"
        nb_above  = sum(float(s[c]) >= float(df[c].mean()) for c in MATIERE_COLS)
        st.markdown(f"""
        <div class="interpret-box">
            📌 <strong>Analyse du profil :</strong><br>
            <strong>{s['prenom']}</strong> présente une
            <span style="color:{prog_col};font-weight:700;">{prog_word} de {'+' if delta>=0 else ''}{delta:.2f} pt(s)</span>
            entre S1 et S2.
            {'Cela traduit un effort soutenu ou une bonne adaptation au programme de S2.' if delta >= 0
             else 'Cela peut indiquer une surcharge de cours ou des difficultés croissantes.'}<br>
            Il/elle est au-dessus de la moyenne filière dans <strong>{nb_above}/10 matières</strong>.
            Rang <strong>#{rang}</strong> sur {n_students} —
            {'premier tiers de la promotion.' if rang <= max(1,n_students//3)
             else 'second tiers.' if rang <= max(1,2*n_students//3)
             else 'dernier tiers — un accompagnement est conseillé.'}
        </div>
        """, unsafe_allow_html=True)

        # Comparaison filière
        st.markdown('<div class="section-title">📊 Comparaison avec la filière</div>', unsafe_allow_html=True)
        comp_cols  = MATIERE_COLS
        comp_names = [COL_LABELS[c] for c in comp_cols]
        comp_df = pd.DataFrame({
            "Matière":  comp_names,
            "Étudiant": [float(s[c]) for c in comp_cols],
            "Filière":  [float(df[c].mean()) for c in comp_cols],
        }).set_index("Matière")
        st.bar_chart(comp_df)
        st.markdown(f"""
        <div class="interpret-box">
            📌 Barres bleues = notes de l'étudiant · Barres rouges = moyenne filière.
            <strong>{s['prenom']}</strong> dépasse la filière dans
            <strong>{nb_above}/10 matières</strong>.
            Les matières en dessous de la moyenne méritent un effort ciblé.
        </div>
        """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# TAB 3 — STATISTIQUES & RÉGRESSION
# ═══════════════════════════════════════════════════════════════
with tab_stats:
    if df.empty or n_students < 2:
        st.info("Minimum 2 étudiants nécessaires pour les analyses statistiques.")
    else:
        stat_cols = MATIERE_COLS + ["moyenne_s1","moyenne_s2","moyenne_generale"]

        # Statistiques descriptives
        st.markdown('<div class="section-title">📊 Statistiques descriptives</div>', unsafe_allow_html=True)
        desc = df[stat_cols].describe().round(2)
        desc.index = ["Effectif","Moyenne","Écart-type","Min","Q1 (25%)","Médiane","Q3 (75%)","Max"]
        desc.columns = [COL_LABELS.get(c, c) for c in stat_cols]
        st.dataframe(desc, use_container_width=True)
        st.markdown("""
        <div class="interpret-box">
            📌 <strong>Comment lire ce tableau :</strong><br>
            • <strong>Moyenne</strong> : note centrale de la cohorte. Si &lt; 10 → problème collectif dans la matière.<br>
            • <strong>Écart-type</strong> : mesure la dispersion. Élevé = niveaux très hétérogènes.<br>
            • <strong>Médiane</strong> : sépare les 50% inférieurs des 50% supérieurs. Plus robuste aux valeurs extrêmes que la moyenne.<br>
            • <strong>Q1 / Q3</strong> : 25% des étudiants sont sous Q1 ; 75% sous Q3.
              L'intervalle inter-quartile (Q3−Q1) mesure la dispersion des 50% centraux.
        </div>
        """, unsafe_allow_html=True)

        # Matrice de corrélation
        st.markdown('<div class="section-title">🔗 Matrice de corrélation (Pearson)</div>', unsafe_allow_html=True)
        corr = df[stat_cols].corr().round(3)
        corr.columns = [COL_LABELS.get(c, c) for c in stat_cols]
        corr.index   = [COL_LABELS.get(c, c) for c in stat_cols]
        st.dataframe(corr.style.background_gradient(cmap="RdYlGn", vmin=-1, vmax=1),
                     use_container_width=True)
        st.markdown("""
        <div class="interpret-box">
            📌 <strong>Lecture :</strong> r de Pearson entre chaque paire de variables.<br>
            • <span style="color:#22c55e;font-weight:700;">r proche de +1</span> : corrélation positive forte.<br>
            • <span style="color:#f87171;font-weight:700;">r proche de −1</span> : corrélation négative forte.<br>
            • r ≈ 0 : pas de lien linéaire détectable.<br>
            Les matières les plus corrélées à la <strong>Moy. Générale</strong> sont les meilleurs
            <strong>prédicteurs de réussite</strong> — elles méritent un investissement pédagogique prioritaire.
        </div>
        """, unsafe_allow_html=True)

        # Top / Flop
        st.markdown('<div class="section-title">🏆 Points forts & faiblesses de la filière</div>', unsafe_allow_html=True)
        mat_means  = {COL_LABELS[c]: float(df[c].mean()) for c in MATIERE_COLS}
        sorted_mat = sorted(mat_means.items(), key=lambda x: x[1], reverse=True)
        tf1, tf2 = st.columns(2)
        with tf1:
            st.markdown("**🟢 Top 3 — Meilleures matières**")
            for mat, moy in sorted_mat[:3]:
                st.markdown(f"""
                <div style="background:#052e16;border:2px solid #166534;border-radius:10px;
                            padding:.75rem 1.1rem;margin-bottom:.5rem;display:flex;
                            justify-content:space-between;align-items:center;">
                    <span style="color:#4ade80;font-weight:600;">{mat}</span>
                    <span style="font-family:'Space Mono',monospace;color:#4ade80;font-weight:700;">{moy:.2f}/20</span>
                </div>
                """, unsafe_allow_html=True)
        with tf2:
            st.markdown("**🔴 Flop 3 — À renforcer**")
            for mat, moy in sorted_mat[-3:]:
                st.markdown(f"""
                <div style="background:#2d0505;border:2px solid #7f1d1d;border-radius:10px;
                            padding:.75rem 1.1rem;margin-bottom:.5rem;display:flex;
                            justify-content:space-between;align-items:center;">
                    <span style="color:#f87171;font-weight:600;">{mat}</span>
                    <span style="font-family:'Space Mono',monospace;color:#f87171;font-weight:700;">{moy:.2f}/20</span>
                </div>
                """, unsafe_allow_html=True)
        st.markdown("""
        <div class="interpret-box">
            📌 Les matières du Flop 3 avec une moyenne &lt; 10 devraient faire l'objet de
            <strong>séances de soutien</strong>, d'une révision des méthodes pédagogiques,
            ou d'une redistribution des heures de cours.
        </div>
        """, unsafe_allow_html=True)

        # Régression
        st.markdown('<div class="section-title">📈 Régression linéaire simple (OLS)</div>', unsafe_allow_html=True)

        num_cols_reg = MATIERE_COLS + ["moyenne_s1","moyenne_s2","age"]
        col_r1, col_r2 = st.columns(2)
        with col_r1:
            x_var = st.selectbox("Variable X (prédicteur)", num_cols_reg,
                                 format_func=lambda c: COL_LABELS.get(c,c), index=11, key="xvar")
        with col_r2:
            y_opts = ["moyenne_generale"] + num_cols_reg
            y_var  = st.selectbox("Variable Y (cible)", y_opts,
                                  format_func=lambda c: COL_LABELS.get(c,"Moy. Générale"), key="yvar")

        x = df[x_var].astype(float).values
        y = df[y_var].astype(float).values

        x_mean, y_mean = x.mean(), y.mean()
        cov_xy = np.sum((x - x_mean) * (y - y_mean))
        var_x  = np.sum((x - x_mean) ** 2)
        b1     = cov_xy / var_x if var_x > 1e-10 else 0.0
        b0     = y_mean - b1 * x_mean
        y_pred = b0 + b1 * x

        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - y_mean) ** 2)
        r2     = max(0.0, 1.0 - ss_res / ss_tot) if ss_tot > 1e-10 else 0.0
        r_val  = float(np.corrcoef(x, y)[0, 1]) if len(set(x)) > 1 and len(set(y)) > 1 else 0.0
        rmse   = float(np.sqrt(ss_res / len(y))) if len(y) > 0 else 0.0

        rc1, rc2, rc3, rc4 = st.columns(4)
        for col, lbl, val, sub in [
            (rc1, "R² — Coeff. déterm.", f"{r2:.4f}", f"{r2*100:.1f}% variance expliquée"),
            (rc2, "Corrélation r", f"{r_val:.4f}", "Pearson [−1, +1]"),
            (rc3, "Pente β₁",  f"{b1:.4f}", "pts de Y par pt de X"),
            (rc4, "RMSE",      f"{rmse:.3f}", "Erreur moy. prédiction"),
        ]:
            with col:
                st.markdown(f"""
                <div class="metric-card purple" style="margin-bottom:1rem;">
                    <div class="metric-label">{lbl}</div>
                    <div class="metric-value" style="font-size:1.35rem;">{val}</div>
                    <div class="metric-sub">{sub}</div>
                </div>
                """, unsafe_allow_html=True)

        x_lbl = COL_LABELS.get(x_var, x_var)
        y_lbl = COL_LABELS.get(y_var, y_var)
        interp_r = ("très forte positive" if r_val > .85 else "forte positive" if r_val > .65
                    else "modérée positive" if r_val > .35 else "faible positive" if r_val > .1
                    else "très forte négative" if r_val < -.85 else "forte négative" if r_val < -.65
                    else "modérée négative" if r_val < -.35 else "faible négative" if r_val < -.1
                    else "nulle ou négligeable")
        r2_qual = ("excellent" if r2 > .85 else "bon" if r2 > .6 else "moyen" if r2 > .35 else "faible")
        dir_word = "augmente" if b1 >= 0 else "diminue"

        st.markdown(f"""
        <div class="interpret-box">
            📐 <strong>Équation de la droite OLS :</strong>
            <span style="color:#c084fc;font-weight:700;font-family:'Space Mono',monospace;">
                {y_lbl} = {b1:.4f} × {x_lbl} + {b0:.4f}
            </span><br><br>
            📌 <strong>Interprétation complète :</strong><br>
            • La corrélation entre <em>{x_lbl}</em> et <em>{y_lbl}</em> est
              <strong style="color:{'#22c55e' if abs(r_val)>.6 else '#f59e0b' if abs(r_val)>.3 else '#f87171'}">{interp_r}</strong>
              (r = {r_val:.3f}).<br>
            • Le R² = <strong>{r2:.4f}</strong> → le modèle explique <strong>{r2*100:.1f}%</strong>
              de la variabilité de <em>{y_lbl}</em>. Pouvoir prédictif : <strong>{r2_qual}</strong>.<br>
            • Pour chaque point gagné en <em>{x_lbl}</em>, <em>{y_lbl}</em>
              <strong>{dir_word}</strong> de <strong>{abs(b1):.4f} point(s)</strong>.<br>
            • RMSE = <strong>{rmse:.3f}</strong> → erreur moyenne de prédiction.
              {'Acceptable pour des notes /20.' if rmse < 2 else 'Élevé : un modèle non-linéaire pourrait mieux convenir.'}
        </div>
        """, unsafe_allow_html=True)

        # Graphiques nuage + droite
        st.markdown(f'<div class="section-title">📉 {x_lbl} → {y_lbl} : nuage & droite</div>', unsafe_allow_html=True)
        sort_idx      = np.argsort(x)
        x_s, yp_s    = x[sort_idx], y_pred[sort_idx]

        scatter_df = pd.DataFrame({x_lbl: x, y_lbl: y})
        line_df    = pd.DataFrame({x_lbl: x_s, "Droite de régression": yp_s})

        col_sc, col_ln = st.columns(2)
        with col_sc:
            st.markdown("**Nuage de points (données réelles)**")
            st.scatter_chart(scatter_df, x=x_lbl, y=y_lbl, color="#7c3aed")
        with col_ln:
            st.markdown("**Droite de régression ajustée (OLS)**")
            st.line_chart(line_df.set_index(x_lbl), color="#06b6d4")

        st.markdown("""
        <div class="interpret-box">
            📌 <strong>Lecture :</strong> Le nuage montre la dispersion réelle des données.
            Si les points s'alignent autour d'une diagonale, la corrélation est forte.<br>
            La droite de régression minimise la somme des carrés des résidus (<strong>MCO</strong>).
            Elle permet de <em>prédire</em> Y pour n'importe quel X.
            Plus les points sont proches de la droite, meilleur est le modèle.
            Les points très éloignés de la droite sont des <strong>valeurs aberrantes</strong> à analyser.
        </div>
        """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# TAB 4 — À PROPOS
# ═══════════════════════════════════════════════════════════════
with tab_about:
    st.markdown("""
    <div class="about-card">
        <h3>🎓 Qu'est-ce qu'EduStat ?</h3>
        <p>
            <strong style="color:#e2e2f0;">EduStat</strong> est une application web de gestion et d'analyse
            des performances académiques conçue pour la filière
            <strong style="color:#a855f7;">Licence 2 Informatique</strong>.
            Elle centralise les données de notation sur les deux semestres et fournit des outils statistiques
            et graphiques avancés pour aider enseignants et responsables pédagogiques à prendre des décisions éclairées.
        </p>
    </div>

    <div class="about-card">
        <h3>⚙️ Fonctionnalités</h3>
        <ul>
            <li><strong style="color:#e2e2f0;">Gestion des étudiants</strong> — Ajout / suppression avec matricule, prénom, nom, âge et toutes les notes S1 & S2.</li>
            <li><strong style="color:#e2e2f0;">Calcul automatique</strong> — Moyennes S1, S2 et générale calculées et stockées instantanément.</li>
            <li><strong style="color:#e2e2f0;">Tableau de bord</strong> — KPIs, classement dynamique, histogramme, comparaison S1 vs S2.</li>
            <li><strong style="color:#e2e2f0;">Profil individuel</strong> — Barres de progression, rang, évolution S1→S2, comparaison filière.</li>
            <li><strong style="color:#e2e2f0;">Statistiques descriptives</strong> — Moyenne, écart-type, médiane, Q1, Q3 pour toutes les matières.</li>
            <li><strong style="color:#e2e2f0;">Matrice de corrélation</strong> — Heatmap Pearson entre toutes les matières.</li>
            <li><strong style="color:#e2e2f0;">Régression linéaire OLS</strong> — R², r de Pearson, RMSE, pente, avec interprétation automatique détaillée.</li>
            <li><strong style="color:#e2e2f0;">Interprétations pédagogiques</strong> — Chaque graphique est accompagné d'une explication concrète et actionnable.</li>
        </ul>
    </div>

    <div class="about-card">
        <h3>📚 Matières couvertes</h3>
        <p><strong style="color:#60a5fa;">Semestre 1 :</strong>
            Programmation, Structures de données, Mathématiques, Architecture des ordinateurs, Système d'exploitation.</p>
        <p><strong style="color:#22d3ee;">Semestre 2 :</strong>
            Programmation avancée, Bases de données, Réseaux informatiques, Génie logiciel, Statistiques.</p>
    </div>

    <div class="about-card">
        <h3>🛠️ Stack technique</h3>
        <ul>
            <li><strong style="color:#e2e2f0;">Frontend :</strong> Streamlit (Python 3.10+)</li>
            <li><strong style="color:#e2e2f0;">Base de données :</strong> SQLite (local) · PostgreSQL (production via Railway)</li>
            <li><strong style="color:#e2e2f0;">Analyse :</strong> Pandas · NumPy</li>
            <li><strong style="color:#e2e2f0;">ORM :</strong> SQLAlchemy 2.x avec pool_pre_ping</li>
            <li><strong style="color:#e2e2f0;">Hébergement :</strong> Railway.app</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:2.5rem 0 1.5rem;margin-top:3rem;
            border-top:3px solid #1a1a40;font-family:'Space Mono',monospace;
            font-size:.68rem;color:#252550;letter-spacing:.12em;">
    EDUSTAT · L2 INFORMATIQUE · 2024–2025
</div>
""", unsafe_allow_html=True)
