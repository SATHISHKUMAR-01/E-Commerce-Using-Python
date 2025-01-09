CREATE TABLE user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    dob DATE NOT NULL,
    phone_number VARCHAR(15) NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE vendor (
    vendor_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    company_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone_number VARCHAR(15) NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    company VARCHAR(255) NOT NULL,
    category VARCHAR(255) NOT NULL,
    sub_category VARCHAR(255) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    count INT NOT NULL
);

ALTER TABLE products
DROP COLUMN weight;

CREATE TABLE discount (
    discount_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT, -- Foreign key reference to products table
    discount_type VARCHAR(255) NOT NULL,
    buy_val INT DEFAULT 0, -- Default value set to 0
    get_val INT DEFAULT 0, -- Default value set to 0
    flat_percentage DECIMAL(10,2) DEFAULT 0.00, -- Default value set to 0.00

    -- Foreign key constraint
    CONSTRAINT fk_product
        FOREIGN KEY (product_id)
        REFERENCES products(id)
        ON DELETE CASCADE -- Ensures related discounts are deleted if product is deleted
);

CREATE TABLE cart (
    cart_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT, -- Foreign key reference to products table
    user_id INT, -- Foreign key reference to user table
    count INT DEFAULT 1, -- Default value set to 1

    -- Foreign key constraints
    CONSTRAINT fk_products
        FOREIGN KEY (product_id)
        REFERENCES products(id)
        ON DELETE CASCADE, -- Comma added here

    CONSTRAINT fk_user
        FOREIGN KEY (user_id)
        REFERENCES user(id)
        ON DELETE CASCADE -- No comma here (last line)
);

CREATE TABLE wishlist (
    wishlist_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT, -- Foreign key reference to products table
    user_id INT, -- Foreign key reference to user table
    count INT DEFAULT 1, -- Default value set to 1

    -- Foreign key constraints
    CONSTRAINT fk_wishlist
        FOREIGN KEY (product_id)
        REFERENCES products(id)
        ON DELETE CASCADE, -- Comma added here

    CONSTRAINT fk_users
        FOREIGN KEY (user_id)
        REFERENCES user(id)
        ON DELETE CASCADE -- No comma here (last line)
);

CREATE TABLE review (
    review_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT, -- Foreign key reference to products table
    user_id INT, -- Foreign key reference to users table
    comments VARCHAR(255) NOT NULL,
    rating INT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Use TIMESTAMP with default value

    -- Foreign key constraints
    CONSTRAINT fk_review_product
        FOREIGN KEY (product_id)
        REFERENCES products(id)
        ON DELETE CASCADE, -- <-- Added comma here

    CONSTRAINT fk_review_users
        FOREIGN KEY (user_id)
        REFERENCES user(id)
        ON DELETE CASCADE -- No comma here (last line)
);


ALTER TABLE user
ADD COLUMN state VARCHAR(100) NOT NULL,
ADD COLUMN city VARCHAR(100) NOT NULL,
ADD COLUMN pincode VARCHAR(10) NOT NULL,
ADD COLUMN address VARCHAR(500) NOT NULL;


CREATE TABLE shipping_address (
    order_id VARCHAR(30), -- Reference to Orders table
    name VARCHAR(255) NOT NULL, -- Recipient name
    phone_number VARCHAR(15) NOT NULL,
    state VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    pincode VARCHAR(10) NOT NULL,
    address VARCHAR(500) NOT NULL,
    is_gift BOOLEAN DEFAULT FALSE, -- True if buying for someone else

    -- Foreign Key Constraint
    CONSTRAINT fk_shipping_address_order
        FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE
);

CREATE TABLE orders (
    order_id VARCHAR(30) PRIMARY KEY,
    user_id INT, -- Buyer user ID
    total_amount DECIMAL(10, 2) NOT NULL,
    order_status VARCHAR(50) DEFAULT 'Pending',
    payment_status VARCHAR(50) DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Foreign Key Constraint
    CONSTRAINT fk_orders_user
        FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
);

CREATE TABLE wallet (
    wallet_id VARCHAR(50) PRIMARY KEY,
    user_id INT, -- Buyer user ID
    amount DECIMAL(10, 2) NOT NULL,
    
    CONSTRAINT fk_wallet_user
        FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
);


ALTER TABLE orders
ADD COLUMN product_id INT DEFAULT NULL;

UPDATE orders
SET product_id = 2

ALTER TABLE orders
MODIFY COLUMN product_id INT NOT NULL;

ALTER TABLE orders
ADD CONSTRAINT fk_orders_product
FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE;

CREATE TABLE return_table (
    return_id VARCHAR(50) PRIMARY KEY,
    order_id VARCHAR(30), -- Reference to Orders table
    reason VARCHAR(255) NOT NULL,
    return_status VARCHAR(50) DEFAULT 'Pending',

    -- Foreign Key Constraint
    CONSTRAINT fk_return
        FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE
);