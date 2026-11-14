"""Curated learning content for Eco-Hero Academy.

The two named regional presets are demonstration scenarios, not verified
municipal recycling rules.
"""

ASCII_ART = {
    "welcome": r"""
    ✨🌍♻️🌟
      ECO-HERO ACADEMY
      Level Up Your Recycling!
    🌟♻️🌍✨
    """,
    "challenge_start": r"""
    🧠🚀 ECO-CHALLENGE INITIATED! 🚀🧠
       Prove Your Recycling Prowess!
    """,
    "badge_unlocked": "🏆 BADGE UNLOCKED! 🏆",
    "trophy": r"""
        /|\
       / | \
      /  |  \
     |_______|
    _|_|_|_|_|_
     \       /
      \_____/
    """,
}

REGIONAL_RULES = {
    "Eco-City Standard": {
        "plastic": {
            "tip": "Most plastics (1, 2, 5) can be recycled. Rinse well, no plastic bags. Lids *on* bottles.",
            "fun_fact": "Recycling one ton of plastic saves 7,200 kWh of electricity!",
        },
        "paper": {
            "tip": "Newspapers, magazines, mail, cardboard. Greasy pizza boxes, waxed paper, and shredded paper must go in general waste.",
            "fun_fact": "Recycling a 4-foot stack of newspapers saves one tree!",
        },
        "glass": {
            "tip": "Glass bottles and jars. Rinse, and remove lids (they're often different materials). Labels can stay.",
            "fun_fact": "Glass can be recycled infinitely without losing quality!",
        },
        "electronics": {
            "tip": "E-waste is toxic. Find specific drop-off points or certified recyclers. Never in regular bins!",
            "fun_fact": "E-waste is the fastest-growing waste stream; proper recycling prevents pollution.",
        },
    },
    "Greenburg Initiative": {
        "plastic": {
            "tip": "Only plastics #1 and #2. Rinse thoroughly. Lids *off* bottles and discarded.",
            "fun_fact": "Plastic recycling reduces landfill waste significantly!",
        },
        "paper": {
            "tip": "All clean paper products, including shredded paper (bagged). Greasy cardboard must be composted or binned.",
            "fun_fact": "Recycled paper uses 60% less energy to produce than virgin paper.",
        },
        "glass": {
            "tip": "Clear, brown, and green glass accepted. Rinse and ensure no ceramic or pyrex contaminants. Lids *off*.",
            "fun_fact": "Every ton of recycled glass saves 1,300 pounds of sand!",
        },
        "electronics": {
            "tip": "Special community collection events for e-waste occur monthly. Check city website for dates.",
            "fun_fact": "Many old electronics contain valuable rare earth metals that can be recovered.",
        },
    },
}

# General guide from the original project. These are educational examples,
# not universal disposal instructions; local programs may differ.
RECYCLING_GUIDE = {
    "plastic": {
        "tip": "Most plastics (bottles, jugs, tubs) can be recycled if clean and have the symbol. Remember to rinse them!",
        "what_not_to_recycle": "Plastic bags, plastic film, Styrofoam, plastic cutlery, toys, or medical waste. These jam machines!",
        "fun_fact": "Plastic can take hundreds of years to decompose in a landfill.",
    },
    "paper": {
        "tip": "Newspapers, magazines, mail, cardboard boxes (flattened), paperboard. Keep them dry!",
        "what_not_to_recycle": "Greasy pizza boxes, paper towels, tissues, coffee cups (often lined with plastic), shredded paper (unless bagged according to local rules).",
        "fun_fact": "Recycling one ton of paper saves 17 trees, 7,000 gallons of water, and 3 cubic yards of landfill space.",
    },
    "glass": {
        "tip": "Glass bottles and jars (food and beverage). Rinse them out. No need to remove labels.",
        "what_not_to_recycle": "Ceramics, Pyrex, window glass, mirrors, light bulbs, drinking glasses. These have different melting points or compositions.",
        "fun_fact": "Glass can be recycled endlessly without losing quality, making it a truly sustainable material!",
    },
    "metal": {
        "tip": "Aluminum cans, steel/tin cans (food and beverage). Rinse them out. Aerosol cans are often accepted if empty.",
        "what_not_to_recycle": "Scrap metal, aluminum foil (unless balled up and very clean), hazardous waste containers, electronics.",
        "fun_fact": "Recycling aluminum saves 95% of the energy compared to making it from raw materials. Enough to power a TV for 3 hours!",
    },
    "electronics": {
        "tip": "Old phones, computers, batteries, TVs. These are 'e-waste' and contain hazardous materials. Never put in regular bins!",
        "what_not_to_recycle": "Anything electronic that's not specifically handled by an e-waste program.",
        "fun_fact": "E-waste is the fastest-growing waste stream in the world. Proper recycling prevents toxic substances like lead and mercury from polluting our environment.",
    },
    "food": {
        "tip": "Compost food waste if possible – it creates nutrient-rich soil! Check if your area has food waste collection.",
        "what_not_to_recycle": "Food scraps should never go into your recycling bin for paper, plastic, glass, or metal. They contaminate recyclables.",
        "fun_fact": "Composting food waste reduces methane gas emissions from landfills, a powerful greenhouse gas.",
    },
    "cardboard": {
        "tip": "Corrugated cardboard boxes (delivery boxes, moving boxes). Flatten them and keep them dry.",
        "what_not_to_recycle": "Greasy pizza boxes, wet cardboard, cardboard with heavy wax coatings.",
        "fun_fact": "Recycling cardboard uses 75% less energy than making new cardboard from virgin pulp.",
    },
    "batteries": {
        "tip": "Most batteries (AA, AAA, C, D, 9V, button cells, rechargeable) should be recycled at special collection points. Never throw in trash!",
        "what_not_to_recycle": "Car batteries (different program), damaged or leaking batteries (handle with extreme care).",
        "fun_fact": "Many batteries contain valuable metals that can be recovered, and harmful chemicals that should not end up in landfills.",
    },
    "clothing": {
        "tip": "Donate usable clothing to charities. For unwearable textiles, check for textile recycling programs in your area.",
        "what_not_to_recycle": "Wet, moldy, or heavily soiled clothing usually cannot be recycled.",
        "fun_fact": "The fashion industry is a major polluter; recycling and reusing clothing reduces its environmental impact.",
    },
}

