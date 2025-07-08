"""Seed initial types data

Revision ID: 56b4fed49d96
Revises: 
Create Date: 2025-07-08 20:28:49.856565

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '56b4fed49d96'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop tables if they exist (order matters due to FKs)
    op.execute("DROP TABLE IF EXISTS ice_cream_flavors;")
    op.execute("DROP TABLE IF EXISTS ice_cream;")
    op.execute("DROP TABLE IF EXISTS flavors;")
    op.execute("DROP TABLE IF EXISTS toppings;")
    op.execute("DROP TABLE IF EXISTS sizes;")
    op.execute("DROP TABLE IF EXISTS types;")
    op.execute("DROP TABLE IF EXISTS users;")  # Add drop for users table

    # Create users table
    op.execute("""
        CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            email VARCHAR(255) UNIQUE,
            hashed_password VARCHAR(255)
        );
    """)

    # Create types table
    op.execute("""
        CREATE TABLE types (
            id SERIAL PRIMARY KEY,
            type VARCHAR(255) NOT NULL
        );
    """)

    # Create sizes table
    op.execute("""
        CREATE TABLE sizes (
            id SERIAL PRIMARY KEY,
            size VARCHAR(255) NOT NULL
        );
    """)

    # Create toppings table
    op.execute("""
        CREATE TABLE toppings (
            id SERIAL PRIMARY KEY,
            topping VARCHAR(255) NOT NULL
        );
    """)

    # Create flavors table
    op.execute("""
        CREATE TABLE flavors (
            id SERIAL PRIMARY KEY,
            flavor VARCHAR(255) NOT NULL
        );
    """)

    # Create ice_cream table
    op.execute("""
        CREATE TABLE ice_cream (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            type_id INTEGER NOT NULL,
            size_id INTEGER NOT NULL,
            topping_id INTEGER,
            price FLOAT NOT NULL,
            description TEXT NOT NULL,
            images TEXT,
            FOREIGN KEY (type_id) REFERENCES types(id),
            FOREIGN KEY (size_id) REFERENCES sizes(id),
            FOREIGN KEY (topping_id) REFERENCES toppings(id)
        );
    """)

    # Create ice_cream_flavors table
    op.execute("""
        CREATE TABLE ice_cream_flavors (
            id SERIAL PRIMARY KEY,
            flavor_id INTEGER NOT NULL,
            ice_cream_id INTEGER NOT NULL,
            FOREIGN KEY (flavor_id) REFERENCES flavors(id),
            FOREIGN KEY (ice_cream_id) REFERENCES ice_cream(id)
        );
    """)
    op.execute("CREATE INDEX idx_flavor_icecream ON ice_cream_flavors(flavor_id, ice_cream_id);")

    # Create orders table
    op.execute("""
        CREATE TABLE orders (
            id SERIAL PRIMARY KEY,
            total_amount FLOAT,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
    """)

    # Create order_items table
    op.execute("""
        CREATE TABLE order_items (
            id SERIAL PRIMARY KEY,
            quantity INTEGER,
            price_at_purchase FLOAT,
            order_id INTEGER,
            ice_cream_id INTEGER,
            FOREIGN KEY (order_id) REFERENCES orders(id),
            FOREIGN KEY (ice_cream_id) REFERENCES ice_cream(id)
        );
    """)

    # Seed types
    op.execute("""
        INSERT INTO types (type) VALUES
        ('Cone'),
        ('Cup'),
        ('Sandwich');
    """)

    # Seed sizes
    op.execute("""
        INSERT INTO sizes (size) VALUES
        ('Small'),
        ('Medium'),
        ('Large');
    """)

    # Seed toppings
    op.execute("""
        INSERT INTO toppings (topping) VALUES
        ('Caramel Sauce'),
        ('Chocolate Syrup'),
        ('Whipped Cream'),
        ('Chopped Nuts'),
        ('Rainbow Sprinkles'),
        ('Chocolate Chips'),
        ('Crushed Cookies'),
        ('Tropical Fruit Slices'),
        ('Marshmallows');
    """)

    # Seed flavors
    op.execute("""
        INSERT INTO flavors (flavor) VALUES
        ('Vanilla'),
        ('Chocolate'),
        ('Mint'),
        ('Matcha'),
        ('Strawberry'),
        ('Blueberry'),
        ('Mango'),
        ('Taro');
    """)

    # Seed ice_cream
    op.execute("""
        INSERT INTO ice_cream (name, type_id, size_id, topping_id, price, description, images) VALUES
        ('Vanilla Cone', 1, 1, NULL, 3.99, 'Vanilla ice cream in a crispy cone.', 'https://kid-dev.australiaeast.cloudapp.azure.com/static/images/Small-Vanilla-Cone.png'),
        ('Chocolate Delight', 2, 2, 2, 4.99, 'Rich chocolate ice cream in a cup with chocolate syrup.', 'https://kid-dev.australiaeast.cloudapp.azure.com/static/images/Medium-Chocolate-Delight.png'),
        ('Minty Matcha Cone', 1, 3, 3, 5.49, 'Refreshing mint and matcha ice cream in a cone with whipped cream.', 'https://kid-dev.australiaeast.cloudapp.azure.com/static/images/BBC-Minty-Matcha-Cone-Large.png'),
        ('Strawberry Dream', 2, 1, 5, 3.99, 'Delicious strawberry ice cream in a cup with rainbow sprinkles.', 'https://kid-dev.australiaeast.cloudapp.azure.com/static/images/BBC-Strawberry-Dream-Cup-Small.png'),
        ('Tropical Mango Sandwich', 3, 2, NULL, 4.49, 'Tropical mango ice cream in a sandwich.', 'https://kid-dev.australiaeast.cloudapp.azure.com/static/images/BBC-Tropical-Mango-Sandwich-Medium.png'),
        ('Blueberry Bliss Cone', 1, 3, 4, 5.49, 'Sweet blueberry ice cream in a cone with chopped nuts.', 'https://kid-dev.australiaeast.cloudapp.azure.com/static/images/BBC-Blueberry-Bliss-Cone.png'),
        ('Taro Cupcake', 2, 2, 7, 4.99, 'Unique taro ice cream in a cup with crushed cookies.', 'https://kid-dev.australiaeast.cloudapp.azure.com/static/images/BBC-Taro-Cupcake.png'),
        ('Double Chocolate Chip Cone', 1, 1, 6, 4.49, 'Decadent chocolate ice cream in a cone with chocolate chips.', 'https://kid-dev.australiaeast.cloudapp.azure.com/static/images/BBC-Double-Chocolate.png'),
        ('Matcha Heaven', 2, 3, 9, 5.99, 'Creamy matcha ice cream in a cup with marshmallows.', 'https://kid-dev.australiaeast.cloudapp.azure.com/static/images/BBC-Matcha-Heaven.png'),
        ('Vanilla Strawberry Sandwich', 3, 2, NULL, 4.99, 'Classic vanilla and strawberry ice cream in a sandwich.', 'https://kid-dev.australiaeast.cloudapp.azure.com/static/images/BBC-Vanilla-Strawberry-Sandwich.png'),
        ('Caramel Nut Cone', 1, 2, 1, 4.99, 'Vanilla ice cream in a cone with caramel sauce and chopped nuts.', 'https://kid-dev.australiaeast.cloudapp.azure.com/static/images/BBC-Caramel-Nut-Cone.png'),
        ('Mango Madness Cup', 2, 1, 8, 4.49, 'Refreshing mango ice cream in a cup with tropical fruit slices.', 'https://kid-dev.australiaeast.cloudapp.azure.com/static/images/BBC-Mango-Madness-Cup.png'),
        ('Chocolate Mint Cone', 1, 3, 2, 5.49, 'Cool mint and rich chocolate ice cream in a cone with chocolate syrup.', 'https://kid-dev.australiaeast.cloudapp.azure.com/static/images/BBC-Chocolate-Mint-Cone.png'),
        ('Blueberry Swirl Cup', 2, 2, 3, 4.99, 'Delicious blueberry ice cream in a cup with whipped cream.', 'https://kid-dev.australiaeast.cloudapp.azure.com/static/images/BBC-Blueberry-Swirl-Cup.png'),
        ('Matcha Cookie Sandwich', 3, 2, NULL, 4.49, 'Smooth matcha ice cream in a sandwich.', 'https://kid-dev.australiaeast.cloudapp.azure.com/static/images/BBC-Matcha-Cookie-Sandwich.png'),
        ('Strawberry Delight Cone', 1, 1, 7, 4.49, 'Fresh strawberry ice cream in a cone with crushed cookies.', 'https://kid-dev.australiaeast.cloudapp.azure.com/static/images/BBC-Strawberry-Delight-Cone.png'),
        ('Minty Marshmallow Cup', 2, 3, 9, 5.49, 'Cool mint ice cream in a cup with marshmallows.', 'https://kid-dev.australiaeast.cloudapp.azure.com/static/images/BBC-Minty-Marshmallow-Cup.png'),
        ('Vanilla Berry Cone', 1, 2, 5, 4.99, 'Vanilla and blueberry ice cream in a cone with rainbow sprinkles.', 'https://kid-dev.australiaeast.cloudapp.azure.com/static/images/BBC-Vanilla-Berry-Cone.png'),
        ('Chocolate Mango Sandwich', 3, 3, NULL, 5.49, 'Exotic chocolate and mango ice cream in a sandwich.', 'https://kid-dev.australiaeast.cloudapp.azure.com/static/images/BBC-Chocolate-Mango-Sandwich.png'),
        ('Taro Nut Delight', 2, 2, 4, 4.99, 'Rich taro ice cream in a cup with chopped nuts.', 'https://kid-dev.australiaeast.cloudapp.azure.com/static/images/BBC-Taro-Nut-Delight.png');
    """)

    # Seed ice_cream_flavors
    op.execute("""
        INSERT INTO ice_cream_flavors (flavor_id, ice_cream_id) VALUES
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 3),
        (5, 4),
        (7, 5),
        (6, 6),
        (8, 7),
        (2, 8),
        (4, 9),
        (1, 10),
        (5, 10),
        (1, 11),
        (7, 12),
        (2, 13),
        (3, 13),
        (6, 14),
        (4, 15),
        (5, 16),
        (3, 17),
        (1, 18),
        (6, 18),
        (2, 19),
        (7, 19),
        (8, 20);
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TABLE IF EXISTS order_items;")
    op.execute("DROP TABLE IF EXISTS orders;")
    op.execute("DROP TABLE IF EXISTS ice_cream_flavors;")
    op.execute("DROP TABLE IF EXISTS ice_cream;")
    op.execute("DROP TABLE IF EXISTS flavors;")
    op.execute("DROP TABLE IF EXISTS toppings;")
    op.execute("DROP TABLE IF EXISTS sizes;")
    op.execute("DROP TABLE IF EXISTS types;")
    op.execute("DROP TABLE IF EXISTS users;")
