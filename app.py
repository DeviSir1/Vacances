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
    # SOFT
    {"id": 1, "text": "Longs baisers profonds avec la langue pendant de longues minutes (baisers passionnés et langoureux)", "tag": "sensuel", "level": "Soft"},
    {"id": 2, "text": "Massage lent et sensuel de tout le corps avec de l'huile chaude avant tout rapport", "tag": "sensuel", "level": "Soft"},
    {"id": 3, "text": "Se caresser mutuellement très longtemps sans pénétration (caresses partout sauf pénétration)", "tag": "sensuel", "level": "Soft"},
    {"id": 4, "text": "Strip-tease lent et sensuel pour l'autre (se déshabiller lentement en dansant)", "tag": "sensuel", "level": "Soft"},
    {"id": 5, "text": "Se regarder intensément dans les yeux pendant qu'on se touche ou pendant le sexe", "tag": "sensuel", "level": "Soft"},
    {"id": 6, "text": "Préliminaires oraux très longs et attentionnés (se lécher et sucer longtemps)", "tag": "oral", "level": "Soft"},
    {"id": 7, "text": "Cunnilingus lent et créatif (lécher le clitoris et la vulve longuement)", "tag": "oral", "level": "Soft"},
    {"id": 8, "text": "Fellation lente et profonde avec beaucoup de salive (sucer le pénis lentement et profondément)", "tag": "oral", "level": "Soft"},
    {"id": 9, "text": "Missionnaire profond avec beaucoup de contact visuel et câlins (position face à face)", "tag": "penetration", "level": "Soft"},
    {"id": 10, "text": "Sexe en cuillères (spooning) très collé-serré et doux (par derrière en cuillère)", "tag": "penetration", "level": "Soft"},

    # MEDIUM
    {"id": 11, "text": "Doggy style bien cambré (levrette classique, pénétration par derrière)", "tag": "penetration", "level": "Medium"},
    {"id": 12, "text": "Cowgirl / Reverse cowgirl en contrôlant le rythme (elle sur lui, face ou dos)", "tag": "penetration", "level": "Medium"},
    {"id": 13, "text": "Parler salement pendant l'acte (dirty talk : dire des choses crues)", "tag": "parole", "level": "Medium"},
    {"id": 14, "text": "Se masturber devant l'autre en se regardant dans les yeux", "tag": "voyeur", "level": "Medium"},
    {"id": 15, "text": "Utiliser un vibromasseur clitoridien pendant la pénétration vaginale", "tag": "jouet", "level": "Medium"},
    {"id": 16, "text": "Plug anal porté pendant un rapport vaginal (petit jouet dans l'anus pendant le sexe)", "tag": "anal", "level": "Medium"},
    {"id": 17, "text": "Fessées légères pendant l'acte (claques sur les fesses)", "tag": "bdsm", "level": "Medium"},
    {"id": 18, "text": "Edging (contrôler l'orgasme en s'arrêtant juste avant pour prolonger le plaisir)", "tag": "hard", "level": "Medium"},
    {"id": 19, "text": "Sexe debout contre un mur (porté ou appuyé)", "tag": "penetration", "level": "Medium"},
    {"id": 20, "text": "Regarder l'autre se masturber jusqu'à l'orgasme", "tag": "voyeur", "level": "Medium"},

    # HARD
    {"id": 21, "text": "Levrette forte et profonde (doggy style intense et rapide)", "tag": "penetration", "level": "Hard"},
    {"id": 22, "text": "Pénétration anale douce et progressive (première fois ou douce sodomie)", "tag": "anal", "level": "Hard"},
    {"id": 23, "text": "Se faire attacher avec des menottes ou foulards (bondage léger)", "tag": "bdsm", "level": "Hard"},
    {"id": 24, "text": "Fessées plus marquantes et répétées (spanking fort)", "tag": "bdsm", "level": "Hard"},
    {"id": 25, "text": "Deepthroat intense (sucer très profondément jusqu'au fond de la gorge)", "tag": "oral", "level": "Hard"},
    {"id": 26, "text": "Éjaculation faciale ou sur les seins (cumshot sur le visage ou la poitrine)", "tag": "facial", "level": "Hard"},
    {"id": 27, "text": "Rough sex (sexe violent et bestial de manière consentie : tirer les cheveux, claques, etc.)", "tag": "hard", "level": "Hard"},
    {"id": 28, "text": "Light choking (main légère sur la gorge pendant le sexe)", "tag": "hard", "level": "Hard"},
    {"id": 29, "text": "Filmer ou se prendre en photo pendant l'acte (vidéo ou photos érotiques)", "tag": "exhib", "level": "Hard"},
    {"id": 30, "text": "Wax play (faire couler de la cire chaude de bougie sur la peau)", "tag": "bdsm", "level": "Hard"},
    {"id": 31, "text": "Pegging (elle porte un strap-on et sodomise lui analement)", "tag": "pegging", "level": "Hard"},
    {"id": 32, "text": "Rimjob (lécher l'anus de l'autre avec la langue)", "tag": "oral", "level": "Hard"},
    {"id": 33, "text": "Double pénétration (pénis + jouet en même temps)", "tag": "double", "level": "Hard"},
    {"id": 34, "text": "Fantasme de plan à trois (MFF ou MMF) – en parler ou simuler", "tag": "trois", "level": "Hard"},
    {"id": 35, "text": "Breeding fantasy (fantasme de se faire remplir sans protection pour 'faire un bébé')", "tag": "hard", "level": "Hard"},

    # VERY HARD / EXTREME
    {"id": 36, "text": "Pénétration anale très intense et profonde (sodomie hard)", "tag": "anal", "level": "Very Hard"},
    {"id": 37, "text": "Fisting vaginal ou anal (introduire toute la main dans le vagin ou l'anus)", "tag": "extreme", "level": "Very Hard"},
    {"id": 38, "text": "Golden shower (uriner sur l'autre ou se faire uriner dessus pendant le jeu sexuel)", "tag": "extreme", "level": "Very Hard"},
    {"id": 39, "text": "Candaulisme (regarder son partenaire avoir un rapport sexuel avec quelqu'un d'autre)", "tag": "voyeur", "level": "Very Hard"},
    {"id": 40, "text": "Humiliation légère (insultes sexuelles consenties, se faire traiter de salope, etc.)", "tag": "bdsm", "level": "Very Hard"},
    {"id": 41, "text": "Consensual Non-Consent (CNC) – simuler un viol fantasy avec safeword", "tag": "extreme", "level": "Very Hard"},
    {"id": 42, "text": "Jeux de douleur plus forte (pinces à seins, morsures fortes, etc.)", "tag": "extreme", "level": "Very Hard"},
    {"id": 43, "text": "Sexe pendant les règles avec creampie (éjaculation intérieure pendant les règles)", "tag": "tabou", "level": "Very Hard"},
    {"id": 44, "text": "Utiliser des poppers pendant l'acte pour intensifier les sensations", "tag": "extreme", "level": "Very Hard"},
    {"id": 45, "text": "Double pénétration anale + vaginale (deux pénétrations en même temps)", "tag": "extreme", "level": "Very Hard"},
    {"id": 46, "text": "Gangbang fantasy (se faire prendre par plusieurs personnes – en parler ou simuler)", "tag": "extreme", "level": "Extreme"},
    {"id": 47, "text": "Humiliation forte et jeux de dégradation (se faire traiter comme un objet sexuel)", "tag": "extreme", "level": "Extreme"},
    {"id": 48, "text": "Jeu de chasteté (mettre une cage à pénis et contrôler les orgasmes)", "tag": "bdsm", "level": "Extreme"},
    {"id": 49, "text": "Public play avec vibro télécommandé en public", "tag": "exhib", "level": "Extreme"},
    {"id": 50, "text": "Face sitting (s'asseoir sur le visage de l'autre pour se faire lécher)", "tag": "oral", "level": "Hard"},
]

