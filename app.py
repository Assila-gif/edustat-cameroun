import os
import streamlit as st
import pandas as pd
import numpy as np
import io

from sqlalchemy import create_engine
from sklearn.linear_model import LinearRegression

# ================= CONFIG =================
st.set_page_config(
    page_title="EduStat L2 Informatique",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 EduStat L2 Informatique - Dashboard d'analyse")

# ================= DATABASE =================
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)

# ================= LOAD DATA =================
@st.cache_data(ttl=5)
def load_data():
    return pd.read_sql("SELECT * FROM students", engine)

df = load_data()

if df.empty:
    st.warning("Aucune donnée disponible")
    st.stop()

# ================= CLEAN DATA =================
numeric_cols = [
    "prog1","structures","maths","architecture","systeme",
    "prog2","bdd","reseaux","genie_logiciel","stats"
]

for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# ================= ANALYSES =================

df["moyenne_s1"] = df[["prog1","structures","maths","architecture","systeme"]].mean(axis=1)
df["moyenne_s2"] = df[["prog2","bdd","reseaux","genie_logiciel","stats"]].mean(axis=1)
df["moyenne"] = (df["moyenne_s1"] + df["moyenne_s2"]) / 2

# ================= METRICS =================
col1, col2, col3, col4 = st.columns(4)

col1.metric("Moyenne générale", round(df["moyenne"].mean(), 2))
col2.metric("Meilleur étudiant", df.loc[df["moyenne"].idxmax(), "name"])
col3.metric("Effectif", len(df))
col4.metric("Admis (%)", round((df["moyenne"] >= 10).mean()*100, 1))

# ================= CLASSEMENT =================
st.subheader("🏆 Classement général")

df_sorted = df.sort_values("moyenne", ascending=False)
st.dataframe(df_sorted[["matricule","name","moyenne"]])

# ================= GRAPHIQUES =================

col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Moyennes des étudiants")
    st.bar_chart(df.set_index("name")["moyenne"])

with col2:
    st.subheader("📈 S1 vs S2")
    st.bar_chart(df.set_index("name")[["moyenne_s1","moyenne_s2"]])

# ================= DISTRIBUTION =================
st.subheader("📊 Distribution des notes")

hist_data = pd.DataFrame({
    "moyenne": df["moyenne"]
})

st.bar_chart(hist_data)

# ================= CORRELATION =================
st.subheader("📌 Corrélation entre matières")

corr = df[numeric_cols].corr()

st.dataframe(corr)

# ================= MATIÈRES =================
st.subheader("📚 Analyse par matière")

matiere_moy = df[numeric_cols].mean().sort_values(ascending=False)

st.bar_chart(matiere_moy)

# ================= IA SIMPLE =================
st.subheader("🤖 Prédiction (IA simple)")

X = df[["prog1","prog2","bdd","reseaux"]]
y = df["moyenne"]

model = LinearRegression()
model.fit(X, y)

df["prediction"] = model.predict(X)

st.line_chart(df[["moyenne","prediction"]])

# ================= TABLE COMPLETE =================
st.subheader("📋 Données complètes")

st.dataframe(df)

# ================= EXPORT EXCEL =================
st.subheader("📥 Export des données")

def to_excel(data):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        data.to_excel(writer, index=False)
    return output.getvalue()

excel = to_excel(df)

st.download_button(
    "📥 Télécharger Excel",
    data=excel,
    file_name="edustat.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# ================= EXPORT CSV =================
csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    "📥 Télécharger CSV",
    data=csv,
    file_name="edustat.csv",
    mime="text/csv"
)

# ================= TOP / BOTTOM =================
st.subheader("🔝 Top 5 étudiants")
st.dataframe(df_sorted.head(5)[["name","moyenne"]])

st.subheader("⚠️ Étudiants en difficulté")
st.dataframe(df_sorted.tail(5)[["name","moyenne"]])
