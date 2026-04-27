import streamlit as st
import sqlite3
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
    CREATE TABLE IF NOT EXISTS custom_questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT,
        text TEXT,
        tag TEXT,
        level TEXT
    )
''')
conn.commit()

# --- 80 QUESTIONS CONCRÈTES ET EXPLICITES ---
BASE_QUESTIONS = [
    {"id": 1, "text": "Longs baisers profonds avec la langue pendant de longues minutes (baisers passionnés et langoureux)", "tag": "sensuel", "level": "Soft"},
    {"id": 2, "text": "Massage lent et sensuel de tout le corps avec de l'huile chaude avant tout rapport", "tag": "sensuel", "level": "Soft"},
    {"id": 3, "text": "Se caresser mutuellement très longtemps sans pénétration", "tag": "sensuel", "level": "Soft"},
    {"id": 4, "text": "Strip-tease lent et sensuel pour l'autre", "tag": "sensuel", "level": "Soft"},
    {"id": 5, "text": "Se regarder intensément dans les yeux pendant qu'on se touche", "tag": "sensuel", "level": "Soft"},
    {"id": 6, "text": "Préliminaires oraux très longs et attentionnés", "tag": "oral", "level": "Soft"},
    {"id": 7, "text": "Cunnilingus lent et créatif", "tag": "oral", "level": "Soft"},
    {"id": 8, "text": "Fellation lente et profonde avec beaucoup de salive", "tag": "oral", "level": "Soft"},
    {"id": 9, "text": "Missionnaire profond avec beaucoup de contact visuel", "tag": "penetration", "level": "Soft"},
    {"id": 10, "text": "Sexe en cuillères (spooning) très collé-serré", "tag": "penetration", "level": "Soft"},

    {"id": 11, "text": "Doggy style bien cambré", "tag": "penetration", "level": "Medium"},
    {"id": 12, "text": "Cowgirl / Reverse cowgirl en contrôlant le rythme", "tag": "penetration", "level": "Medium"},
    {"id": 13, "text": "Parler salement pendant l'acte (dirty talk)", "tag": "parole", "level": "Medium"},
    {"id": 14, "text": "Se masturber devant l'autre en se regardant", "tag": "voyeur", "level": "Medium"},
    {"id": 15, "text": "Utiliser un vibromasseur pendant la pénétration", "tag": "jouet", "level": "Medium"},
    {"id": 16, "text": "Plug anal porté pendant un rapport vaginal", "tag": "anal", "level": "Medium"},
    {"id": 17, "text": "Fessées légères pendant l'acte", "tag": "bdsm", "level": "Medium"},
    {"id": 18, "text": "Edging (contrôler l'orgasme longuement)", "tag": "hard", "level": "Medium"},
    {"id": 19, "text": "Sexe debout contre un mur", "tag": "penetration", "level": "Medium"},
    {"id": 20, "text": "Regarder l'autre se masturber jusqu'à l'orgasme", "tag": "voyeur", "level": "Medium"},

    {"id": 21, "text": "Levrette forte et profonde", "tag": "penetration", "level": "Hard"},
    {"id": 22, "text": "Pénétration anale douce et progressive", "tag": "anal", "level": "Hard"},
    {"id": 23, "text": "Se faire attacher avec des menottes ou foulards", "tag": "bdsm", "level": "Hard"},
    {"id": 24, "text": "Fessées plus marquantes", "tag": "bdsm", "level": "Hard"},
    {"id": 25, "text": "Deepthroat intense", "tag": "oral", "level": "Hard"},
    {"id": 26, "text": "Éjaculation faciale ou sur les seins", "tag": "facial", "level": "Hard"},
    {"id": 27, "text": "Rough sex (violent et bestial consentie)", "tag": "hard", "level": "Hard"},
    {"id": 28, "text": "Light choking (main sur la gorge)", "tag": "hard", "level": "Hard"},
    {"id": 29, "text": "Filmer pendant l'acte", "tag": "exhib", "level": "Hard"},
    {"id": 30, "text": "Pegging (elle sodomise lui)", "tag": "pegging", "level": "Hard"},

    {"id": 31, "text": "Pénétration anale très intense", "tag": "anal", "level": "Very Hard"},
    {"id": 32, "text": "Fisting vaginal ou anal", "tag": "extreme", "level": "Very Hard"},
    {"id": 33, "text": "Golden shower (uriner sur l'autre)", "tag": "extreme", "level": "Very Hard"},
    {"id": 34, "text": "Candaulisme (regarder l'autre avec quelqu'un)", "tag": "voyeur", "level": "Very Hard"},
    {"id": 35, "text": "Humiliation légère consentie", "tag": "bdsm", "level": "Very Hard"},
    {"id": 36, "text": "Consensual Non-Consent (CNC - viol fantasy)", "tag": "extreme", "level": "Very Hard"},
    {"id": 37, "text": "Gangbang fantasy", "tag": "extreme", "level": "Extreme"},
    {"id": 38, "text": "Humiliation forte", "tag": "extreme", "level": "Extreme"},
    {"id": 39, "text": "Jeu de chasteté (cage à pénis)", "tag": "bdsm", "level": "Extreme"},
    {"id": 40, "text": "Public play avec vibro télécommandé", "tag": "exhib", "level": "Extreme"},
]

for i in range(41, 81):
    BASE_QUESTIONS.append({
        "id": i,
        "text": f"Fantasme coquin à définir ensemble (question {i})",
        "tag": "love",
        "level": "Variable"
    })

QUESTIONS = BASE_QUESTIONS.copy()

# --- FONCTIONS ---
def load_all_questions():
    c.execute("SELECT id, text, tag, level FROM custom_questions")
    custom = [{"id": row[0] + 1000, "text": row[1], "tag": row[2], "level": row[3]} for row in c.fetchall()]
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

def add_custom_question(user, text, tag, level):
    c.execute("INSERT INTO custom_questions (user, text, tag, level) VALUES (?, ?, ?, ?)",
              (user, text, tag, level))
    conn.commit()

def reset_db():
    c.execute("DELETE FROM answers")
    c.execute("DELETE FROM custom_questions")
    conn.commit()
    st.toast("✅ Tout a été réinitialisé !", icon="🔄")
    st.rerun()

# --- INTERFACE ---
st.title("🔥 Smash or Pass – Notre Univers Coquin 2026")

st.markdown("### Qui tient le téléphone ? 📱")
user = st.radio("Profil :", ["Julien", "Lydie"], horizontal=True, label_visibility="collapsed")

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

    col1, col2 = st.columns(2)
    with col1:
        if st.button("❌ PASS", use_container_width=True):
            save_answer(user, next_q["id"], "pass")
            st.rerun()
    with col2:
        if st.button("❤️ SMASH", type="primary", use_container_width=True):
            comfort = st.slider("Niveau de confort (1→5)", 1, 5, 4, key=f"comf_{next_q['id']}")
            save_answer(user, next_q["id"], "smash", comfort)
            st.success("Smash enregistré !")
            st.rerun()
else:
    st.success(f"🎉 Bravo {user} ! Tu as terminé les 80 questions.")

# --- RÉSULTATS ---
st.write("---")
st.subheader("🔥 Nos Matchs Coquins")

matches = get_matches()

if not matches:
    st.info("Pas encore de smash commun. Continuez à swiper !")
else:
    st.success(f"**{len(matches)} fantasmes validés à deux !**")
    
    tag_count = defaultdict(int)
    for m in matches:
        tag_count[m["tag"]] += 1

    st.write("**Répartition :**")
    for tag, count in sorted(tag_count.items(), key=lambda x: x[1], reverse=True):
        st.progress(count / max(len(matches), 1))
        st.caption(f"**{tag.capitalize()}** : {count}")

    with st.expander("Détail des matchs"):
        for m in matches:
            st.write(f"• {m['text']}")

# --- QUESTION PERSONNALISÉE ---
st.write("---")
st.subheader("➕ Ajouter une question personnalisée")
with st.form("custom_form"):
    txt = st.text_area("Ton fantasme précis :", placeholder="Ex: Se faire attacher et utiliser comme objet sexuel...")
    c1, c2 = st.columns(2)
    with c1:
        tag = st.selectbox("Catégorie", ["sensuel", "oral", "penetration", "anal", "bdsm", "hard", "extreme", "trois", "love"])
    with c2:
        lvl = st.selectbox("Niveau", ["Soft", "Medium", "Hard", "Very Hard", "Extreme"])
    if st.form_submit_button("Ajouter"):
        if txt.strip():
            add_custom_question(user, txt.strip(), tag, lvl)
            st.success("Question ajoutée !")
            st.rerun()

# --- RESET (maintenant plus puissant) ---
with st.expander("⚙️ Paramètres & Reset"):
    st.warning("⚠️ Cette action va supprimer TOUTES les réponses de Julien et Lydie + les questions personnalisées.")
    if st.button("🔄 Reboot complet – Tout effacer et recommencer", type="secondary"):
        if st.checkbox("Je confirme vouloir tout supprimer"):
            reset_db()

st.caption("Amusez-vous bien ❤️🔥")
