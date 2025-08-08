import os

if os.path.exists("students.db"):
    os.remove("students.db")
    print("Database deleted.")
else:
    print("Database not found.")