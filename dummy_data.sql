-- Insert dummy data for tenants
INSERT INTO customers_metadata (tenant_id, db_host, db_name, db_user, db_password) VALUES
('tenant-12345', 'localhost', 'rodgenix', 'root', 'securepassword'),
('tenant-67890', 'localhost', 'rodgenix', 'root', 'securepassword');

-- Insert dummy data into customers table
INSERT INTO customers (tenant_id, first_name, last_name, email, phone, address) VALUES
('tenant-12345', 'John', 'Doe', 'john.doe@example.com', '123-456-7890', '123 Main St'),
('tenant-12345', 'Jane', 'Smith', 'jane.smith@example.com', '987-654-3210', '456 Elm St'),
('tenant-67890', 'Bob', 'Williams', 'bob.williams@example.com', '555-555-5555', '789 Oak Ave');

INSERT INTO blanks (tenant_id, blank_id, qb_item_id, name, brand, length, power, action, quantity, price) VALUES
('tenant-12345', 1, 'BLANK001', 'Pro Series Blank', 'BrandA', 7.5, 'Medium', 'Fast', 10, 45.99),
('tenant-12345', 2, 'BLANK002', 'Ultra Light Blank', 'BrandB', 6.0, 'Light', 'Moderate', 5, 29.99),
('tenant-12345', 3, 'BLANK003', 'Heavy Duty Blank', 'BrandC', 8.0, 'Heavy', 'Extra Fast', 12, 59.99),
('tenant-67890', 3, 'BLANK004', 'High Power Blank', 'BrandD', 9.0, 'Extra Heavy', 'Extra Fast', 4, 69.99),
('tenant-67890', 1, 'BLANK005', 'Standard Blank', 'BrandE', 7.0, 'Medium', 'Moderate', 8, 39.99);

-- Ensure blank_ids match the generated IDs from AUTO_INCREMENT
SET @blank1 = 1;
SET @blank2 = 2;
SET @blank3 = 3;

-- Insert dummy data into guides table
INSERT INTO guides (tenant_id, qb_item_id, name, brand, size, material, vendor, cost, quantity, price) VALUES
('tenant-12345', 'GUIDE001', 'Titanium Guide', 'BrandX', 'M', 'Titanium', 'VendorA', 5.50, 50, 8.99),
('tenant-67890', 'GUIDE002', 'Ceramic Guide', 'BrandY', 'L', 'Ceramic', 'VendorB', 3.75, 30, 6.99);

-- Insert dummy data into threads table
INSERT INTO threads (tenant_id, qb_item_id, thread_color_id, color_name, brand, type, quantity, price) VALUES
('tenant-12345', 'THREAD001', 'RED001', 'Red', 'BrandT', 'Nylon', 100, 1.99),
('tenant-67890', 'THREAD002', 'BLU002', 'Blue', 'BrandU', 'Polyester', 200, 2.49);

INSERT INTO component_compatibility (tenant_id, component_a_id, component_b_id, compatibility_score) VALUES
('tenant-12345', 1, 2, 0.85),
('tenant-12345', 2, 3, 0.90),
('tenant-67890', 3, 1, 0.80);

-- Insert dummy data into inventory_forecasts table
INSERT INTO inventory_forecasts (tenant_id, component_id, forecast_date, predicted_demand, actual_demand) VALUES
('tenant-12345', @blank1, '2024-01-15', 20, 18),
('tenant-67890', @blank3, '2024-01-20', 30, NULL);

-- Insert dummy data into reel_seats table
INSERT INTO reel_seats (tenant_id, qb_item_id, name, brand, type, material, color, quantity, price) VALUES
('tenant-12345', 'REEL001', 'Graphite Seat', 'BrandG', 'Spinning', 'Graphite', 'Black', 15, 12.99),
('tenant-67890', 'REEL002', 'Aluminum Seat', 'BrandH', 'Casting', 'Aluminum', 'Silver', 10, 14.99);

