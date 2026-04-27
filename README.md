# EduStat — L2 Informatique

Tableau de bord Streamlit pour la gestion et l'analyse des notes étudiants (S1 & S2).

## Déploiement sur Railway

1. Pousse ce dossier sur GitHub
2. Crée un nouveau projet sur [railway.app](https://railway.app)
3. Connecte ton repo GitHub
4. **Ajoute un service PostgreSQL** depuis Railway (Add Plugin → PostgreSQL)
5. Railway injecte automatiquement la variable `DATABASE_URL` → rien à faire

## Variables d'environnement

| Variable | Description |
|---|---|
| `DATABASE_URL` | Injectée automatiquement par Railway PostgreSQL |

## Lancer en local

```bash
pip install -r requirements.txt
streamlit run app.py
```

En local, l'app utilise SQLite (`edustat.db`) si `DATABASE_URL` n'est pas définie.
