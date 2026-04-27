import streamlit as st
import sqlite3
import plotly.express as px
from collections import defaultdict

# --- CONFIGURATION ---
st.set_page_config(page_title="Smash or Pass Coquin 2026 🔥", page_icon="🔥", layout="centered")

# --- BASE DE DONNÉES ---
conn = sqlite3.connect("couple_coquin.db", check_same_thread=False)
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS answers (
        user TEXT,
        question_id INTEGER,
        answer TEXT,
        comfort INTEGER,
        PRIMARY KEY (user, question_id)
    )
''')
c.execute('''
    CREATE TABLE IF NOT EXISTS limits (
        user TEXT PRIMARY KEY,
        hard_limits TEXT,
        safeword TEXT
    )
''')
c.execute('''
    CREATE TABLE IF NOT EXISTS custom_questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT,
        text TEXT,
        tag TEXT,
        level TEXT
    )
''')
conn.commit()

# --- 100 QUESTIONS PROGRESSIVES ---
BASE_QUESTIONS = [
    # === NIVEAU SOFT (1-15) ===
    {"id": 1, "text": "Longs baisers profonds avec la langue pendant de longues minutes", "tag": "sensuel", "level": "Soft"},
    {"id": 2, "text": "Massage lent et sensuel de tout le corps avec de l'huile chaude", "tag": "sensuel", "level": "Soft"},
    {"id": 3, "text": "Se caresser mutuellement très longtemps sans pénétration", "tag": "sensuel", "level": "Soft"},
    {"id": 4, "text": "Strip-tease lent et sensuel pour l'autre", "tag": "sensuel", "level": "Soft"},
    {"id": 5, "text": "Se regarder intensément dans les yeux pendant qu'on se touche", "tag": "sensuel", "level": "Soft"},
    {"id": 6, "text": "Préliminaires oraux très longs et attentionnés", "tag": "oral", "level": "Soft"},
    {"id": 7, "text": "Cunnilingus lent et créatif avec beaucoup de temps", "tag": "oral", "level": "Soft"},
    {"id": 8, "text": "Fellation lente et profonde avec beaucoup de salive", "tag": "oral", "level": "Soft"},
    {"id": 9, "text": "Missionnaire profond avec beaucoup de contact visuel et câlins", "tag": "penetration", "level": "Soft"},
    {"id": 10, "text": "Sexe en cuillères (spooning) très collé-serré et doux", "tag": "penetration", "level": "Soft"},
    {"id": 11, "text": "Sexe du matin au réveil, encore à moitié endormi", "tag": "sensuel", "level": "Soft"},
    {"id": 12, "text": "Se faire lécher partout (cou, seins, ventre, cuisses…)", "tag": "oral", "level": "Soft"},
    {"id": 13, "text": "69 très lent et sensuel", "tag": "oral", "level": "Soft"},
    {"id": 14, "text": "Sexe dans la douche ou le bain avec caresses", "tag": "sensuel", "level": "Soft"},
    {"id": 15, "text": "Dire des mots tendres et 'je t'aime' pendant l'acte", "tag": "love", "level": "Soft"},

    # === NIVEAU MEDIUM (16-35) ===
    {"id": 16, "text": "Doggy style bien cambré", "tag": "penetration", "level": "Medium"},
    {"id": 17, "text": "Cowgirl / Reverse cowgirl en contrôlant le rythme", "tag": "penetration", "level": "Medium"},
    {"id": 18, "text": "Parler salement pendant l'acte", "tag": "parole", "level": "Medium"},
    {"id": 19, "text": "Se masturber devant l'autre en se regardant", "tag": "voyeur", "level": "Medium"},
    {"id": 20, "text": "Utiliser un vibromasseur clitoridien pendant la pénétration", "tag": "jouet", "level": "Medium"},
    {"id": 21, "text": "Plug anal porté pendant un rapport vaginal", "tag": "anal", "level": "Medium"},
    {"id": 22, "text": "Fessées légères pendant l'acte", "tag": "bdsm", "level": "Medium"},
    {"id": 23, "text": "Edging (contrôle de l'orgasme pendant longtemps)", "tag": "hard", "level": "Medium"},
    {"id": 24, "text": "Sexe debout contre un mur", "tag": "penetration", "level": "Medium"},
    {"id": 25, "text": "Regarder l'autre se masturber jusqu'à l'orgasme", "tag": "voyeur", "level": "Medium"},

    # === NIVEAU HARD (26-50) ===
    {"id": 26, "text": "Levrette forte et profonde", "tag": "penetration", "level": "Hard"},
    {"id": 27, "text": "Pénétration anale douce et progressive", "tag": "anal", "level": "Hard"},
    {"id": 28, "text": "Se faire attacher avec des menottes ou foulards", "tag": "bdsm", "level": "Hard"},
    {"id": 29, "text": "Fessées plus marquantes", "tag": "bdsm", "level": "Hard"},
    {"id": 30, "text": "Deepthroat intense", "tag": "oral", "level": "Hard"},
    {"id": 31, "text": "Éjaculation faciale ou sur les seins", "tag": "facial", "level": "Hard"},
    {"id": 32, "text": "Rough sex (un peu violent et bestial)", "tag": "hard", "level": "Hard"},
    {"id": 33, "text": "Light choking (main sur la gorge)", "tag": "hard", "level": "Hard"},
    {"id": 34, "text": "Sexe dans un lieu semi-public avec risque", "tag": "exhib", "level": "Hard"},
    {"id": 35, "text": "Jeu de rôle (prof/élève, patron/secrétaire…)", "tag": "roleplay", "level": "Hard"},
    {"id": 36, "text": "Filmer ou se prendre en photo pendant l'acte", "tag": "exhib", "level": "Hard"},
    {"id": 37, "text": "Wax play (bougie chaude sur la peau)", "tag": "bdsm", "level": "Hard"},
    {"id": 38, "text": "Pegging (elle sodomise lui avec un strap-on)", "tag": "pegging", "level": "Hard"},
    {"id": 39, "text": "Fantasme de plan à trois (MFF ou MMF)", "tag": "trois", "level": "Hard"},
    {"id": 40, "text": "Breeding / impregnation fantasy", "tag": "hard", "level": "Hard"},
    {"id": 41, "text": "Rimjob (lécher l'anus)", "tag": "oral", "level": "Hard"},
    {"id": 42, "text": "Double pénétration (pénis + jouet)", "tag": "double", "level": "Hard"},
    {"id": 43, "text": "Être dominé(e) complètement avec ordres", "tag": "bdsm", "level": "Hard"},
    {"id": 44, "text": "Sexe anal plus intense", "tag": "anal", "level": "Hard"},
    {"id": 45, "text": "Orgasm control très long", "tag": "hard", "level": "Hard"},

    # === NIVEAU VERY HARD (46-70) ===
    {"id": 46, "text": "Pénétration anale très intense et profonde", "tag": "anal", "level": "Very Hard"},
    {"id": 47, "text": "Fisting vaginal ou anal", "tag": "extreme", "level": "Very Hard"},
    {"id": 48, "text": "Golden shower (uriner dessus ou boire)", "tag": "extreme", "level": "Very Hard"},
    {"id": 49, "text": "Candaulisme (regarder l'autre avec quelqu'un)", "tag": "voyeur", "level": "Very Hard"},
    {"id": 50, "text": "Humiliation légère (insultes sexuelles, etc.)", "tag": "bdsm", "level": "Very Hard"},
    {"id": 51, "text": "Consensual Non-Consent (CNC - viol fantasy)", "tag": "extreme", "level": "Very Hard"},
    {"id": 52, "text": "Jeux de douleur plus forte (pinces, wax intensif)", "tag": "extreme", "level": "Very Hard"},
    {"id": 53, "text": "Sexe pendant les règles avec creampie", "tag": "tabou", "level": "Very Hard"},
    {"id": 54, "text": "Utiliser des poppers pendant l'acte", "tag": "extreme", "level": "Very Hard"},
    {"id": 55, "text": "Double pénétration anale + vaginale", "tag": "extreme", "level": "Very Hard"},

    # === NIVEAU EXTREME + QUESTIONS OUVERTES (56-100) ===
    {"id": 56, "text": "Gangbang ou orgie (fantasme ou réel)", "tag": "extreme", "level": "Extreme"},
    {"id": 57, "text": "Scat play", "tag": "extreme", "level": "Extreme"},
    {"id": 58, "text": "Humiliation forte et jeux de dégradation", "tag": "extreme", "level": "Extreme"},
    {"id": 59, "text": "Jeu de chasteté (cage à pénis)", "tag": "bdsm", "level": "Extreme"},
    {"id": 60, "text": "Public play avec vibro télécommandé", "tag": "exhib", "level": "Extreme"},
]

# Compléter jusqu'à 100 avec des questions ouvertes / personnalisables
for i in range(61, 101):
    BASE_QUESTIONS.append({
        "id": i,
        "text": f"Explorer un nouveau fantasme très personnel ou pratique coquine à définir ensemble (question {i})",
        "tag": "love",
        "level": "Variable"
    })

QUESTIONS = BASE_QUESTIONS.copy()

# (Le reste du code est identique à la version précédente : fonctions, interface, limites, questions personnalisées, graphique, etc.)

# --- FONCTIONS (identiques) ---
def load_all_questions():
    c.execute("SELECT id, text, tag, level FROM custom_questions")
    custom = [{"id": row[0]+1000, "text": row[1], "tag": row[2], "level": row[3]} for row in c.fetchall()]
    return QUESTIONS + custom

def save_answer(user, q_id, answer, comfort=None):
    c.execute("REPLACE INTO answers (user, question_id, answer, comfort) VALUES (?, ?, ?, ?)",
              (user, q_id, answer, comfort))
    conn.commit()

def get_user_answers(user):
    c.execute("SELECT question_id, answer, comfort FROM answers WHERE user=?", (user,))
    return {row[0]: {"answer": row[1], "comfort": row[2]} for row in c.fetchall()}

def get_matches():
    c.execute('''
        SELECT a1.question_id 
        FROM answers a1 
        JOIN answers a2 ON a1.question_id = a2.question_id 
        WHERE a1.user = 'Julien' AND a2.user = 'Lydie' 
        AND a1.answer = 'smash' AND a2.answer = 'smash'
    ''')
    matched_ids = [row[0] for row in c.fetchall()]
    all_q = load_all_questions()
    return [q for q in all_q if q["id"] in matched_ids]

def save_limits(user, hard_limits, safeword):
    c.execute("REPLACE INTO limits (user, hard_limits, safeword) VALUES (?, ?, ?)", 
              (user, hard_limits, safeword))
    conn.commit()

def get_limits(user):
    c.execute("SELECT hard_limits, safeword FROM limits WHERE user=?", (user,))
    row = c.fetchone()
    return row if row else ("Aucune limite définie", "ROUGE")

def add_custom_question(user, text, tag, level):
    c.execute("INSERT INTO custom_questions (user, text, tag, level) VALUES (?, ?, ?, ?)",
              (user, text, tag, level))
    conn.commit()

def reset_db():
    c.execute("DELETE FROM answers")
    c.execute("DELETE FROM limits")
    c.execute("DELETE FROM custom_questions")
    conn.commit()

# --- INTERFACE (identique à la version précédente) ---
st.title("🔥 Smash or Pass – Notre Univers Coquin 2026")

st.markdown("### Qui tient le téléphone ? 📱")
user = st.radio("Profil :", ["Julien", "Lydie"], horizontal=True, label_visibility="collapsed")

# Section Limites (inchangée)
st.subheader("🚫 Limites & Consentement")
col1, col2 = st.columns(2)
with col1:
    if user == "Julien":
        limits = get_limits("Julien")
        hard = st.text_area("Mes limites dures :", value=limits[0], key="hard_j")
        sw = st.text_input("Mon safeword :", value=limits[1], key="sw_j")
        if st.button("Enregistrer mes limites", key="save_j"):
            save_limits("Julien", hard, sw)
            st.success("✅ Limites enregistrées")

with col2:
    if user == "Lydie":
        limits = get_limits("Lydie")
        hard = st.text_area("Mes limites dures :", value=limits[0], key="hard_l")
        sw = st.text_input("Mon safeword :", value=limits[1], key="sw_l")
        if st.button("Enregistrer mes limites", key="save_l"):
            save_limits("Lydie", hard, sw)
            st.success("✅ Limites enregistrées")

st.write("---")

blind_mode = st.checkbox("🔒 Mode Découverte à l'aveugle (recommandé)", value=True)

all_questions = load_all_questions()
user_answers = get_user_answers(user)
answered_count = len(user_answers)

next_q = next((q for q in all_questions if q["id"] not in user_answers), None)

if next_q:
    progress = answered_count / len(all_questions)
    st.progress(progress)
    st.caption(f"Question {answered_count + 1} / {len(all_questions)} — **{next_q.get('level', 'Variable')}**")

    st.markdown(f"""
    <div style='background:#2a2a3a; padding:30px; border-radius:15px; text-align:center; border:2px solid #ff4d94; margin:20px 0;'>
        <h3 style='color:#ff99cc;'>{next_q['text']}</h3>
    </div>
    """, unsafe_allow_html=True)

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("❌ PASS", use_container_width=True):
            save_answer(user, next_q["id"], "pass")
            st.rerun()
    with col_btn2:
        if st.button("❤️ SMASH", type="primary", use_container_width=True):
            comfort = st.slider("Niveau de confort avec ce fantasme (1 → 5)", 1, 5, 4, key=f"comfort_{next_q['id']}")
            save_answer(user, next_q["id"], "smash", comfort)
            st.success("Smash enregistré !")
            st.rerun()

else:
    st.success(f"🎉 Bravo {user} ! Tu as terminé les 100 questions.")

# --- RÉSULTATS (identique) ---
st.write("---")
st.subheader("🔥 Nos Matchs Coquins")

matches = get_matches()

if not matches:
    st.info("Pas encore de smash commun. Quand vous aurez fini tous les deux, vous verrez les résultats.")
else:
    st.success(f"**{len(matches)} fantasmes validés à deux !**")

    tag_count = defaultdict(int)
    level_count = defaultdict(int)
    for m in matches:
        tag_count[m["tag"]] += 1
        level_count[m["level"]] += 1

    if tag_count:
        fig = px.bar(x=list(tag_count.keys()), y=list(tag_count.values()),
                     labels={"x": "Catégorie", "y": "Smash communs"},
                     title="Répartition de vos fantasmes communs")
        st.plotly_chart(fig, use_container_width=True)

    extreme_score = level_count.get("Extreme", 0) + level_count.get("Very Hard", 0)
    if extreme_score >= 8:
        style = "🚨 **Style Extrême / Hardcore**"
    elif extreme_score >= 4:
        style = "🔥 **Style Hard & Kinky**"
    elif level_count.get("Medium", 0) >= 10:
        style = "🌶️ **Style Sensuel & Joueur**"
    else:
        style = "❤️ **Style Romantique & Intime**"
    st.info(style)

    with st.expander("Voir le détail des matchs communs"):
        for m in matches:
            st.markdown(f"• **{m.get('level', '')}** — {m['text']}")

# --- QUESTION PERSONNALISÉE (identique) ---
st.write("---")
st.subheader("➕ Ajouter une question personnalisée")
with st.form("custom_form"):
    custom_text = st.text_area("Décris ton fantasme :", placeholder="Exemple : Se faire attacher et utiliser comme objet sexuel...")
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        custom_tag = st.selectbox("Catégorie", ["sensuel", "oral", "penetration", "anal", "bdsm", "hard", "extreme", "trois", "love", "jouet", "voyeur", "exhib"])
    with col_t2:
        custom_level = st.selectbox("Niveau", ["Soft", "Medium", "Hard", "Very Hard", "Extreme", "Variable"])
    
    if st.form_submit_button("Ajouter cette question"):
        if custom_text.strip():
            add_custom_question(user, custom_text.strip(), custom_tag, custom_level)
            st.success("Question ajoutée pour les deux !")
            st.rerun()

# --- RESET ---
with st.expander("⚙️ Paramètres"):
    if st.button("🔄 Tout effacer et recommencer", type="secondary"):
        if st.checkbox("Je confirme la suppression complète"):
            reset_db()
            st.success("Tout réinitialisé.")
            st.rerun()

st.caption("Jouez toujours en respectant le consentement, les limites et le safeword. Amusez-vous bien ❤️🔥")
