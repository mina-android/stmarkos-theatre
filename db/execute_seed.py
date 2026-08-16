import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'server'))
import db

def run_seed():
    seed_sql_path = os.path.join(os.path.dirname(__file__), 'seed.sql')
    if not os.path.exists(seed_sql_path):
        print(f"Error: seed.sql not found at {seed_sql_path}. Please run seed.py first.")
        return

    try:
        print("Connecting to database...")
        conn = db.get_db_connection()
        cursor = conn.cursor()
        
        print("Reading seed.sql...")
        with open(seed_sql_path, "r", encoding="utf-8") as f:
            sql_content = f.read()

        print("Executing seed database commands as a single transaction...")
        cursor.execute(sql_content)
        
        print("Database seeded successfully!")
        conn.close()
    except Exception as e:
        print("Failed to seed database:", e)

if __name__ == '__main__':
    run_seed()