QUIZ_QUESTIONS = [
    {"type": "tf", "question": "True or False: Greasy pizza boxes can always be recycled with other paper.", "answer": False, "explanation": "Grease contaminates paper, making it non-recyclable. Compost or trash the greasy part!"},
    {"type": "tf", "question": "True or False: All plastics with a recycling symbol are accepted in every curbside recycling program.", "answer": False, "explanation": "Recycling rules vary by location! Always check your local guidelines."},
    {"type": "tf", "question": "True or False: You should rinse glass jars before recycling them.", "answer": True, "explanation": "Rinsing removes food residue that can attract pests and contaminate other recyclables."},
    {"type": "tf", "question": "True or False: Old cell phones can be safely thrown in the regular trash.", "answer": False, "explanation": "E-waste like cell phones contains toxic materials and valuable components; it requires special recycling."},
    {"type": "tf", "question": "True or False: Plastic bags should be put in your curbside recycling bin.", "answer": False, "explanation": "Plastic bags jam recycling machinery. Many grocery stores have special drop-offs for them."},
    {"type": "tf", "question": "True or False: Ceramics and Pyrex dishes can be recycled with glass bottles.", "answer": False, "explanation": "Ceramics and Pyrex have different melting points and compositions than glass bottles, contaminating the batch."},
    {"type": "mc", "question": "Which of these materials is generally NOT accepted in curbside recycling bins?", "options": ["A. Aluminum cans", "B. Glass bottles", "C. Styrofoam cups", "D. Cardboard boxes"], "answer": "C", "explanation": "Styrofoam is notoriously difficult to recycle and rarely accepted in curbside programs."},
    {"type": "mc", "question": "What is the best way to dispose of old batteries?", "options": ["A. Throw them in the trash", "B. Place them in the recycling bin with plastics", "C. Take them to a special battery collection point", "D. Flush them down the toilet"], "answer": "C", "explanation": "Batteries contain hazardous materials and should be recycled at designated collection points."},
    {"type": "mc", "question": "Before recycling plastic bottles, what is the most important step?", "options": ["A. Remove the label", "B. Rinse them out", "C. Flatten them completely", "D. Put the lid back on tightly"], "answer": "B", "explanation": "Rinsing removes food and liquid residue, preventing contamination and odors."},
    {"type": "mc", "question": "Which material can be recycled endlessly without losing quality?", "options": ["A. Plastic", "B. Paper", "C. Glass", "D. Textiles"], "answer": "C", "explanation": "Glass is unique in its ability to be recycled repeatedly without degradation."},
    {"type": "mc", "question": "What is 'e-waste'?", "options": ["A. Everyday trash", "B. Electronic waste like old computers and phones", "C. Organic food scraps", "D. Excess paper waste"], "answer": "B", "explanation": "E-waste refers to discarded electronic devices, which require special handling due to hazardous components."},
]

BADGES = {
    "First Step": {"desc": "Completed your first Eco-Challenge round.", "threshold": {"challenge_rounds": 1}},
    "Recycling Rookie": {"desc": "Scored 3 points in Eco-Challenge.", "threshold": {"challenge_score": 3}},
    "Material Master": {"desc": "Viewed tips for 5 different materials.", "threshold": {"materials_viewed": 5}},
    "Eco-Enthusiast": {"desc": "Played 5 Eco-Challenge rounds.", "threshold": {"challenge_rounds": 5}},
    "Challenge Conqueror": {"desc": "Achieved a perfect score in a 5-question challenge round.", "threshold": {"perfect_challenge": True}},
    "Knowledge Seeker": {"desc": "Used the built-in Eco Advisor 3 times.", "threshold": {"advisor_uses": 3}},
    "Green Guardian": {"desc": "Scored 10 points in Eco-Challenge.", "threshold": {"challenge_score": 10}},
}

# These two named presets are fictional examples retained from the 2025 demo.
REGIONS = tuple(REGIONAL_RULES) + ("General Guide",)
MATERIALS = tuple(RECYCLING_GUIDE)
