import random

# ✅ Core Ninja Activities
ninja_idle_actions = [
    "Ninja trains tirelessly, refining his precision and speed.",
    "Ninja meditates in silence, attuning himself to the system’s energy.",
    "Ninja sharpens his katana, preparing to eliminate inefficiencies.",
    "Ninja studies ancient scrolls, learning optimization techniques.",
    "Ninja vanishes into the shadows, watching over the system’s balance.",
    "Ninja moves silently, scanning for threats in the background processes.",
    "Ninja senses the digital current flowing smoothly, remaining vigilant.",
    "Ninja executes a rapid maneuver, clearing unnecessary system bloat.",
    "Ninja practices control, preventing memory leaks before they emerge.",
    "Ninja enhances his reflexes, preparing for sudden system overloads.",
    "Ninja polishes his tools, optimizing logs for efficiency.",
    "Ninja conceals his presence, monitoring for unseen system disruptions.",
    "Ninja prepares his tools, ensuring rapid response to system threats.",
    "Ninja adjusts his stance, prepared to strike at inefficiencies.",
    "Ninja maintains a watchful eye, ensuring smooth operations.",
]

# ✅ Environmental & System Events
weather_storms = [
    {
        "start": "The system’s energy shifts... Ninja senses an approaching disturbance.",
        "peak": "A digital storm erupts! Logs pile up, and memory pressure increases!",
        "fade": "The storm passes. Ninja restores harmony to the system’s flow.",
    },
    {
        "start": "A strong current emerges, disrupting stability.",
        "peak": "A data whirlwind forms, clogging system pathways! Ninja intervenes.",
        "fade": "The disruption fades. Processes are optimized, and stability returns.",
    },
    {
        "start": "An unusual heat radiates through the system, indicating inefficiencies.",
        "peak": "The system strains under pressure! Ninja strikes swiftly to restore balance.",
        "fade": "The system breathes easier. Unnecessary data has been eliminated.",
    },
    {
        "start": "Time slows... Ninja detects an impending system overload.",
        "peak": "Warning! Resources are under strain. Ninja acts to prevent collapse.",
        "fade": "Ninja neutralizes the threat. The system remains steady and efficient.",
    },
]

# ✅ Rare, Unpredictable Events (5% chance)
secret_moments = [
    "A hidden protocol reveals itself. Ninja deciphers its purpose.",
    "A rogue process moves undetected... Ninja silently neutralizes it.",
    "An anomaly appears in the logs. Ninja studies its meaning.",
    "A forgotten script awakens, threatening system balance. Ninja intercepts.",
    "Ninja discovers a pattern in the data flow, enhancing system efficiency.",
]

# ✅ Random Probability Functions
def should_trigger_storm():
    return random.random() < 0.10  # 10% chance of system disturbance

def should_trigger_secret():
    return random.random() < 0.05  # 5% chance of uncovering a hidden event

# ✅ Get Ninja Actions
def get_ninja_action():
    """🎭 Returns a ninja activity, system event, or secret moment."""
    if should_trigger_storm():
        storm = random.choice(weather_storms)
        return [storm["start"], storm["peak"], storm["fade"]]
    
    if should_trigger_secret():
        return [random.choice(secret_moments)]
    
    return [random.choice(ninja_idle_actions)]
