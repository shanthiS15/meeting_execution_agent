import os
from database import DATABASE_PATH, get_all_tasks

print("Database path:", os.path.abspath(DATABASE_PATH))
print("Tasks:", get_all_tasks())