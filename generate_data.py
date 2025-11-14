import csv
import random
from pathlib import Path

try:
    from faker import Faker
except ImportError as exc:
    raise ImportError(
        "Faker is required to run this script. Install it with 'pip install faker'."
    ) from exc


def generate_categories(fake: Faker, count: int):
    categories = []
    used_names = set()
    for idx in range(1, count + 1):
        # Ensure category names are unique for easier joins/readability.
        while True:
            name = fake.unique.word().title()
            if name not in used_names:
                used_names.add(name)
                break
        categories.append(
            {
                "id": idx,
                "name": name,
                "description": fake.sentence(nb_words=6),
            }
        )
    return categories


def generate_customers(fake: Faker, count: int):
    customers = []
    for idx in range(1, count + 1):
        customers.append(
            {
                "id": idx,
                "name": fake.name(),
                "email": fake.unique.email(),
                "city": fake.city(),
                "signup_date": fake.date_between(start_date="-2y", end_date="today"),
            }
        )
    return customers


def generate_products(fake: Faker, categories, count: int):
    products = []
    for idx in range(1, count + 1):
        category = random.choice(categories)
        products.append(
            {
                "id": idx,
                "name": fake.catch_phrase(),
                "category_id": category["id"],
                "category": category["name"],
                "price": round(random.uniform(5, 500), 2),
                "stock": random.randint(10, 500),
            }
        )
    return products


def generate_orders(fake: Faker, customers, count: int):
    orders = []
    for idx in range(1, count + 1):
        customer = random.choice(customers)
        order_date = fake.date_between(start_date=customer["signup_date"], end_date="today")
        orders.append(
            {
                "id": idx,
                "customer_id": customer["id"],
                "order_date": order_date,
                "total_amount": 0.0,  # Placeholder, updated after generating order items
            }
        )
    return orders


def generate_order_items(orders, products, count: int):
    order_items = []
    for idx in range(1, count + 1):
        order = random.choice(orders)
        product = random.choice(products)
        quantity = random.randint(1, 5)
        price = product["price"]
        order_items.append(
            {
                "id": idx,
                "order_id": order["id"],
                "product_id": product["id"],
                "quantity": quantity,
                "price": price,
            }
        )
        order["total_amount"] += round(price * quantity, 2)
    # Round totals for consistency after all items are added
    for order in orders:
        order["total_amount"] = round(order["total_amount"], 2)
    return order_items


def write_csv(file_path: Path, fieldnames, rows):
    with file_path.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def select_fields(rows, fieldnames):
    return [{field: row[field] for field in fieldnames} for row in rows]


def main():
    fake = Faker()
    Faker.seed(42)
    random.seed(42)

    base_path = Path(__file__).resolve().parent

    categories = generate_categories(fake, 10)
    customers = generate_customers(fake, 50)
    products = generate_products(fake, categories, 30)
    orders = generate_orders(fake, customers, 100)
    order_items = generate_order_items(orders, products, 200)

    write_csv(
        base_path / "categories.csv",
        ["id", "name", "description"],
        select_fields(categories, ["id", "name", "description"]),
    )
    write_csv(
        base_path / "customers.csv",
        ["id", "name", "email", "city", "signup_date"],
        select_fields(customers, ["id", "name", "email", "city", "signup_date"]),
    )
    write_csv(
        base_path / "products.csv",
        ["id", "name", "category", "price", "stock"],
        select_fields(products, ["id", "name", "category", "price", "stock"]),
    )
    write_csv(
        base_path / "orders.csv",
        ["id", "customer_id", "order_date", "total_amount"],
        select_fields(orders, ["id", "customer_id", "order_date", "total_amount"]),
    )
    write_csv(
        base_path / "order_items.csv",
        ["id", "order_id", "product_id", "quantity", "price"],
        select_fields(order_items, ["id", "order_id", "product_id", "quantity", "price"]),
    )


if __name__ == "__main__":
    main()

