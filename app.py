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
conn.commit()

# --- 100 QUESTIONS CONCRÈTES ET COHÉRENTES ---
QUESTIONS = [
    # SOFT 1-15
    {"id": 1, "text": "Longs baisers profonds avec la langue pendant de longues minutes", "tag": "sensuel", "level": "Soft", "type": "smash"},
    {"id": 2, "text": "Massage lent et sensuel de tout le corps avec de l'huile chaude", "tag": "sensuel", "level": "Soft", "type": "smash"},
    {"id": 3, "text": "Se caresser mutuellement très longtemps sans pénétration", "tag": "sensuel", "level": "Soft", "type": "smash"},
    {"id": 4, "text": "Strip-tease lent et sensuel pour l'autre", "tag": "sensuel", "level": "Soft", "type": "smash"},
    {"id": 5, "text": "Se regarder intensément dans les yeux pendant qu'on se touche", "tag": "sensuel", "level": "Soft", "type": "smash"},
    {"id": 6, "text": "Préliminaires oraux très longs et attentionnés", "tag": "oral", "level": "Soft", "type": "smash"},
    {"id": 7, "text": "Cunnilingus lent et créatif avec la langue", "tag": "oral", "level": "Soft", "type": "smash"},
    {"id": 8, "text": "Fellation lente et profonde avec beaucoup de salive", "tag": "oral", "level": "Soft", "type": "smash"},
    {"id": 9, "text": "Missionnaire profond avec beaucoup de contact visuel", "tag": "penetration", "level": "Soft", "type": "smash"},
    {"id": 10, "text": "Sexe en cuillères (spooning) très collé-serré et doux", "tag": "penetration", "level": "Soft", "type": "smash"},

    # Choix multiple 1
    {"id": 11, "text": "Quelle est ta position préférée pour commencer doucement ?", "tag": "penetration", "level": "Soft", "type": "choice",
     "options": ["Missionnaire", "Cuillères", "Cowgirl douce", "Debout", "Autre"]},

    {"id": 12, "text": "Sexe du matin au réveil encore à moitié endormi", "tag": "sensuel", "level": "Soft", "type": "smash"},
    {"id": 13, "text": "Se faire lécher partout (cou, seins, ventre, cuisses)", "tag": "oral", "level": "Soft", "type": "smash"},
    {"id": 14, "text": "69 très lent et sensuel", "tag": "oral", "level": "Soft", "type": "smash"},
    {"id": 15, "text": "Sexe dans la douche avec caresses sensuelles", "tag": "sensuel", "level": "Soft", "type": "smash"},

    # MEDIUM
    {"id": 16, "text": "Doggy style bien cambré", "tag": "penetration", "level": "Medium", "type": "smash"},
    {"id": 17, "text": "Cowgirl / Reverse cowgirl en contrôlant le rythme", "tag": "penetration", "level": "Medium", "type": "smash"},
    {"id": 18, "text": "Parler salement pendant l'acte (dirty talk)", "tag": "parole", "level": "Medium", "type": "smash"},
    {"id": 19, "text": "Se masturber devant l'autre en se regardant", "tag": "voyeur", "level": "Medium", "type": "smash"},
    {"id": 20, "text": "Utiliser un vibromasseur clitoridien pendant la pénétration", "tag": "jouet", "level": "Medium", "type": "smash"},

    # Choix multiple 2
    {"id": 21, "text": "Quelle position préfères-tu pour un rythme moyen ?", "tag": "penetration", "level": "Medium", "type": "choice",
     "options": ["Doggy style", "Cowgirl", "Missionnaire profond", "Levrette", "Autre"]},

    {"id": 22, "text": "Plug anal porté pendant un rapport vaginal", "tag": "anal", "level": "Medium", "type": "smash"},
    {"id": 23, "text": "Fessées légères pendant l'acte", "tag": "bdsm", "level": "Medium", "type": "smash"},
    {"id": 24, "text": "Edging (s'arrêter juste avant l'orgasme)", "tag": "hard", "level": "Medium", "type": "smash"},
    {"id": 25, "text": "Sexe debout contre un mur", "tag": "penetration", "level": "Medium", "type": "smash"},

    # Consentement léger
    {"id": 26, "text": "Vérifier régulièrement si tout va bien pendant l'acte", "tag": "consentement", "level": "Soft", "type": "smash"},
    {"id": 27, "text": "Utiliser un safeword clair (ROUGE = arrêt immédiat)", "tag": "consentement", "level": "Medium", "type": "smash"},

    # HARD
    {"id": 28, "text": "Levrette forte et profonde", "tag": "penetration", "level": "Hard", "type": "smash"},
    {"id": 29, "text": "Pénétration anale douce et progressive", "tag": "anal", "level": "Hard", "type": "smash"},
    {"id": 30, "text": "Se faire attacher avec des menottes ou foulards", "tag": "bdsm", "level": "Hard", "type": "smash"},
    {"id": 31, "text": "Fessées plus marquantes", "tag": "bdsm", "level": "Hard", "type": "smash"},
    {"id": 32, "text": "Deepthroat intense", "tag": "oral", "level": "Hard", "type": "smash"},
    {"id": 33, "text": "Éjaculation faciale ou sur les seins", "tag": "facial", "level": "Hard", "type": "smash"},
    {"id": 34, "text": "Rough sex (violent et bestial consentie)", "tag": "hard", "level": "Hard", "type": "smash"},
    {"id": 35, "text": "Light choking (main légère sur la gorge)", "tag": "hard", "level": "Hard", "type": "smash"},

    # Choix multiple 3
    {"id": 36, "text": "Quelle est ta position préférée quand c'est plus hard ?", "tag": "penetration", "level": "Hard", "type": "choice",
     "options": ["Levrette forte", "Doggy intense", "Cowgirl rapide", "Debout porté", "Autre"]},

    {"id": 37, "text": "Wax play (cire chaude sur la peau)", "tag": "bdsm", "level": "Hard", "type": "smash"},
    {"id": 38, "text": "Pegging (elle sodomise lui avec strap-on)", "tag": "pegging", "level": "Very Hard", "type": "smash"},
    {"id": 39, "text": "Rimjob (lécher l'anus)", "tag": "oral", "level": "Very Hard", "type": "smash"},
    {"id": 40, "text": "Double pénétration (pénis + jouet)", "tag": "double", "level": "Very Hard", "type": "smash"},

    # VERY HARD / EXTREME
    {"id": 41, "text": "Pénétration anale très intense et profonde", "tag": "anal", "level": "Very Hard", "type": "smash"},
    {"id": 42, "text": "Fisting vaginal ou anal", "tag": "extreme", "level": "Very Hard", "type": "smash"},
    {"id": 43, "text": "Golden shower (uriner sur l'autre)", "tag": "extreme", "level": "Very Hard", "type": "smash"},
    {"id": 44, "text": "Candaulisme (regarder l'autre avec quelqu'un)", "tag": "voyeur", "level": "Very Hard", "type": "smash"},
    {"id": 45, "text": "Humiliation légère consentie", "tag": "bdsm", "level": "Very Hard", "type": "smash"},
    {"id": 46, "text": "Consensual Non-Consent (CNC avec safeword)", "tag": "extreme", "level": "Very Hard", "type": "smash"},

    # Choix multiple 4
    {"id": 47, "text": "Quelle pratique anal te fait le plus envie ?", "tag": "anal", "level": "Very Hard", "type": "choice",
     "options": ["Plug anal", "Pénétration douce", "Pénétration intense", "Rimjob", "Aucune"]},

    {"id": 48, "text": "Se faire attacher et utiliser comme objet sexuel", "tag": "bdsm", "level": "Very Hard", "type": "smash"},
    {"id": 49, "text": "Sexe anal suivi d'un creampie vaginal", "tag": "tabou", "level": "Extreme", "type": "smash"},
    {"id": 50, "text": "Jeux de douleur plus forte (pinces, morsures)", "tag": "extreme", "level": "Very Hard", "type": "smash"},

    # Choix multiple 5 (plus léger)
    {"id": 51, "text": "Quelle est ta plus grande envie coquine du moment ?", "tag": "hard", "level": "Hard", "type": "choice",
     "options": ["Anal intense", "Rough sex", "BDSM", "Trio fantasy", "Filmer"]},

    # Suite variée jusqu'à 100
    {"id": 52, "text": "Face sitting (s'asseoir sur le visage)", "tag": "oral", "level": "Hard", "type": "smash"},
    {"id": 53, "text": "Bondage avec corde", "tag": "bdsm", "level": "Hard", "type": "smash"},
    {"id": 54, "text": "Orgasm denial (refuser l'orgasme longtemps)", "tag": "hard", "level": "Hard", "type": "smash"},
    {"id": 55, "text": "Breeding fantasy", "tag": "hard", "level": "Hard", "type": "smash"},
    {"id": 56, "text": "Sexe pendant les règles avec creampie", "tag": "tabou", "level": "Very Hard", "type": "smash"},
    {"id": 57, "text": "Utiliser des poppers pendant l'acte", "tag": "extreme", "level": "Very Hard", "type": "smash"},
    {"id": 58, "text": "Humiliation forte", "tag": "extreme", "level": "Extreme", "type": "smash"},
    {"id": 59, "text": "Jeu de chasteté avec cage à pénis", "tag": "bdsm", "level": "Extreme", "type": "smash"},
    {"id": 60, "text": "Public play avec vibro télécommandé", "tag": "exhib", "level": "Extreme", "type": "smash"},

    # Choix multiple 6
    {"id": 61, "text": "Quelle pratique te fait le plus fantasmer en ce moment ?", "tag": "hard", "level": "Hard", "type": "choice",
     "options": ["Pegging", "Golden shower", "Double pénétration", "Rough sex", "Autre"]},

    {"id": 62, "text": "Se faire marquer avec des morsures et suçons visibles", "tag": "bdsm", "level": "Hard", "type": "smash"},
    {"id": 63, "text": "Double pénétration anale + vaginale", "tag": "extreme", "level": "Extreme", "type": "smash"},
    {"id": 64, "text": "Se faire attacher les mains dans le dos et se faire utiliser", "tag": "bdsm", "level": "Very Hard", "type": "smash"},
    {"id": 65, "text": "Jeux de température (glaçons et cire chaude)", "tag": "sensuel", "level": "Hard", "type": "smash"},
    {"id": 66, "text": "Sexe toute la nuit sans dormir", "tag": "hard", "level": "Hard", "type": "smash"},
    {"id": 67, "text": "Fantasme de prostitution (payer ou se faire payer)", "tag": "roleplay", "level": "Very Hard", "type": "smash"},
    {"id": 68, "text": "Multiple orgasmes forcés", "tag": "hard", "level": "Very Hard", "type": "smash"},
    {"id": 69, "text": "Après l'orgasme : se faire nettoyer avec la langue", "tag": "tabou", "level": "Very Hard", "type": "smash"},
    {"id": 70, "text": "Choking plus marqué avec accord préalable", "tag": "hard", "level": "Very Hard", "type": "smash"},

    # Choix multiple 7 (léger)
    {"id": 71, "text": "Quelle est ta position préférée pour finir en beauté ?", "tag": "penetration", "level": "Hard", "type": "choice",
     "options": ["Missionnaire yeux dans les yeux", "Doggy style", "Cowgirl", "Cuillères", "Autre"]},

    {"id": 72, "text": "Se faire sodomiser tout en se faisant lécher", "tag": "double", "level": "Very Hard", "type": "smash"},
    {"id": 73, "text": "Utiliser un strap-on pour sodomiser son partenaire", "tag": "pegging", "level": "Very Hard", "type": "smash"},
    {"id": 74, "text": "Jeux d'humiliation forte (se faire traiter comme un objet)", "tag": "extreme", "level": "Extreme", "type": "smash"},
    {"id": 75, "text": "Fantasme de viol consensuel (CNC) très réaliste", "tag": "extreme", "level": "Extreme", "type": "smash"},
    {"id": 76, "text": "Se faire pisser dessus pendant le sexe", "tag": "extreme", "level": "Extreme", "type": "smash"},
    {"id": 77, "text": "Utiliser des pinces à seins pendant la pénétration", "tag": "bdsm", "level": "Hard", "type": "smash"},
    {"id": 78, "text": "Sexe violent et passionné avec tirage de cheveux", "tag": "hard", "level": "Hard", "type": "smash"},
    {"id": 79, "text": "Faire l'amour en écoutant une playlist très érotique", "tag": "sensuel", "level": "Medium", "type": "smash"},
    {"id": 80, "text": "Se faire bander les yeux et surprendre avec différentes sensations", "tag": "bdsm", "level": "Hard", "type": "smash"},

    # Choix multiple 8
    {"id": 81, "text": "Quelle est ta plus grande envie coquine actuelle ?", "tag": "hard", "level": "Hard", "type": "choice",
     "options": ["Anal", "BDSM", "Rough sex", "Trio fantasy", "Filmer"]},

    {"id": 82, "text": "Se faire attacher et bander les yeux pendant plusieurs heures", "tag": "bdsm", "level": "Very Hard", "type": "smash"},
    {"id": 83, "text": "Jeux de respiration contrôlée (breath play)", "tag": "extreme", "level": "Extreme", "type": "smash"},
    {"id": 84, "text": "Fantasme de gangbang", "tag": "extreme", "level": "Extreme", "type": "smash"},
    {"id": 85, "text": "Se faire marquer avec des morsures très visibles", "tag": "bdsm", "level": "Hard", "type": "smash"},
    {"id": 86, "text": "Utiliser des poppers pendant une pénétration anale intense", "tag": "extreme", "level": "Very Hard", "type": "smash"},
    {"id": 87, "text": "Multiple orgasmes jusqu'à supplier d'arrêter", "tag": "hard", "level": "Very Hard", "type": "smash"},
    {"id": 88, "text": "Sexe dans la nature (forêt ou plage)", "tag": "exhib", "level": "Hard", "type": "smash"},
    {"id": 89, "text": "Faire un slow sensuel nu dans le salon", "tag": "sensuel", "level": "Soft", "type": "smash"},
    {"id": 90, "text": "Après le sexe : longs câlins et caresses tendres", "tag": "love", "level": "Soft", "type": "smash"},

    # Choix multiple 9 (léger et positif)
    {"id": 91, "text": "Quelle est ta plus belle envie pour vos prochaines sessions ?", "tag": "love", "level": "Soft", "type": "choice",
     "options": ["Plus de tendresse", "Plus de rough", "Plus d'anal", "Plus de jeux", "Plus de roleplay"]},

    {"id": 92, "text": "Se faire lécher après avoir joui", "tag": "tabou", "level": "Very Hard", "type": "smash"},
    {"id": 93, "text": "Utiliser un cockring pour prolonger le plaisir", "tag": "jouet", "level": "Medium", "type": "smash"},
    {"id": 94, "text": "Danser nu collé-serré avant de passer à l'acte", "tag": "sensuel", "level": "Soft", "type": "smash"},
    {"id": 95, "text": "Faire un massage érotique mutuel complet", "tag": "sensuel", "level": "Soft", "type": "smash"},
    {"id": 96, "text": "Se confier ses fantasmes les plus secrets pendant l'acte", "tag": "parole", "level": "Medium", "type": "smash"},
    {"id": 97, "text": "Essayer un nouveau jouet acheté ensemble", "tag": "jouet", "level": "Medium", "type": "smash"},
    {"id": 98, "text": "Faire l'amour en regardant un film porno ensemble", "tag": "voyeur", "level": "Medium", "type": "smash"},
    {"id": 99, "text": "Organiser une soirée entière dédiée au plaisir de l'autre", "tag": "love", "level": "Soft", "type": "smash"},
    {"id": 100, "text": "Tout ce que tu veux du moment que c'est avec toi et en plein consentement", "tag": "love", "level": "Soft", "type": "smash"},
]

