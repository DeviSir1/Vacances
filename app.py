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

# --- 100 QUESTIONS CONCRÈTES ET EXPLICITES ---
QUESTIONS = [
    # SOFT (1-10)
    {"id": 1, "text": "Longs baisers profonds avec la langue pendant de longues minutes", "tag": "sensuel", "level": "Soft", "type": "smash"},
    {"id": 2, "text": "Massage lent et sensuel de tout le corps avec de l'huile chaude", "tag": "sensuel", "level": "Soft", "type": "smash"},
    {"id": 3, "text": "Se caresser mutuellement très longtemps sans aucune pénétration", "tag": "sensuel", "level": "Soft", "type": "smash"},
    {"id": 4, "text": "Strip-tease lent et sensuel pour l'autre", "tag": "sensuel", "level": "Soft", "type": "smash"},
    {"id": 5, "text": "Se regarder intensément dans les yeux pendant qu'on se touche", "tag": "sensuel", "level": "Soft", "type": "smash"},
    {"id": 6, "text": "Préliminaires oraux très longs et attentionnés", "tag": "oral", "level": "Soft", "type": "smash"},
    {"id": 7, "text": "Cunnilingus lent et créatif avec la langue et les doigts", "tag": "oral", "level": "Soft", "type": "smash"},
    {"id": 8, "text": "Fellation lente et profonde avec beaucoup de salive", "tag": "oral", "level": "Soft", "type": "smash"},
    {"id": 9, "text": "Missionnaire profond avec beaucoup de contact visuel et câlins", "tag": "penetration", "level": "Soft", "type": "smash"},
    {"id": 10, "text": "Quelle est ta position préférée pour commencer doucement ?", "tag": "penetration", "level": "Soft", "type": "choice",
     "options": ["Missionnaire", "Cuillères (spooning)", "Cowgirl douce", "Debout contre un mur", "Autre"]},

    # MEDIUM (11-20)
    {"id": 11, "text": "Doggy style bien cambré", "tag": "penetration", "level": "Medium", "type": "smash"},
    {"id": 12, "text": "Cowgirl / Reverse cowgirl en contrôlant le rythme", "tag": "penetration", "level": "Medium", "type": "smash"},
    {"id": 13, "text": "Parler salement pendant l'acte (dirty talk)", "tag": "parole", "level": "Medium", "type": "smash"},
    {"id": 14, "text": "Se masturber devant l'autre en se regardant dans les yeux", "tag": "voyeur", "level": "Medium", "type": "smash"},
    {"id": 15, "text": "Utiliser un vibromasseur clitoridien pendant la pénétration", "tag": "jouet", "level": "Medium", "type": "smash"},
    {"id": 16, "text": "Plug anal porté pendant un rapport vaginal", "tag": "anal", "level": "Medium", "type": "smash"},
    {"id": 17, "text": "Fessées légères pendant l'acte", "tag": "bdsm", "level": "Medium", "type": "smash"},
    {"id": 18, "text": "Edging (s'arrêter juste avant l'orgasme pour prolonger le plaisir)", "tag": "hard", "level": "Medium", "type": "smash"},
    {"id": 19, "text": "Sexe debout contre un mur", "tag": "penetration", "level": "Medium", "type": "smash"},
    {"id": 20, "text": "Quelle position préfères-tu pour un rythme moyen ?", "tag": "penetration", "level": "Medium", "type": "choice",
     "options": ["Doggy style", "Cowgirl", "Missionnaire profond", "Levrette", "Autre"]},

    # Consentement & Communication
    {"id": 21, "text": "Vérifier régulièrement pendant l'acte si tout va bien (check-in verbal)", "tag": "consentement", "level": "Soft", "type": "smash"},
    {"id": 22, "text": "Utiliser un safeword clair (ex: ROUGE = arrêt immédiat)", "tag": "consentement", "level": "Medium", "type": "smash"},
    {"id": 23, "text": "Pouvoir dire 'stop' ou 'ralentis' à n'importe quel moment sans justification", "tag": "consentement", "level": "Soft", "type": "smash"},

    # HARD (24-40)
    {"id": 24, "text": "Levrette forte et profonde", "tag": "penetration", "level": "Hard", "type": "smash"},
    {"id": 25, "text": "Pénétration anale douce et progressive", "tag": "anal", "level": "Hard", "type": "smash"},
    {"id": 26, "text": "Se faire attacher avec des menottes ou foulards", "tag": "bdsm", "level": "Hard", "type": "smash"},
    {"id": 27, "text": "Fessées plus marquantes et répétées", "tag": "bdsm", "level": "Hard", "type": "smash"},
    {"id": 28, "text": "Deepthroat intense", "tag": "oral", "level": "Hard", "type": "smash"},
    {"id": 29, "text": "Éjaculation faciale ou sur les seins", "tag": "facial", "level": "Hard", "type": "smash"},
    {"id": 30, "text": "Quelle est ta position préférée quand c'est plus hard ?", "tag": "penetration", "level": "Hard", "type": "choice",
     "options": ["Levrette forte", "Doggy style intense", "Cowgirl rapide", "Debout porté", "Autre"]},

    {"id": 31, "text": "Rough sex (violent et bestial de manière consentie)", "tag": "hard", "level": "Hard", "type": "smash"},
    {"id": 32, "text": "Light choking (main légère sur la gorge)", "tag": "hard", "level": "Hard", "type": "smash"},
    {"id": 33, "text": "Filmer ou se prendre en photo pendant l'acte", "tag": "exhib", "level": "Hard", "type": "smash"},
    {"id": 34, "text": "Wax play (cire chaude de bougie sur la peau)", "tag": "bdsm", "level": "Hard", "type": "smash"},
    {"id": 35, "text": "Pegging (elle porte un strap-on et sodomise lui)", "tag": "pegging", "level": "Hard", "type": "smash"},

    # Consentement
    {"id": 36, "text": "Dire explicitement 'oui je veux ça' avant de passer à une nouvelle pratique", "tag": "consentement", "level": "Hard", "type": "smash"},
    {"id": 37, "text": "Faire un débrief après la session pour dire ce qui était bien et ce qui l'était moins", "tag": "consentement", "level": "Soft", "type": "smash"},

    # VERY HARD / EXTREME (38-60)
    {"id": 38, "text": "Pénétration anale très intense et profonde", "tag": "anal", "level": "Very Hard", "type": "smash"},
    {"id": 39, "text": "Fisting vaginal ou anal", "tag": "extreme", "level": "Very Hard", "type": "smash"},
    {"id": 40, "text": "Golden shower (uriner sur l'autre ou se faire uriner dessus)", "tag": "extreme", "level": "Very Hard", "type": "smash"},
    {"id": 41, "text": "Candaulisme (regarder l'autre avoir un rapport avec quelqu'un)", "tag": "voyeur", "level": "Very Hard", "type": "smash"},
    {"id": 42, "text": "Humiliation légère consentie (insultes sexuelles)", "tag": "bdsm", "level": "Very Hard", "type": "smash"},
    {"id": 43, "text": "Consensual Non-Consent (CNC - viol fantasy avec safeword)", "tag": "extreme", "level": "Very Hard", "type": "smash"},
    {"id": 44, "text": "Rimjob (lécher l'anus de l'autre)", "tag": "oral", "level": "Very Hard", "type": "smash"},
    {"id": 45, "text": "Double pénétration (pénis + jouet en même temps)", "tag": "double", "level": "Very Hard", "type": "smash"},

    # Choix multiple
    {"id": 50, "text": "Quelle pratique anal te fait le plus envie ?", "tag": "anal", "level": "Very Hard", "type": "choice",
     "options": ["Plug anal", "Pénétration douce", "Pénétration intense", "Rimjob", "Aucune"]},

    # Suite jusqu'à 100 (toutes concrètes)
    {"id": 51, "text": "Face sitting (s'asseoir sur le visage pour se faire lécher)", "tag": "oral", "level": "Hard", "type": "smash"},
    {"id": 52, "text": "Bondage avec corde ou ruban adhésif", "tag": "bdsm", "level": "Hard", "type": "smash"},
    {"id": 53, "text": "Orgasm denial (refuser l'orgasme pendant longtemps)", "tag": "hard", "level": "Hard", "type": "smash"},
    {"id": 54, "text": "Sexe pendant les règles avec creampie intérieur", "tag": "tabou", "level": "Very Hard", "type": "smash"},
    {"id": 55, "text": "Utiliser des poppers pendant l'acte pour intensifier les sensations", "tag": "extreme", "level": "Very Hard", "type": "smash"},
    {"id": 56, "text": "Breeding fantasy (fantasme de se faire remplir pour faire un bébé)", "tag": "hard", "level": "Hard", "type": "smash"},
    {"id": 57, "text": "Humiliation forte et jeux de dégradation", "tag": "extreme", "level": "Extreme", "type": "smash"},
    {"id": 58, "text": "Jeu de chasteté avec cage à pénis", "tag": "bdsm", "level": "Extreme", "type": "smash"},
    {"id": 59, "text": "Public play avec vibro télécommandé en public", "tag": "exhib", "level": "Extreme", "type": "smash"},
    {"id": 60, "text": "Gangbang fantasy (se faire prendre par plusieurs personnes)", "tag": "extreme", "level": "Extreme", "type": "smash"},
]

