import csv
import sqlite3
from pathlib import Path


DB_NAME = "ecommerce.db"
CSV_FILES = {
    "customers": "customers.csv",
    "products": "products.csv",
    "orders": "orders.csv",
    "order_items": "order_items.csv",
    "categories": "categories.csv",
}


TABLE_DEFINITIONS = {
    "customers": """
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            city TEXT NOT NULL,
            signup_date TEXT NOT NULL
        )
    """,
    "products": """
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    """,
    "orders": """
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            order_date TEXT NOT NULL,
            total_amount REAL NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers (id)
        )
    """,
    "order_items": """
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders (id),
            FOREIGN KEY (product_id) REFERENCES products (id)
        )
    """,
    "categories": """
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT NOT NULL
        )
    """,
}


def load_csv_rows(csv_path: Path):
    with csv_path.open("r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)


def insert_rows(cursor, table_name: str, rows):
    if not rows:
        return
    columns = rows[0].keys()
    placeholders = ", ".join(["?"] * len(columns))
    sql = f'INSERT INTO {table_name} ({", ".join(columns)}) VALUES ({placeholders})'
    values = [tuple(row[col] for col in columns) for row in rows]
    cursor.executemany(sql, values)


def main():
    base_path = Path(__file__).resolve().parent
    db_path = base_path / DB_NAME

    if db_path.exists():
        db_path.unlink()

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    for table, ddl in TABLE_DEFINITIONS.items():
        cursor.execute(ddl)
    print("Tables created successfully.")

    for table_name, filename in CSV_FILES.items():
        csv_path = base_path / filename
        rows = load_csv_rows(csv_path)
        insert_rows(cursor, table_name, rows)
        print(f"Inserted {len(rows)} records into {table_name}.")

    conn.commit()
    conn.close()
    print(f"SQLite database '{DB_NAME}' populated successfully.")


if __name__ == "__main__":
    main()

