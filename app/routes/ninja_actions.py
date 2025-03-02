import random

# ✅ Ninja activities when nothing happens
ninja_idle_actions = [
    "🏋️ Ninja hits the gym to sharpen his skills! 💪",
    "🧘 Ninja is meditating under the waterfall... 🌊",
    "🥋 Ninja practices his katas in the dojo... ⚔️",
    "💨 Ninja goes for a quick rooftop sprint to stay agile. 🏃‍♂️",
    "🍣 Ninja takes a sushi break. Even warriors need to eat. 🍣",
]

# ✅ Storm events (randomly appear)
weather_storms = [
    {
        "start": "🌥️ The sky darkens... Something is coming.",
        "peak": "🌩️⚡ A storm is raging! Winds howl through the dojo.",
        "fade": "🌅 The storm passes, leaving fresh air behind.",
    },
    {
        "start": "🌫️ A thick mist creeps in... The air feels heavy.",
        "peak": "⛈️ Torrential rain batters the rooftops! Lightning splits the sky!",
        "fade": "🌤️ The mist slowly lifts. Silence returns.",
    },
    {
        "start": "💨 A powerful gust of wind sweeps through the village.",
        "peak": "🌪️ A massive whirlwind forms! The ninja holds his ground.",
        "fade": "🌞 The winds settle. The sun breaks through once more.",
    }
]

# ✅ Random chance to trigger a storm (10% chance)
def should_trigger_storm():
    return random.random() < 0.10  # 10% probability

def get_storm_event():
    """🌩️ Returns a storm sequence with start, peak, and fade stages."""
    return random.choice(weather_storms)

def get_ninja_action():
    """🎭 Returns either a normal ninja activity or a weather event."""
    if should_trigger_storm():
        storm = get_storm_event()
        return [storm["start"], storm["peak"], storm["fade"]]  # ⚡ A full storm sequence
    return [random.choice(ninja_idle_actions)]  # Normal ninja action