-- Insert dummy data into winding_checks table
INSERT INTO winding_checks (tenant_id, qb_item_id, size, material, color, quantity, price) VALUES
('tenant-12345', 'WIND001', 'M', 'Metal', 'Silver', 25, 0.99),
('tenant-67890', 'WIND002', 'L', 'Plastic', 'Black', 30, 0.79);

-- Insert dummy data into quotes table
INSERT INTO quotes (tenant_id, customer_id, total_price, status) VALUES
('tenant-12345', 1, 99.99, 'Pending'),
('tenant-12345', 2, 149.99, 'Converted'),
('tenant-67890', 3, 89.50, 'Pending');

-- Insert dummy data into orders table
INSERT INTO orders (tenant_id, customer_id, total_price, status, order_date) VALUES
('tenant-12345', 1, 99.99, 'Shipped', '2024-01-01'),
('tenant-12345', 2, 149.99, 'Pending', '2024-01-10'),
('tenant-67890', 3, 89.50, 'Completed', '2024-01-05');

-- Insert dummy data into payments table
INSERT INTO payments (tenant_id, order_id, amount_paid, payment_method, payment_date) VALUES
('tenant-12345', 1, 99.99, 'Credit Card', '2024-01-02'),
('tenant-67890', 3, 89.50, 'PayPal', '2024-01-06');

-- Insert dummy data into photos table
INSERT INTO photos (tenant_id, related_table, related_id, photo_url) VALUES
('tenant-12345', 'blanks', 1, 'http://example.com/photos/blank1.jpg'),
('tenant-67890', 'guides', 2, 'http://example.com/photos/guide2.jpg');

-- Insert dummy data into user_interactions table
INSERT INTO user_interactions (tenant_id, user_id, component_id, action_type, timestamp) VALUES
('tenant-12345', 1, @blank1, 'view', NOW()),
('tenant-67890', 3, @blank2, 'order', NOW());

-- Insert dummy data into nlp_query_mapping table
INSERT INTO nlp_query_mapping (tenant_id, query, mapped_action, created_at) VALUES
('tenant-12345', 'show all blanks', '{"action": "fetch_blanks"}', NOW()),
('tenant-67890', 'list guides', '{"action": "fetch_guides"}', NOW());

-- Insert dummy data into ai_model_metadata table
INSERT INTO ai_model_metadata (model_name, version, last_trained, metrics, deployed_at) VALUES
('Rodgenix-AI', 'v1.0', '2024-01-01 00:00:00', '{"accuracy": 95.5, "precision": 92.3}', NOW());

-- Insert test data into component_compatibility
INSERT INTO component_compatibility (tenant_id, component_a_id, component_b_id, compatibility_score) VALUES
('tenant-12345', 1, 2, 0.85),
('tenant-12345', 2, 3, 0.90),
('tenant-67890', 3, 1, 0.80);

-- Insert test data into inventory_forecasts
INSERT INTO inventory_forecasts (tenant_id, component_id, forecast_date, predicted_demand, actual_demand) VALUES
('tenant-12345', 1, '2024-01-15', 20, 18),
('tenant-12345', 2, '2024-01-20', 15, NULL),
('tenant-67890', 3, '2024-01-25', 25, 22);

-- Insert test data into nlp_query_mapping
INSERT INTO nlp_query_mapping (tenant_id, query, mapped_action, created_at) VALUES
('tenant-12345', 'show all blanks', '{"action": "fetch_blanks"}', NOW()),
('tenant-12345', 'list guides', '{"action": "fetch_guides"}', NOW()),
('tenant-67890', 'fetch threads', '{"action": "fetch_threads"}', NOW());

-- Insert test data into ai_model_metadata
INSERT INTO ai_model_metadata (model_name, version, last_trained, metrics, deployed_at) VALUES
('Rodgenix-AI', 'v1.0', '2024-01-01 00:00:00', '{"accuracy": 95.5, "precision": 92.3}', NOW()),
('Rodgenix-AI', 'v1.1', '2024-01-10 00:00:00', '{"accuracy": 96.0, "precision": 93.0}', NOW());

