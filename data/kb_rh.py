KB_RH = {
    "salutations": {
        "keywords": ["bonjour", "bonsoir", "salam", "salut", "coucou", "hi", "hello"],
        "responses": {
            "default": "Bonjour ! Je suis l'assistant RH de Safran. Comment puis-je vous aider ?",
            "darija": "السلام عليكم ! أنا مساعد الموارد البشرية في سافران. كيف يمكنني مساعدتك ؟"
        },
        "confidence": 0.95
    },
    "remerciements": {
        "keywords": ["merci", "merci beaucoup", "thanks", "thank you", "shukran"],
        "responses": {
            "default": "De rien ! N'hésitez pas à me poser d'autres questions.",
            "darija": "عفاك ! لا تتردد في طرح أسئلة أخرى."
        },
        "confidence": 0.95
    },
    "au_revoir": {
        "keywords": ["au revoir", "bye", "goodbye", "à bientôt", "bisous", "bslama"],
        "responses": {
            "default": "Au revoir ! Bonne journée.",
            "darija": "بسلامة ! يوم سعيد."
        },
        "confidence": 0.95
    },
    "conges": {
        "keywords": ["congé", "congés", "vacances", "leave", "holiday", "absence"],
        "responses": {
            "CDI": "En tant que CDI, vous avez droit à 30 jours de congés payés par an. Vous pouvez les prendre en accord avec votre manager.",
            "CDD": "En tant que CDD, vous avez droit à 10% de votre salaire brut en congés payés.",
            "Intérim": "En tant qu'intérimaire, vos congés sont gérés selon votre contrat d'agence.",
            "Stagiaire": "En tant que stagiaire, vous n'avez pas droit aux congés payés.",
            "default": "Pour les congés, veuillez consulter votre contrat ou contacter RH."
        },
        "confidence": 0.90
    },
    "rtt": {
        "keywords": ["rtt", "réduction temps travail", "jours rtt", "réduction du temps"],
        "responses": {
            "Cadre": "En tant que cadre, vous avez droit à des jours RTT selon votre accord collectif.",
            "Non-cadre": "En tant que non-cadre, vous avez droit à des jours RTT selon votre accord collectif.",
            "default": "Les jours RTT sont gérés selon votre accord collectif. Contactez RH pour plus d'informations."
        },
        "confidence": 0.85
    },
    "avantages_sociaux": {
        "keywords": ["avantages", "social", "benefits", "mutuelle", "assurance"],
        "responses": {
            "default": "Safran propose une mutuelle complémentaire, une prévoyance, et des services aux salariés. Consultez votre contrat pour les détails."
        },
        "confidence": 0.80
    },
    "transport": {
        "keywords": ["transport", "navette", "bus", "métro", "ticket", "mobilité"],
        "responses": {
            "default": "Safran propose une prise en charge du transport selon votre lieu de travail. Consultez RH pour les modalités."
        },
        "confidence": 0.80
    },
    "pointage": {
        "keywords": ["pointage", "horaires", "heures", "timing", "présence", "badge"],
        "responses": {
            "default": "Le pointage se fait via votre badge. Les horaires standards sont 9h-17h30. Contactez votre manager en cas de question."
        },
        "confidence": 0.85
    },
    "paie": {
        "keywords": ["paie", "salaire", "rémunération", "paye", "bulletin", "fiche de paie"],
        "responses": {
            "default": "Votre bulletin de paie est disponible sur le portail RH. Pour toute question sur votre rémunération, contactez RH."
        },
        "confidence": 0.85
    },
    "statut": {
        "keywords": ["statut", "contrat", "cdi", "cdd", "intérim", "stagiaire", "apprenti"],
        "responses": {
            "CDI": "Vous êtes en CDI. Vous bénéficiez de la protection du code du travail et des avantages Safran.",
            "CDD": "Vous êtes en CDD. Votre contrat a une date d'expiration définie.",
            "Intérim": "Vous êtes en contrat d'intérim. Vos conditions sont gérées par votre agence.",
            "Stagiaire": "Vous êtes stagiaire. Consultez votre convention de stage pour vos droits.",
            "Apprenti": "Vous êtes apprenti. Consultez votre contrat d'apprentissage pour vos droits."
        },
        "confidence": 0.90
    },
    "droits": {
        "keywords": ["droits", "droit", "protection", "légal", "loi"],
        "responses": {
            "default": "Vos droits dépendent de votre statut. Consultez votre contrat ou contactez RH pour plus d'informations."
        },
        "confidence": 0.80
    },
    "mutuelle": {
        "keywords": ["mutuelle", "santé", "assurance maladie", "couverture", "médical"],
        "responses": {
            "default": "Safran propose une mutuelle complémentaire. Consultez votre contrat pour les garanties et modalités."
        },
        "confidence": 0.85
    },
    "formation": {
        "keywords": ["formation", "training", "cours", "apprentissage", "développement"],
        "responses": {
            "default": "Safran propose des formations continues. Contactez RH pour connaître les formations disponibles et les modalités d'accès."
        },
        "confidence": 0.80
    },
    "cantine": {
        "keywords": ["cantine", "restaurant", "repas", "déjeuner", "lunch", "food"],
        "responses": {
            "default": "Une cantine est disponible sur site. Les repas sont subventionnés selon votre statut."
        },
        "confidence": 0.80
    },
    "interdites": {
        "keywords": ["salaire collègue", "dossier médical", "sanction", "discipline", "secret", "confidentiel"],
        "responses": {
            "default": "Je ne peux pas répondre à cette question pour des raisons de confidentialité. Contactez RH directement."
        },
        "confidence": 1.0,
        "blocked": True
    },
    "default": {
        "response": "Je n'ai pas trouvé de réponse à votre question. Pouvez-vous reformuler ou contacter RH directement ?"
    }
}

PROFILE_ADAPTATIONS = {
    "CDI": {
        "congés": 30,
        "rtt": "Selon accord collectif",
        "avantages": "Tous les avantages"
    },
    "CDD": {
        "congés": "10% du salaire brut",
        "rtt": "Selon accord collectif",
        "avantages": "Avantages réduits"
    },
    "Intérim": {
        "congés": "Selon agence",
        "rtt": "Non applicable",
        "avantages": "Minimes"
    },
    "Stagiaire": {
        "congés": "Non applicable",
        "rtt": "Non applicable",
        "avantages": "Accès cantine"
    },
    "Apprenti": {
        "congés": "Selon contrat",
        "rtt": "Non applicable",
        "avantages": "Selon contrat"
    }
}

LANGUAGES = {
    "fr": "Français",
    "ar": "Darija"
}
