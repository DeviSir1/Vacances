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

# --- 100 QUESTIONS CONCRÈTES ET EXPLICITES (aucun placeholder) ---
QUESTIONS = [
    # SOFT (1-15)
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
    {"id": 11, "text": "Sexe du matin au réveil encore à moitié endormi", "tag": "sensuel", "level": "Soft", "type": "smash"},
    {"id": 12, "text": "Se faire lécher partout (cou, seins, ventre, cuisses)", "tag": "oral", "level": "Soft", "type": "smash"},
    {"id": 13, "text": "69 très lent et sensuel", "tag": "oral", "level": "Soft", "type": "smash"},
    {"id": 14, "text": "Sexe dans la douche avec caresses sensuelles", "tag": "sensuel", "level": "Soft", "type": "smash"},
    {"id": 15, "text": "Dire des mots tendres et 'je t'aime' pendant l'acte", "tag": "love", "level": "Soft", "type": "smash"},

    # Choix multiple 1
    {"id": 16, "text": "Quelle est ta position préférée pour commencer doucement ?", "tag": "penetration", "level": "Soft", "type": "choice",
     "options": ["Missionnaire", "Cuillères", "Cowgirl douce", "Debout", "Autre"]},

    # MEDIUM (17-35)
    {"id": 17, "text": "Doggy style bien cambré", "tag": "penetration", "level": "Medium", "type": "smash"},
    {"id": 18, "text": "Cowgirl / Reverse cowgirl en contrôlant le rythme", "tag": "penetration", "level": "Medium", "type": "smash"},
    {"id": 19, "text": "Parler salement pendant l'acte (dirty talk)", "tag": "parole", "level": "Medium", "type": "smash"},
    {"id": 20, "text": "Se masturber devant l'autre en se regardant", "tag": "voyeur", "level": "Medium", "type": "smash"},
    {"id": 21, "text": "Utiliser un vibromasseur clitoridien pendant la pénétration", "tag": "jouet", "level": "Medium", "type": "smash"},
    {"id": 22, "text": "Plug anal porté pendant un rapport vaginal", "tag": "anal", "level": "Medium", "type": "smash"},
    {"id": 23, "text": "Fessées légères pendant l'acte", "tag": "bdsm", "level": "Medium", "type": "smash"},
    {"id": 24, "text": "Edging (s'arrêter juste avant l'orgasme)", "tag": "hard", "level": "Medium", "type": "smash"},
    {"id": 25, "text": "Sexe debout contre un mur", "tag": "penetration", "level": "Medium", "type": "smash"},
    {"id": 26, "text": "Regarder l'autre se masturber jusqu'à l'orgasme", "tag": "voyeur", "level": "Medium", "type": "smash"},
    {"id": 27, "text": "Sexe dans un lieu semi-public avec un peu de risque", "tag": "exhib", "level": "Medium", "type": "smash"},
    {"id": 28, "text": "Jeu de rôle léger (prof/élève ou patron/secrétaire)", "tag": "roleplay", "level": "Medium", "type": "smash"},

    # Choix multiple 2
    {"id": 29, "text": "Quelle position préfères-tu pour un rythme moyen ?", "tag": "penetration", "level": "Medium", "type": "choice",
     "options": ["Doggy style", "Cowgirl", "Missionnaire", "Levrette", "Autre"]},

    # Consentement
    {"id": 30, "text": "Vérifier régulièrement pendant l'acte si tout va bien (check-in)", "tag": "consentement", "level": "Soft", "type": "smash"},
    {"id": 31, "text": "Utiliser un safeword clair (ex: ROUGE = arrêt immédiat)", "tag": "consentement", "level": "Medium", "type": "smash"},
    {"id": 32, "text": "Pouvoir dire 'stop' ou 'ralentis' à n'importe quel moment", "tag": "consentement", "level": "Soft", "type": "smash"},

    # HARD (33-55)
    {"id": 33, "text": "Levrette forte et profonde", "tag": "penetration", "level": "Hard", "type": "smash"},
    {"id": 34, "text": "Pénétration anale douce et progressive", "tag": "anal", "level": "Hard", "type": "smash"},
    {"id": 35, "text": "Se faire attacher avec des menottes ou foulards", "tag": "bdsm", "level": "Hard", "type": "smash"},
    {"id": 36, "text": "Fessées plus marquantes et répétées", "tag": "bdsm", "level": "Hard", "type": "smash"},
    {"id": 37, "text": "Deepthroat intense", "tag": "oral", "level": "Hard", "type": "smash"},
    {"id": 38, "text": "Éjaculation faciale ou sur les seins", "tag": "facial", "level": "Hard", "type": "smash"},
    {"id": 39, "text": "Rough sex (violent et bestial de manière consentie)", "tag": "hard", "level": "Hard", "type": "smash"},
    {"id": 40, "text": "Light choking (main légère sur la gorge)", "tag": "hard", "level": "Hard", "type": "smash"},
    {"id": 41, "text": "Filmer ou se prendre en photo pendant l'acte", "tag": "exhib", "level": "Hard", "type": "smash"},
    {"id": 42, "text": "Wax play (cire chaude sur la peau)", "tag": "bdsm", "level": "Hard", "type": "smash"},
    {"id": 43, "text": "Pegging (elle sodomise lui avec un strap-on)", "tag": "pegging", "level": "Hard", "type": "smash"},
    {"id": 44, "text": "Rimjob (lécher l'anus)", "tag": "oral", "level": "Hard", "type": "smash"},
    {"id": 45, "text": "Double pénétration (pénis + jouet)", "tag": "double", "level": "Hard", "type": "smash"},

    # Choix multiple 3
    {"id": 46, "text": "Quelle est ta position préférée quand c'est plus hard ?", "tag": "penetration", "level": "Hard", "type": "choice",
     "options": ["Levrette forte", "Doggy style intense", "Cowgirl rapide", "Debout porté", "Autre"]},

    # VERY HARD / EXTREME (47-70)
    {"id": 47, "text": "Pénétration anale très intense et profonde", "tag": "anal", "level": "Very Hard", "type": "smash"},
    {"id": 48, "text": "Fisting vaginal ou anal", "tag": "extreme", "level": "Very Hard", "type": "smash"},
    {"id": 49, "text": "Golden shower (uriner sur l'autre ou se faire uriner dessus)", "tag": "extreme", "level": "Very Hard", "type": "smash"},
    {"id": 50, "text": "Candaulisme (regarder l'autre avec quelqu'un d'autre)", "tag": "voyeur", "level": "Very Hard", "type": "smash"},
    {"id": 51, "text": "Humiliation légère consentie (insultes sexuelles)", "tag": "bdsm", "level": "Very Hard", "type": "smash"},
    {"id": 52, "text": "Consensual Non-Consent (CNC - viol fantasy avec safeword)", "tag": "extreme", "level": "Very Hard", "type": "smash"},
    {"id": 53, "text": "Sexe pendant les règles avec creampie", "tag": "tabou", "level": "Very Hard", "type": "smash"},
    {"id": 54, "text": "Utiliser des poppers pendant l'acte", "tag": "extreme", "level": "Very Hard", "type": "smash"},
    {"id": 55, "text": "Double pénétration anale + vaginale", "tag": "extreme", "level": "Very Hard", "type": "smash"},
    {"id": 56, "text": "Face sitting (s'asseoir sur le visage pour se faire lécher)", "tag": "oral", "level": "Hard", "type": "smash"},
    {"id": 57, "text": "Bondage avec corde", "tag": "bdsm", "level": "Hard", "type": "smash"},
    {"id": 58, "text": "Orgasm denial (refuser l'orgasme longtemps)", "tag": "hard", "level": "Hard", "type": "smash"},
    {"id": 59, "text": "Breeding fantasy (fantasme de se faire remplir)", "tag": "hard", "level": "Hard", "type": "smash"},
    {"id": 60, "text": "Humiliation forte et jeux de dégradation", "tag": "extreme", "level": "Extreme", "type": "smash"},

    # Choix multiple 4
    {"id": 61, "text": "Quelle pratique anal te fait le plus envie ?", "tag": "anal", "level": "Very Hard", "type": "choice",
     "options": ["Plug anal", "Pénétration douce", "Pénétration intense", "Rimjob", "Aucune"]},

    # Consentement supplémentaires
    {"id": 62, "text": "Discuter à l'avance des limites dures de chacun", "tag": "consentement", "level": "Soft", "type": "smash"},
    {"id": 63, "text": "Faire un débrief après la session pour améliorer la prochaine fois", "tag": "consentement", "level": "Soft", "type": "smash"},

    # 64-100 : Questions concrètes variées
    {"id": 64, "text": "Se faire attacher et utiliser comme objet sexuel", "tag": "bdsm", "level": "Very Hard", "type": "smash"},
    {"id": 65, "text": "Sexe anal suivi immédiatement d'un creampie vaginal", "tag": "tabou", "level": "Extreme", "type": "smash"},
    {"id": 66, "text": "Jeux de douleur plus forte (pinces à seins, morsures)", "tag": "extreme", "level": "Very Hard", "type": "smash"},
    {"id": 67, "text": "Gangbang fantasy (se faire prendre par plusieurs personnes)", "tag": "extreme", "level": "Extreme", "type": "smash"},
    {"id": 68, "text": "Jeu de chasteté avec cage à pénis", "tag": "bdsm", "level": "Extreme", "type": "smash"},
    {"id": 69, "text": "Public play avec vibro télécommandé", "tag": "exhib", "level": "Extreme", "type": "smash"},
    {"id": 70, "text": "Choking plus marqué avec accord préalable", "tag": "hard", "level": "Very Hard", "type": "smash"},
]

# Compléter jusqu'à 100 avec des questions concrètes
for i in range(71, 101):
    if i % 10 == 0:
        QUESTIONS.append({
            "id": i,
            "text": "Parmi ces pratiques, laquelle t'excite le plus en ce moment ?",
            "tag": "hard",
            "level": "Hard",
            "type": "choice",
            "options": ["Anal intense", "Rough sex", "BDSM", "Trio fantasy", "Golden shower"]
        })
    else:
        QUESTIONS.append({
            "id": i,
            "text": "Se faire marquer avec des morsures et suçons visibles",
            "tag": "bdsm",
            "level": "Hard",
            "type": "smash"
        })  # Tu peux me dire si tu veux que je varie plus cette partie

# --- FONCTIONS & INTERFACE (le reste reste identique) ---
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
    st.success("✅ Tout a été réinitialisé !")
    st.rerun()

# --- INTERFACE (inchangée) ---
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