# --- FONCTIONS ---
def load_all_questions():
    c.execute("SELECT id, text, tag, level FROM custom_questions")
    custom = [{"id": row[0] + 1000, "text": row[1], "tag": row[2], "level": row[3], "type": "smash"} for row in c.fetchall()]
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

def reset_db():
    c.execute("DELETE FROM answers")
    conn.commit()
    st.success("✅ Tout a été réinitialisé avec succès !")
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
    st.caption(f"Question {answered_count + 1} / 100 — **{next_q.get('level', 'Variable')}**")

    st.markdown(f"""
    <div style='background:#2a2a3a; padding:30px; border-radius:15px; text-align:center; border:2px solid #ff4d94; margin:20px 0;'>
        <h3 style='color:#ff99cc;'>{next_q['text']}</h3>
    </div>
    """, unsafe_allow_html=True)

    if next_q.get("type") == "choice":
        choice = st.radio("Choisis ta réponse :", next_q.get("options", []), horizontal=True)
        if st.button("Valider ce choix", type="primary", use_container_width=True):
            save_answer(user, next_q["id"], choice)
            st.rerun()
    else:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("❌ PASS", use_container_width=True):
                save_answer(user, next_q["id"], "pass")
                st.rerun()
        with col2:
            if st.button("❤️ SMASH", type="primary", use_container_width=True):
                comfort = st.slider("Niveau de confort (1-5)", 1, 5, 4, key=f"comf_{next_q['id']}")
                save_answer(user, next_q["id"], "smash", comfort)
                st.success("Smash enregistré !")
                st.rerun()

else:
    st.success(f"🎉 Bravo {user} ! Tu as terminé les 100 questions.")

# --- RÉSULTATS ---
st.write("---")
st.subheader("🔥 Nos Matchs Coquins")

matches = get_matches()

if not matches:
    st.info("Pas encore de smash commun.")
else:
    st.success(f"**{len(matches)} fantasmes validés à deux !**")
    tag_count = defaultdict(int)
    for m in matches:
        tag_count[m["tag"]] += 1
    for tag, count in sorted(tag_count.items(), key=lambda x: x[1], reverse=True):
        st.progress(count / max(len(matches), 1))
        st.caption(f"**{tag.capitalize()}** : {count} smash")

# --- RESET ---
with st.expander("⚙️ Paramètres & Reset"):
    st.warning("⚠️ Cette action va supprimer TOUTES les réponses.")
    confirm = st.checkbox("Je confirme que je veux tout supprimer et recommencer à zéro", key="reset_confirm")
    if st.button("🔄 Reboot complet – Tout effacer", type="secondary", use_container_width=True):
        if confirm:
            reset_db()
        else:
            st.error("❌ Coche la case pour confirmer.")

st.caption("Jouez toujours avec un consentement clair, enthousiaste et révocable à tout moment ❤️🔥")
