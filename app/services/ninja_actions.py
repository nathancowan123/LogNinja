import random

# ✅ Core Ninja Activities
ninja_idle_actions = [
    "🏋️ Ninja trains tirelessly, perfecting his technique. 💪",
    "🧘 Ninja meditates under the waterfall, finding inner peace. 🌊",
    "🥋 Ninja sharpens his katana, preparing for the next battle. ⚔️",
    "🍣 Ninja enjoys sushi and a warm cup of sake. 🍶",
    "🌙 Ninja disappears into the night, watching over the system. 🥷",
    "🐾 Ninja silently moves through the shadows, scouting for threats. 👣",
    "🔥 Ninja practices breathing techniques to summon his inner energy. 🔥",
    "🌪️ Ninja performs a tornado kick, slicing through unnecessary files. 🌀",
    "💨 Ninja moves at lightning speed, eliminating system bloat. ⚡",
    "🔮 Ninja studies ancient scrolls, learning the secrets of system optimization. 📜",
    "👀 Ninja stays vigilant, waiting for the perfect moment to strike. 🏯",
    "🕶️ Ninja polishes his throwing stars, preparing for swift removals. ✨",
    "🎭 Ninja switches disguises, blending into the logs undetected. 🎎",
    "⚡ Ninja channels his chi, sensing unnecessary cache buildup... and strikes! ⚔️",
    "🥷 Ninja vanishes from sight, leaving no trace behind. 🌫️",
    "🗡️ Ninja carves a path through inefficiencies, making the system run smoother. 🔪",
]

# ✅ Special Combat & Environmental Events
weather_storms = [
    {
        "start": "🌥️ The sky darkens... Ninja senses a disturbance in the system.",
        "peak": "🌩️ A storm rages! Logs pile up, and cache clogs the pathways! ⚔️",
        "fade": "🌅 The storm passes. Ninja restores balance to the system. 🌀",
    },
    {
        "start": "💨 A strong wind rises. Ninja adjusts his stance, prepared for anything.",
        "peak": "🌪️ A whirlwind of errors threatens stability! Ninja takes action! ⚡",
        "fade": "🌞 The winds settle. Logs have been cleared, and peace returns. 🍃",
    },
    {
        "start": "🔥 The air grows warm... Ninja detects inefficiencies forming. 🥵",
        "peak": "⚔️ The battle begins! Ninja slashes through bloated files and wasted space!",
        "fade": "🌙 The fight is over. The system is optimized once more. 🥷",
    },
    {
        "start": "⏳ Time slows down... Something big is coming.",
        "peak": "⚠️ The system struggles under pressure! Ninja unleashes a powerful strike! 🗡️",
        "fade": "💨 With a final swift move, Ninja restores order. ⚖️",
    },
]

# ✅ Secret Easter Egg Events (10% chance)
secret_moments = [
    "🦉 A mysterious owl lands nearby. Ninja listens to the whispers of ancient knowledge. 📜",
    "💀 Ninja encounters a ghostly warrior... A silent nod is exchanged before parting ways. ☠️",
    "🎴 Ninja flips a secret talisman, revealing hidden system secrets. 🀄",
    "🐉 A dragon appears in the logs... Ninja bows in deep respect. 🐲",
    "🔮 Ninja glimpses into the future... He sees an optimized, perfected system. ⏳",
]

# ✅ Random Probability Functions
def should_trigger_storm():
    return random.random() < 0.10  # 10% probability of storm event

def should_trigger_secret():
    return random.random() < 0.05  # 5% probability of special ninja event

# ✅ Get Ninja Actions
def get_ninja_action():
    """🎭 Returns a ninja activity, weather event, or secret moment."""
    if should_trigger_storm():
        storm = random.choice(weather_storms)
        return [storm["start"], storm["peak"], storm["fade"]]
    
    if should_trigger_secret():
        return [random.choice(secret_moments)]
    
    return [random.choice(ninja_idle_actions)]
