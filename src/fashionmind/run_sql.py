
import sqlite3
from pathlib import Path

db_path = Path("database/fashionmind.db")
sql_path = Path("database/analysis.sql")

connection = sqlite3.connect(db_path)

with open(sql_path, "r", encoding="utf-8") as file:
    sql_script = file.read()

for statement in sql_script.split(";"):
    statement = statement.strip()

    if not statement:
        continue

    cursor = connection.execute(statement)

    if cursor.description:
        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()

        print("\n" + "=" * 45)
        print("QUERY RESULT")
        print("=" * 45)
        print(" | ".join(columns))

        for row in rows:
            print(" | ".join(str(value) for value in row))

connection.close()