# Compléter jusqu'à 80
for i in range(51, 81):
    BASE_QUESTIONS.append({
        "id": i,
        "text": f"Autre fantasme coquin à définir ensemble (question {i})",
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
    st.success("✅ Tout a été réinitialisé. Rafraîchis la page.")
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

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("❌ PASS", use_container_width=True):
            save_answer(user, next_q["id"], "pass")
            st.rerun()
    with col_btn2:
        if st.button("❤️ SMASH", type="primary", use_container_width=True):
            comfort = st.slider("Niveau de confort avec ce fantasme (1 = pas à l'aise → 5 = très excité)", 1, 5, 4, key=f"comfort_{next_q['id']}")
            save_answer(user, next_q["id"], "smash", comfort)
            st.success("Smash enregistré !")
            st.rerun()

else:
    st.success(f"🎉 Bravo {user} ! Tu as terminé toutes les questions.")

# --- RÉSULTATS ---
st.write("---")
st.subheader("🔥 Nos Matchs Coquins")

matches = get_matches()

if not matches:
    st.info("Pas encore de smash commun. Continuez à swiper tous les deux !")
else:
    st.success(f"**{len(matches)} fantasmes validés à deux !**")

    tag_count = defaultdict(int)
    level_count = defaultdict(int)
    for m in matches:
        tag_count[m["tag"]] += 1
        level_count[m["level"]] += 1

    st.write("**Répartition des smash communs :**")
    for tag, count in sorted(tag_count.items(), key=lambda x: x[1], reverse=True):
        st.progress(count / max(len(matches), 1))
        st.caption(f"**{tag.capitalize()}** : {count} smash")

    extreme_score = level_count.get("Extreme", 0) + level_count.get("Very Hard", 0)
    if extreme_score >= 8:
        style = "🚨 **Style Extrême / Hardcore Kink**"
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

# --- AJOUT QUESTION PERSONNALISÉE ---
st.write("---")
st.subheader("➕ Ajouter une question personnalisée")
with st.form("custom_form"):
    custom_text = st.text_area("Décris ton fantasme ou pratique précise :", 
                               placeholder="Ex : Se faire attacher les mains dans le dos et se faire utiliser pendant 20 minutes...")
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        custom_tag = st.selectbox("Catégorie", ["sensuel", "oral", "penetration", "anal", "bdsm", "hard", "extreme", "trois", "love", "jouet", "voyeur", "exhib", "facial", "tabou", "pegging", "roleplay"])
    with col_t2:
        custom_level = st.selectbox("Niveau", ["Soft", "Medium", "Hard", "Very Hard", "Extreme", "Variable"])
    
    if st.form_submit_button("Ajouter cette question"):
        if custom_text.strip():
            add_custom_question(user, custom_text.strip(), custom_tag, custom_level)
            st.success("✅ Question personnalisée ajoutée pour vous deux !")
            st.rerun()

# --- RESET ---
with st.expander("⚙️ Paramètres & Reset"):
    st.warning("Cette action effacera toutes les réponses et questions personnalisées.")
    if st.button("🔄 Reboot complet (effacer tout et recommencer)", type="secondary"):
        if st.checkbox("Je confirme que je veux tout supprimer"):
            reset_db()

st.caption("Amusez-vous bien ❤️🔥 – Jouez toujours avec consentement mutuel.")
