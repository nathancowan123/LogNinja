from app.data.log_ninja_data import get_ninja_action

# ✅ Generate a random ninja log entry
ninja_log = get_ninja_action()

# ✅ Print to the console
for entry in ninja_log:
    print(entry)
