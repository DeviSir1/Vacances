import streamlit as st
import sqlite3

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Smash or Pass - Été 2026", page_icon="☀️", layout="centered")

# --- BASE DE DONNÉES SQLITE ---
conn = sqlite3.connect("vacances_famille.db", check_same_thread=False)
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS answers (
        user TEXT,
        question_id INTEGER,
        answer TEXT,
        PRIMARY KEY (user, question_id)
    )
''')
conn.commit()

# --- LA SUPER-BANQUE DE 100 QUESTIONS ---
QUESTIONS = [
    # Ambiance / Climat (1-10)
    {"id": 1, "text": "Fuir la canicule : la fraîcheur des nuits est non-négociable pour le bien-être d'Eliott ❄️", "tag": "alpes"},
    {"id": 2, "text": "La chaleur ne me fait pas peur du tout si on a une piscine à disposition ☀️", "tag": "sud"},
    {"id": 3, "text": "L'odeur des pins, le chant des cigales et un petit vent sec 🌲", "tag": "sud"},
    {"id": 4, "text": "L'air vif du matin à la montagne et les cloches des vaches au loin 🐄", "tag": "alpes"},
    {"id": 5, "text": "L'air iodé de l'océan avec une belle brise pour ne pas transpirer 🌬️", "tag": "mer"},
    {"id": 6, "text": "Se réveiller avec la vue sur une vallée verdoyante recouverte de brume matinale 🌫️", "tag": "perigord"},
    {"id": 7, "text": "L'humidité ne me dérange pas si le paysage est dingue 🌿", "tag": "nature"},
    {"id": 8, "text": "Il me faut du grand soleil tous les jours, c'est l'essence des vacances d'été ! 🌞", "tag": "sud"},
    {"id": 9, "text": "Un climat tempéré, quitte à avoir un jour ou deux de pluie pour rafraîchir l'atmosphère 🌦️", "tag": "alpes"},
    {"id": 10, "text": "Bronzer intensément au bord de l'eau 🍅", "tag": "sud"},

    # Logement et Logistique (11-25)
    {"id": 11, "text": "Un appartement douillet en station, bien équipé et super bien placé 🏔️", "tag": "alpes"},
    {"id": 12, "text": "Une vieille maison en pierre authentique avec un grand terrain 🏡", "tag": "perigord"},
    {"id": 13, "text": "Trouver une pharmacie à 5 minutes pour ne pas avoir à stocker 10 boîtes de lait Biostime dans le coffre 🍼", "tag": "pratique"},
    {"id": 14, "text": "Un logement isolé dans la pampa, même s'il faut faire 15 min de voiture pour le pain 🚗", "tag": "calme"},
    {"id": 15, "text": "Laverie ou machine à laver impérative dans la loc, avec un bébé et un 4 ans, c'est la survie 🧺", "tag": "pratique"},
    {"id": 16, "text": "Avoir une baignoire dans la location pour faciliter le bain des garçons 🛁", "tag": "pratique"},
    {"id": 17, "text": "Une location avec un extérieur bien clos pour que Samuel puisse courir sans aucun danger 🏡", "tag": "pratique"},
    {"id": 18, "text": "Un logement où je peux tout faire à pied ou en poussette (boulangerie, balade, resto) 🚶‍♂️", "tag": "pratique"},
    {"id": 19, "text": "Privilégier un trajet de nuit pour que les enfants dorment dans la voiture et arriver frais 🚗💤", "tag": "pratique"},
    {"id": 20, "text": "Louer un mobil-home tout confort dans un camping 4 étoiles ⛺", "tag": "social"},
    {"id": 21, "text": "Zéro camping, on veut du dur : appartement ou vraie maison 🧱", "tag": "calme"},
    {"id": 22, "text": "Avoir une chambre séparée pour Samuel pour qu'il ait son espace (et nous notre intimité !) 🛏️", "tag": "pratique"},
    {"id": 23, "text": "Une location avec la clim, c'est indispensable avec un nourrisson ❄️", "tag": "pratique"},
    {"id": 24, "text": "Faire péter le budget pour avoir une vue exceptionnelle depuis la terrasse 🌅", "tag": "budget_max"},
    {"id": 25, "text": "Avoir Netflix/Disney+ sur la télé de la loc pour gérer un temps calme en fin de journée 📺", "tag": "pratique"},

    # Nourriture et Budget (26-38)
    {"id": 26, "text": "Tartiflette d'été, bonne charcuterie locale et fromage fondu 🧀", "tag": "alpes"},
    {"id": 27, "text": "Magret de canard, foie gras, pommes sarladaises et bon vin rouge 🦆", "tag": "perigord"},
    {"id": 28, "text": "Acheter le poisson frais du matin au port pour le cuisiner le midi 🐟", "tag": "mer"},
    {"id": 29, "text": "Faire un barbecue le soir pendant que les enfants jouent dans le jardin 🌭", "tag": "chill"},
    {"id": 30, "text": "Cuisiner le moins possible : on fait péter le budget resto ou traiteur ! 🍽️", "tag": "budget_max"},
    {"id": 31, "text": "Gérer la majorité des repas nous-mêmes avec de bons produits du marché local 🧺", "tag": "budget_eco"},
    {"id": 32, "text": "Manger d'énormes glaces artisanales ou des crêpes au goûter presque tous les jours 🍦", "tag": "budget_max"},
    {"id": 33, "text": "Tester au moins un resto semi-gastronomique de la région, juste pour le kiff 🍽️", "tag": "budget_max"},
    {"id": 34, "text": "S'acheter une très bonne bouteille de vin local à déguster tranquillement 🥂", "tag": "oleole"},
    {"id": 35, "text": "Un petit dej ultra copieux avec des viennoiseries fraîches de la boulangerie tous les matins 🥐", "tag": "budget_max"},
    {"id": 36, "text": "Organiser un apéro dinatoire qui dure de 19h à 22h au lieu d'un repas classique 🥖🧀", "tag": "chill"},
    {"id": 37, "text": "Des vacances avec un budget maîtrisé : on privilégie les balades gratuites et les pique-niques 🥪", "tag": "budget_eco"},
    {"id": 38, "text": "Ramener plein de pots de miel, de fromages ou de vins dans le coffre au retour 🍯", "tag": "budget_max"},

    # Activités Enfants (39-55)
    {"id": 39, "text": "Exploration de châteaux forts avec une épée en bois pour notre petit chevalier Samuel 🏰", "tag": "perigord"},
    {"id": 40, "text": "Chasse aux marmottes avec de petites jumelles 🔭", "tag": "alpes"},
    {"id": 41, "text": "Visite d'une ferme pédagogique (traite des vaches, caresser les lapins, nourrir les chèvres) 🐇", "tag": "nature"},
    {"id": 42, "text": "Structure gonflable et pataugeoire dans une grande base de loisirs de montagne 🎈", "tag": "alpes"},
    {"id": 43, "text": "Descente en gabarre très calme sur la rivière (zéro secousse pour bébé Eliott) 🚣", "tag": "perigord"},
    {"id": 44, "text": "Grottes préhistoriques (idéal car il y fait toujours 13 degrés, parfait pour fuir la chaleur !) 🦇", "tag": "perigord"},
    {"id": 45, "text": "Un petit tour de manège en fin de journée pour la plus grande joie de Samuel 🎠", "tag": "activite"},
    {"id": 46, "text": "Passer l'après-midi dans un parc aquatique avec des toboggans et des jeux d'eau 💦", "tag": "activite"},
    {"id": 47, "text": "Faire du pédalo sur un lac avec Eliott bien à l'ombre sous le parasol de l'embarcation 🚣‍♂️", "tag": "alpes"},
    {"id": 48, "text": "Faire des châteaux de sable géants sur la plage (même si on en met plein la voiture après) 🏖️", "tag": "mer"},
    {"id": 49, "text": "Se faire une session accrobranche pour les tout-petits avec Samuel 🐒", "tag": "activite"},
    {"id": 50, "text": "Prendre un télécabine tous ensemble juste pour le fun et la vue panoramique 🚠", "tag": "alpes"},
    {"id": 51, "text": "Aller voir un grand aquarium marin ou d'eau douce 🐠", "tag": "activite"},
    {"id": 52, "text": "Partir à la chasse aux insectes ou chercher les plus beaux cailloux avec le grand frère 🦋", "tag": "nature"},
    {"id": 53, "text": "Faire une bataille d'eau improvisée en famille dans le jardin 🔫", "tag": "activite"},
    {"id": 54, "text": "Rencontrer d'autres familles pour que Samuel puisse se faire des copains de vacances 👫", "tag": "social"},
    {"id": 55, "text": "Des pistes cyclables plates et sécurisées pour louer des vélos avec une carriole pour les enfants 🚲", "tag": "pratique"},

    # Olé Olé / Couple / Détente (56-75)
    {"id": 56, "text": "Sieste crapuleuse climatisée pendant que Samuel fait un temps calme devant un film 🔥", "tag": "oleole"},
    {"id": 57, "text": "Bain de minuit tous nus dans la piscine de la loc (babyphone posé au bord !) 🔞", "tag": "oleole"},
    {"id": 58, "text": "Apéro saucisson/vin rouge en amoureux sur le balcon une fois les garçons couchés 🍷", "tag": "alpes"},
    {"id": 59, "text": "Dîner aux chandelles dans le jardin pendant que les deux dorment profondément ✨", "tag": "oleole"},
    {"id": 60, "text": "Jouer à des jeux de société (ou des jeux coquins) en amoureux avec un bon verre une fois la nuit tombée 🎲", "tag": "oleole"},
    {"id": 61, "text": "Prendre un baby-sitter local pour une soirée resto rien que tous les deux 🕯️", "tag": "oleole"},
    {"id": 62, "text": "Avoir un grand lit double bien confortable (minimum 160) pour pouvoir s'étaler la nuit 🛌", "tag": "oleole"},
    {"id": 63, "text": "S'embrasser passionnément sous un coucher de soleil de carte postale 🌅💋", "tag": "oleole"},
    {"id": 64, "text": "Mettre de la musique douce et danser un slow dans le salon en chaussettes 🎵", "tag": "oleole"},
    {"id": 65, "text": "S'autoriser une grasse matinée chacun son tour (l'autre gère les biberons et les réveils) ⏰", "tag": "chill"},
    {"id": 66, "text": "Prendre chacun son tour 2 heures 'off' en solo pour souffler, lire ou marcher 🧘", "tag": "chill"},
    {"id": 67, "text": "S'offrir un massage ou un spa pendant que l'autre gère la tribu 💆", "tag": "chill"},
    {"id": 68, "text": "Des vacances au ralenti : sieste, bouquin, piscine, et c'est absolument tout 😴", "tag": "chill"},
    {"id": 69, "text": "S'asseoir sur un banc en bord de mer et refaire le monde en regardant les passants 💭", "tag": "chill"},
    {"id": 70, "text": "Faire la sieste tous les 4 en même temps dans la même pièce pour un gros câlin familial 😴", "tag": "love"},
    {"id": 71, "text": "Rien à faire du sport, les vacances c'est fait pour faire du gras et se détendre ! 🍕", "tag": "chill"},
    {"id": 72, "text": "Pas de programme le matin, on décide au réveil selon notre humeur et celle des garçons 🤷‍♂️", "tag": "chill"},
    {"id": 73, "text": "Des vacances où l'on est dans notre bulle familiale, sans chercher à sociabiliser avec d'autres 🫧", "tag": "calme"},
    {"id": 74, "text": "Dormir avec la fenêtre ouverte pour écouter le silence de la nature (grillons, chouettes...) 🦉", "tag": "nature"},
    {"id": 75, "text": "Peu importe où l'on va, du moment qu'on profite de se retrouver tous les quatre ❤️", "tag": "love"},

    # Divers Nature / Sport / Découvertes (76-100)
    {"id": 76, "text": "Des chemins plats et goudronnés pour rouler en poussette sans effort avec Eliott 👶", "tag": "pratique"},
    {"id": 77, "text": "Les chemins escarpés ne me gênent pas, on gère les balades en porte-bébé ! 🎒", "tag": "sportif"},
    {"id": 78, "text": "Des vacances hyper actives : on bouge et on visite tous les jours ! 🏃‍♂️", "tag": "sportif"},
    {"id": 79, "text": "Flâner dans un marché de producteurs nocturne avec de la musique en live 🎶", "tag": "perigord"},
    {"id": 80, "text": "Des paysages grandioses et vertigineux à photographier 📸", "tag": "alpes"},
    {"id": 81, "text": "De douces collines verdoyantes, des vignes et des petits villages classés 'Plus beaux villages de France' 🏘️", "tag": "perigord"},
    {"id": 82, "text": "Se baigner dans un lac naturel d'eau douce et transparente 💧", "tag": "alpes"},
    {"id": 83, "text": "Se baigner dans une rivière sauvage (en trouvant un coin sans courant pour tremper les pieds) 🌊", "tag": "perigord"},
    {"id": 84, "text": "Se baigner dans l'océan Atlantique et affronter les vagues 🏄‍♂️", "tag": "mer"},
    {"id": 85, "text": "Préférer la mer Méditerranée pour avoir une eau à 27 degrés minimum 🏖️", "tag": "sud"},
    {"id": 86, "text": "Faire une mini rando nocturne (ou au crépuscule) pour regarder les étoiles 🌟", "tag": "nature"},
    {"id": 87, "text": "Trouver des sentiers bien ombragés en forêt pour les balades de l'après-midi 🌳", "tag": "nature"},
    {"id": 88, "text": "Louer un petit bateau sans permis pour une mini croisière de 2 heures 🚤", "tag": "activite"},
    {"id": 89, "text": "Une journée pique-nique dans l'herbe avec la grande couverture familiale 🥪", "tag": "chill"},
    {"id": 90, "text": "Essayer de faire un petit footing matinal pendant que l'autre garde les enfants 🏃‍♀️", "tag": "sportif"},
    {"id": 91, "text": "Faire du vélo sur une piste cyclable aménagée directement au bord de l'eau 🚲", "tag": "mer"},
    {"id": 92, "text": "Prendre de superbes photos de famille par un photographe pro dans la région 📸", "tag": "activite"},
    {"id": 93, "text": "Avoir du réseau 4G/5G ou un très bon Wifi (impossible de déconnecter à 100%) 📱", "tag": "pratique"},
    {"id": 94, "text": "Zone blanche acceptée : on coupe les téléphones, c'est de la vraie déconnexion ! 📵", "tag": "calme"},
    {"id": 95, "text": "Faire le moins d'heures de route possible depuis la maison pour ne pas ruiner le premier jour 🛣️", "tag": "pratique"},
    {"id": 96, "text": "Une destination chargée d'Histoire (musées, ruines, châteaux) 🏺", "tag": "perigord"},
    {"id": 97, "text": "S'acheter de beaux vêtements ou accessoires d'été sur un petit marché artisanal 👗", "tag": "sud"},
    {"id": 98, "text": "Faire un concours de celui qui saute le mieux dans la piscine 🏊‍♂️", "tag": "activite"},
    {"id": 99, "text": "Des vacances avec un vrai planning d'activités bien ficelé à l'avance pour ne rien rater 📅", "tag": "sportif"},
    {"id": 100, "text": "Ramasser des coquillages le matin de bonne heure sur le sable 🐚", "tag": "mer"}
]

# --- FONCTIONS UTILITAIRES ---
def save_answer(user, q_id, answer):
    c.execute("REPLACE INTO answers (user, question_id, answer) VALUES (?, ?, ?)", (user, q_id, answer))
    conn.commit()

def get_user_answers(user):
    c.execute("SELECT question_id, answer FROM answers WHERE user=?", (user,))
    return {row[0]: row[1] for row in c.fetchall()}

def get_matches():
    c.execute('''
        SELECT a1.question_id 
        FROM answers a1 
        JOIN answers a2 ON a1.question_id = a2.question_id 
        WHERE a1.user = 'Julien' AND a2.user = 'Lydie' 
        AND a1.answer = 'smash' AND a2.answer = 'smash'
    ''')
    matched_ids = [row[0] for row in c.fetchall()]
    return [q for q in QUESTIONS if q["id"] in matched_ids]

def reset_db():
    c.execute("DELETE FROM answers")
    conn.commit()

# --- INTERFACE UTILISATEUR ---
st.title("☀️ Smash or Pass - Nos Vacances")

# Sélection de l'utilisateur
st.markdown("### Qui tient le téléphone ? 📱")
user = st.radio("Sélectionnez votre profil :", ["Julien", "Lydie"], horizontal=True, label_visibility="collapsed")
st.write("---")

# Récupération des réponses
user_answers = get_user_answers(user)
answered_count = len(user_answers)

# Trouver la prochaine question
next_q = next((q for q in QUESTIONS if q["id"] not in user_answers), None)

# --- ZONE DE JEU ---
if next_q:
    progress_val = answered_count / len(QUESTIONS)
    st.progress(progress_val)
    st.caption(f"Question {answered_count + 1} sur {len(QUESTIONS)}")
    
    # Carte Question
    st.markdown(
        f"""
        <div style='background-color: white; padding: 30px; border-radius: 15px; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center; border: 1px solid #ddd; margin-bottom: 20px;'>
            <h3 style='color: #2c3e50; margin: 0;'>{next_q['text']}</h3>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # Boutons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("❌ PASS", use_container_width=True):
            save_answer(user, next_q["id"], "pass")
            st.rerun()
    with col2:
        if st.button("❤️ SMASH", type="primary", use_container_width=True):
            save_answer(user, next_q["id"], "smash")
            st.rerun()
else:
    st.success(f"Bravo {user}, tu as terminé tes 100 questions ! 🎉")

st.write("---")

# --- ZONE DE RÉSULTATS ---
st.subheader("🔥 Notre Match en direct")

matches = get_matches()

if len(matches) == 0:
    st.warning("Pas encore de match commun... Continuez à swiper !")
else:
    # Calcul des statistiques
    tags_count = {"alpes": 0, "perigord": 0, "mer": 0, "sud": 0, "oleole": 0, "chill": 0, "sportif": 0, "pratique": 0}
    for m in matches:
        if m["tag"] in tags_count:
            tags_count[m["tag"]] += 1
            
    # Déduction de la destination gagnante
    dests = {
        "🏔️ La Montagne (Alpes)": tags_count["alpes"],
        "🏰 La Campagne (Périgord)": tags_count["perigord"],
        "🌊 La Mer / Le Sud": tags_count["mer"] + tags_count["sud"]
    }
    top_dest = max(dests, key=dests.get)
    
    # Affichage du verdict
    st.success(f"**{len(matches)} envies validées à deux !**")
    
    if dests[top_dest] > 0:
        st.info(f"**📍 Destination en tête : {top_dest}**")
        
    # Analyse du style de vacances
    style_text = ""
    if tags_count["oleole"] >= 2:
        style_text += "🔥 Ambiance romance et retrouvailles activée !<br>"
    if tags_count["chill"] > tags_count["sportif"]:
        style_text += "😴 Mode vacances : Détente, farniente et repos total.<br>"
    elif tags_count["sportif"] > tags_count["chill"]:
        style_text += "🏃‍♂️ Mode vacances : Ça va bouger, hyperactifs !<br>"
    if tags_count["pratique"] >= 3:
        style_text += "🍼 La logistique avec les enfants dicte vos choix.<br>"
        
    if style_text:
        st.markdown(f"<div style='background:#f1c40f; color:#333; padding:15px; border-radius:10px;'>{style_text}</div>", unsafe_allow_html=True)
    
    st.write("")
    with st.expander("Voir le détail de nos matchs"):
        for m in matches:
            st.markdown(f"- {m['text']}")

st.write("---")
with st.expander("⚙️ Paramètres / Réinitialisation"):
    if st.button("Effacer toutes les réponses et recommencer", type="secondary"):
        reset_db()
        st.rerun()
