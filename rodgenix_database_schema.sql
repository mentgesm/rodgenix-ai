-- Drop existing tables if they exist
DROP TABLE IF EXISTS blanks;
DROP TABLE IF EXISTS guides;
DROP TABLE IF EXISTS threads;
DROP TABLE IF EXISTS reel_seats;
DROP TABLE IF EXISTS winding_checks;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS quotes;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS payments;
DROP TABLE IF EXISTS photos;
DROP TABLE IF EXISTS user_interactions;
DROP TABLE IF EXISTS component_compatibility;
DROP TABLE IF EXISTS inventory_forecasts;
DROP TABLE IF EXISTS nlp_query_mapping;
DROP TABLE IF EXISTS ai_model_metadata;
DROP TABLE IF EXISTS customers_metadata;

-- Create blanks table
CREATE TABLE blanks (
    blank_id INT AUTO_INCREMENT PRIMARY KEY,
    qb_item_id VARCHAR(50) UNIQUE,
    tenant_id CHAR(36) NOT NULL,
    name VARCHAR(100) NOT NULL,
    brand VARCHAR(100),
    length DECIMAL(5, 2),
    power VARCHAR(50),
    action VARCHAR(50),
    quantity INT DEFAULT 0,
    price DECIMAL(10, 2) NOT NULL,
    UNIQUE KEY (blank_id, tenant_id)
);

-- Create guides table
CREATE TABLE guides (
    guide_id INT AUTO_INCREMENT PRIMARY KEY,
    qb_item_id VARCHAR(50) UNIQUE,
    tenant_id CHAR(36) NOT NULL,
    name VARCHAR(100) NOT NULL,
    brand VARCHAR(100),
    size VARCHAR(50),
    material VARCHAR(50),
    vendor VARCHAR(100),
    cost DECIMAL(10, 2),
    quantity INT DEFAULT 0,
    price DECIMAL(10, 2) NOT NULL
);

-- Create threads table
CREATE TABLE threads (
    thread_id INT AUTO_INCREMENT PRIMARY KEY,
    qb_item_id VARCHAR(50) UNIQUE,
    tenant_id CHAR(36) NOT NULL,
    thread_color_id VARCHAR(50) NOT NULL,
    color_name VARCHAR(100) NOT NULL,
    brand VARCHAR(100),
    type VARCHAR(50),
    quantity INT DEFAULT 0,
    price DECIMAL(10, 2) NOT NULL
);

-- Create reel_seats table
CREATE TABLE reel_seats (
    reel_seat_id INT AUTO_INCREMENT PRIMARY KEY,
    qb_item_id VARCHAR(50) UNIQUE,
    tenant_id CHAR(36) NOT NULL,
    name VARCHAR(100) NOT NULL,
    brand VARCHAR(100),
    type VARCHAR(50),
    material VARCHAR(50),
    color VARCHAR(50),
    quantity INT DEFAULT 0,
    price DECIMAL(10, 2) NOT NULL
);

-- Create winding_checks table
CREATE TABLE winding_checks (
    winding_check_id INT AUTO_INCREMENT PRIMARY KEY,
    qb_item_id VARCHAR(50) UNIQUE,
    tenant_id CHAR(36) NOT NULL,
    size VARCHAR(50) NOT NULL,
    material VARCHAR(50),
    color VARCHAR(50),
    quantity INT DEFAULT 0,
    price DECIMAL(10, 2) NOT NULL
);

-- Create customers table with a composite unique key
CREATE TABLE customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    tenant_id CHAR(36) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(15),
    address VARCHAR(255),
    UNIQUE KEY (customer_id, tenant_id) -- Composite unique key for referencing
);

-- Create quotes table
CREATE TABLE quotes (
    quote_id INT AUTO_INCREMENT PRIMARY KEY,
    tenant_id CHAR(36) NOT NULL,
    customer_id INT NOT NULL,
    total_price DECIMAL(10, 2) NOT NULL,
    status VARCHAR(50) DEFAULT 'Pending',
    FOREIGN KEY (customer_id, tenant_id) REFERENCES customers(customer_id, tenant_id)
);

-- Create orders table
CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    tenant_id CHAR(36) NOT NULL,
    customer_id INT NOT NULL,
    total_price DECIMAL(10, 2) NOT NULL,
    status VARCHAR(50) DEFAULT 'Pending',
    order_date DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (customer_id, tenant_id) REFERENCES customers(customer_id, tenant_id)
);

-- Create payments table
CREATE TABLE payments (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    tenant_id CHAR(36) NOT NULL,
    order_id INT NOT NULL,
    amount_paid DECIMAL(10, 2) NOT NULL,
    payment_method VARCHAR(50),
    payment_date DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

-- Create photos table
CREATE TABLE photos (
    photo_id INT AUTO_INCREMENT PRIMARY KEY,
    tenant_id CHAR(36) NOT NULL,
    related_table VARCHAR(50) NOT NULL,
    related_id INT NOT NULL,
    photo_url VARCHAR(255) NOT NULL
);

-- Create user_interactions table for tracking user actions
CREATE TABLE user_interactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tenant_id CHAR(36) NOT NULL,
    user_id INT NOT NULL,
    component_id INT NOT NULL,
    action_type ENUM('view', 'select', 'order') NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id, tenant_id) REFERENCES customers(customer_id, tenant_id)
);

-- Create component_compatibility table
CREATE TABLE component_compatibility (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tenant_id CHAR(36) NOT NULL,
    component_a_id INT NOT NULL,
    component_b_id INT NOT NULL,
    compatibility_score DECIMAL(3, 2) DEFAULT 0.00,
    FOREIGN KEY (component_a_id, tenant_id) REFERENCES blanks(blank_id, tenant_id),
    FOREIGN KEY (component_b_id, tenant_id) REFERENCES blanks(blank_id, tenant_id)
);

-- Create inventory_forecasts table for AI-driven inventory predictions
CREATE TABLE inventory_forecasts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tenant_id CHAR(36) NOT NULL,
    component_id INT NOT NULL,
    forecast_date DATE NOT NULL,
    predicted_demand INT NOT NULL,
    actual_demand INT DEFAULT NULL,
    FOREIGN KEY (component_id, tenant_id) REFERENCES blanks(blank_id, tenant_id)
);

-- Create nlp_query_mapping table for mapping natural language queries
CREATE TABLE nlp_query_mapping (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tenant_id CHAR(36) NOT NULL,
    query TEXT NOT NULL,
    mapped_action TEXT NOT NULL, -- JSON or configuration reference
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Create ai_model_metadata table for tracking AI model deployments
CREATE TABLE ai_model_metadata (
    id INT AUTO_INCREMENT PRIMARY KEY,
    model_name VARCHAR(255) NOT NULL,
    version VARCHAR(50) NOT NULL,
    last_trained DATETIME,
    metrics JSON,
    deployed_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Create customers_metadata table for central tenant database management
CREATE TABLE customers_metadata (
    tenant_id CHAR(36) PRIMARY KEY,
    db_host VARCHAR(255) NOT NULL,
    db_name VARCHAR(255) NOT NULL,
    db_user VARCHAR(255) NOT NULL,
    db_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
