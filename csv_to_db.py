import sqlite3
import csv
from datetime import datetime

CSV_FILE = "country_vaccination_stats.csv"
DB_FILE = "sqlite3.db"
TABLE_NAME = "country_vaccination_stats"


def read_csv_file():
    data = []
    with open(CSV_FILE) as f:
        reader = csv.DictReader(f)
        for index, row in enumerate(reader, start=1):
            data.append({
                "id": index,
                "country": row["country"],
                "date": datetime.strptime(row["date"], "%m/%d/%Y"),
                "daily_vaccinations": int(row["daily_vaccinations"]) if row["daily_vaccinations"] else None,
                "vaccines": row["vaccines"],
            })
    return list(sorted(data, key=lambda d: d["id"]))


def create_db():
    con = sqlite3.connect(DB_FILE)
    con.set_trace_callback(print)
    cursor = con.cursor()
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        id INTEGER PRIMARY KEY NOT NULL,
        country VARCHAR(255) NOT NULL,
        date TIMESTAMP NOT NULL,
        daily_vaccinations INTEGER NULL,
        vaccines VARCHAR(255) NOT NULL
    );
    """
    cursor.execute(create_table_query)
    con.commit()
    con.close()


def insert_data_to_db(data, cursor):
    print(f"Inserting: {data}")
    query = f"""INSERT INTO {TABLE_NAME} (id, country, date, daily_vaccinations, vaccines) VALUES (?,?,?,?,?)
    """
    values = [
        data["id"],
        data["country"],
        data["date"],
        data["daily_vaccinations"],
        data["vaccines"],
    ]
    cursor.execute(query, values)


def main():
    create_db()
    data = read_csv_file()
    con = sqlite3.connect(DB_FILE)
    con.set_trace_callback(print)
    cursor = con.cursor()
    for d in data:
        insert_data_to_db(data=d, cursor=cursor)
    cursor.close()
    con.commit()
    con.close()


if __name__ == "__main__":
    main()
