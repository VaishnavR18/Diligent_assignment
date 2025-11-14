import sqlite3
from pathlib import Path


DB_NAME = "ecommerce.db"


QUERY = """
SELECT
    c.name AS customer_name,
    o.order_date,
    p.name AS product_name,
    oi.quantity,
    ROUND(oi.quantity * oi.price, 2) AS total_spent
FROM orders o
JOIN customers c ON o.customer_id = c.id
JOIN order_items oi ON oi.order_id = o.id
JOIN products p ON oi.product_id = p.id
ORDER BY o.order_date DESC, c.name ASC
"""


def main():
    db_path = Path(__file__).resolve().parent / DB_NAME

    if not db_path.exists():
        raise FileNotFoundError(f"Database '{DB_NAME}' not found. Run load_to_database.py first.")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(QUERY)
    rows = cursor.fetchall()

    if not rows:
        print("No records found.")
        conn.close();
        return

    header = f"{'Customer':<25} {'Order Date':<12} {'Product':<35} {'Qty':<5} {'Total Spent':>12}"
    divider = "-" * len(header)
    print(header)
    print(divider)
    for customer_name, order_date, product_name, quantity, total_spent in rows:
        print(
            f"{customer_name:<25} {order_date:<12} {product_name:<35} {quantity:<5} ${total_spent:>10.2f}"
        )

    conn.close()


if __name__ == "__main__":
    main()

