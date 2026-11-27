import sqlite3


connection = sqlite3.connect(":memory:")
connection.execute("PRAGMA foreign_keys = ON")

connection.executescript(
    """
    CREATE TABLE Users (
        user_id INTEGER PRIMARY KEY,
        full_name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        created_at TEXT NOT NULL DEFAULT (datetime('now')),
        CHECK (length(trim(full_name)) > 0),
        CHECK (instr(email, '@') > 1)
    );

    CREATE TABLE Products (
        product_id INTEGER PRIMARY KEY,
        product_name TEXT NOT NULL,
        unit_price NUMERIC NOT NULL,
        stock_quantity INTEGER NOT NULL DEFAULT 0,
        CHECK (length(trim(product_name)) > 0),
        CHECK (unit_price >= 0),
        CHECK (stock_quantity >= 0)
    );

    CREATE TABLE Orders (
        order_id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        order_date TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'pending',
        FOREIGN KEY (user_id) REFERENCES Users(user_id),
        CHECK (datetime(order_date) IS NOT NULL),
        CHECK (status IN ('pending', 'paid', 'shipped', 'cancelled'))
    );

    CREATE TABLE OrderDetails (
        order_detail_id INTEGER PRIMARY KEY,
        order_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        unit_price NUMERIC NOT NULL,
        FOREIGN KEY (order_id) REFERENCES Orders(order_id),
        FOREIGN KEY (product_id) REFERENCES Products(product_id),
        CHECK (quantity > 0),
        CHECK (unit_price >= 0),
        UNIQUE (order_id, product_id)
    );

    CREATE INDEX idx_orders_user_date ON Orders(user_id, order_date);
    CREATE INDEX idx_orderdetails_product ON OrderDetails(product_id);
    CREATE INDEX idx_orderdetails_order ON OrderDetails(order_id);

    INSERT INTO Users (user_id, full_name, email) VALUES
        (1, 'Aarav Shah', 'aarav@example.com'),
        (2, 'Sara Khan', 'sara@example.com'),
        (3, 'Leo Martin', 'leo@example.com');

    INSERT INTO Products (product_id, product_name, unit_price, stock_quantity) VALUES
        (101, 'Wireless Mouse', 25.00, 50),
        (102, 'Mechanical Keyboard', 75.00, 30),
        (103, 'USB-C Hub', 40.00, 40),
        (104, 'Laptop Stand', 35.00, 25);

    INSERT INTO Orders (order_id, user_id, order_date, status) VALUES
        (5001, 1, '2026-01-10 10:30:00', 'paid'),
        (5002, 1, '2026-02-14 14:15:00', 'paid'),
        (5003, 2, '2026-02-18 09:45:00', 'paid'),
        (5004, 3, '2026-03-03 16:20:00', 'cancelled'),
        (5005, 2, '2026-03-20 11:10:00', 'paid');

    INSERT INTO OrderDetails (
        order_detail_id, order_id, product_id, quantity, unit_price
    ) VALUES
        (1, 5001, 101, 2, 25.00),
        (2, 5001, 103, 1, 40.00),
        (3, 5002, 102, 1, 75.00),
        (4, 5003, 101, 3, 25.00),
        (5, 5003, 104, 1, 35.00),
        (6, 5004, 102, 1, 75.00),
        (7, 5005, 103, 2, 40.00),
        (8, 5005, 104, 1, 35.00);
    """
)


def print_rows(title, cursor):
    print(f"\n{title}")
    columns = [description[0] for description in cursor.description]
    print(" | ".join(columns))
    print("-" * (sum(len(column) for column in columns) + 3 * (len(columns) - 1)))
    for row in cursor.fetchall():
        print(" | ".join("" if value is None else str(value) for value in row))


print_rows(
    "Orders for User ID 1",
    connection.execute(
        """
        SELECT
            o.order_id,
            o.order_date,
            o.status,
            p.product_name,
            od.quantity,
            od.unit_price,
            od.quantity * od.unit_price AS line_total
        FROM Orders AS o
        JOIN OrderDetails AS od ON od.order_id = o.order_id
        JOIN Products AS p ON p.product_id = od.product_id
        WHERE o.user_id = ?
        ORDER BY o.order_date DESC, o.order_id, p.product_name
        """,
        (1,),
    ),
)

print_rows(
    "Most Purchased Product",
    connection.execute(
        """
        SELECT
            p.product_id,
            p.product_name,
            SUM(od.quantity) AS total_quantity_purchased
        FROM OrderDetails AS od
        JOIN Orders AS o ON o.order_id = od.order_id
        JOIN Products AS p ON p.product_id = od.product_id
        WHERE o.status <> 'cancelled'
        GROUP BY p.product_id, p.product_name
        ORDER BY total_quantity_purchased DESC, p.product_id
        LIMIT 1
        """
    ),
)

print_rows(
    "Monthly Paid-Order Revenue",
    connection.execute(
        """
        SELECT
            substr(o.order_date, 1, 7) AS revenue_month,
            ROUND(SUM(od.quantity * od.unit_price), 2) AS monthly_revenue
        FROM Orders AS o
        JOIN OrderDetails AS od ON od.order_id = o.order_id
        WHERE o.status = 'paid'
        GROUP BY substr(o.order_date, 1, 7)
        ORDER BY revenue_month
        """
    ),
)

print(
    """
\nNormalization
1NF: Each table uses atomic columns and OrderDetails stores one product per row.
2NF: Customer and product attributes are separated from order-detail attributes.
3NF: Names, prices, stock, and order data are stored only in their owning entities.

Optimization
- Foreign keys enforce valid users, orders, and products.
- Indexes support user/order-date, order-detail/order, and product lookups.
- Unit price in OrderDetails preserves the purchase-time price.
- Parameterized queries prevent SQL injection.
- In a production database, use DECIMAL for money and add reporting indexes
  based on measured query plans.
"""
)

connection.close()