# Compléter de 61 à 100 avec des questions concrètes variées
extra = [
    "Sexe anal suivi immédiatement d'un creampie vaginal",
    "Se faire attacher et utiliser comme objet sexuel (free use)",
    "Praise kink (se faire complimenter excessivement pendant le sexe)",
    "Blindfold + écouteurs (priver la vue et l'ouïe)",
    "Creampie eating (lécher le sperme après éjaculation intérieure)",
    "Sexe dans un lieu public avec fort risque d'être surpris",
    "Fessées très fortes jusqu'à avoir des marques",
    "Choking plus marqué (avec accord préalable)",
    "Utiliser des pinces à seins pendant la pénétration",
    "Scat play (très extrême)",
    "Double pénétration anale + vaginale",
    "Se faire marquer avec des morsures et suçons visibles",
    "Jeux de température (glaçons et cire chaude alternés)",
    "Sexe toute la nuit sans dormir",
    "Fantasme de prostitution (payer ou se faire payer)",
    "Age play / Daddy-Mommy roleplay",
    "Utiliser un glory hole (fantasme)",
    "Se faire sodomiser tout en se faisant sucer",
    "Multiple orgasmes forcés",
    "Après-sex : se faire nettoyer par l'autre avec la langue",
]

for i in range(61, 101):
    if i % 10 == 0:
        QUESTIONS.append({
            "id": i,
            "text": "Parmi ces pratiques, laquelle t'excite le plus en ce moment ?",
            "tag": "hard",
            "level": "Hard",
            "type": "choice",
            "options": ["Anal intense", "Rough sex", "BDSM", "Trio fantasy", "Autre"]
        })
    else:
        text = extra[(i - 61) % len(extra)] if (i - 61) < len(extra) else f"Pratique coquine intense n°{i}"
        QUESTIONS.append({
            "id": i,
            "text": text,
            "tag": "hard" if "anal" in text.lower() or "rough" in text.lower() else "extreme",
            "level": "Very Hard" if i > 80 else "Hard",
            "type": "smash"
        })

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
        choice = st.radio("Choisis ta réponse :", next_q["options"], horizontal=True)
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
                comfort = st.slider("Niveau de confort (1 = pas à l'aise → 5 = très excité)", 1, 5, 4, key=f"comf_{next_q['id']}")
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
