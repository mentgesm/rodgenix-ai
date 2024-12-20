# Rodgenix Application

Rodgenix is a multi-tenant application designed for custom fishing rod builders to manage inventory, create quotes, and process orders. The application leverages Flask for the backend, MariaDB for the database, and Docker for containerization, with a goal to achieve a functional MVP by February 2025.

---

## **Ownership and NDA**
This codebase is proprietary and owned by **Mentges Outdoors LLC**. By viewing or using this repository, you automatically agree to the **Non-Disclosure Agreement (NDA)** provided by Mentges Outdoors LLC.

---

## **Project Structure**

The project is organized into a modular structure to maintain scalability and readability.

```
├── app
│   ├── administration.py      # Placeholder for admin-level management
│   ├── ai_models.py           # CRUD operations for AI model metadata
│   ├── app.py                 # Main Flask application entry point
│   ├── compatibility.py       # CRUD for compatibility scores
│   ├── customers.py           # CRUD for customer management
│   ├── db.py                  # Database connection logic
│   ├── forecasts.py           # CRUD for inventory forecasts
│   ├── inventory.py           # CRUD for all inventory-related tables
│   ├── nlp_queries.py         # CRUD for natural language query mappings
│   ├── orders.py              # CRUD for customer orders
│   ├── orig-app.py            # Original version of app.py (backup)
│   ├── payments.py            # CRUD for payment processing
│   ├── photos.py              # CRUD for photos related to inventory and orders
│   ├── quotes.py              # CRUD for customer quotes
│   ├── requirements.txt       # Python dependencies
│   ├── tenants.py             # CRUD for tenant management
│   └── user_interactions.py   # CRUD for tracking user actions
├── docker-compose.yaml         # Docker Compose configuration
├── dockerfile                  # Docker image configuration
├── dummy_data.sql              # SQL script for populating dummy data
├── frontend
│   ├── api_explorer.html       # Interactive API endpoint explorer
│   ├── css/
│   │   └── styles.css          # Global styles for the frontend
│   ├── index.html              # Landing page for the application
│   ├── js/
│   │   └── tenants.js          # JavaScript for tenant management
│   └── tenants.html            # Tenant management page
├── postman_collection.json     # Postman collection for testing API endpoints
├── rodgenix_database_schema.sql # Database schema definition
└── tests.py                    # API endpoint test script
```

---

## **Database Diagram**

### **Entity Relationship Overview**
```plaintext
+----------------+       +--------------+       +-------------+
| customers      |       | quotes       |       | orders      |
|----------------|       |--------------|       |-------------|
| customer_id PK |<--+   | quote_id PK  |<--+   | order_id PK |
| tenant_id FK   |   |   | customer_id  |   |   | customer_id |
| first_name     |   |   | total_price  |   |   | total_price |
| last_name      |   |   | status       |   |   | status      |
+----------------+   |   +--------------+   |   +-------------+
                     |                      |
                     |                      +-->
                     |                      +-------------+
                     |                      | payments    |
                     |                      |-------------|
                     |                      | payment_id PK |
                     |                      | order_id FK |
                     +--------------------->| amount_paid |
                                            | payment_date|
                                            +-------------+

+------------------+
| inventory        |
|------------------|
| qb_item_id PK    |
| tenant_id FK     |
| name             |
| brand            |
| quantity         |
| price            |
+------------------+

+---------------------+
| blanks              |
|---------------------|
| blank_id PK         |
| tenant_id FK        |
| qb_item_id          |
| name                |
| brand               |
| length              |
| power               |
| action              |
| quantity            |
| price               |
+---------------------+

+---------------------+
| guides              |
|---------------------|
| guide_id PK         |
| tenant_id FK        |
| qb_item_id          |
| name                |
| brand               |
| size                |
| material            |
| vendor              |
| cost                |
| quantity            |
| price               |
+---------------------+

+---------------------+
| threads             |
|---------------------|
| thread_id PK        |
| tenant_id FK        |
| qb_item_id          |
| thread_color_id     |
| color_name          |
| brand               |
| type                |
| quantity            |
| price               |
+---------------------+

+---------------------+
| reel_seats          |
|---------------------|
| reel_seat_id PK     |
| tenant_id FK        |
| qb_item_id          |
| name                |
| brand               |
| type                |
| material            |
| color               |
| quantity            |
| price               |
+---------------------+

+---------------------+
| winding_checks      |
|---------------------|
| winding_check_id PK |
| tenant_id FK        |
| qb_item_id          |
| size                |
| material            |
| color               |
| quantity            |
| price               |
+---------------------+

+---------------------+
| ai_model_metadata   |
|---------------------|
| model_id PK         |
| model_name          |
| version             |
| last_trained        |
| metrics             |
| deployed_at         |
+---------------------+

+---------------------+
| nlp_query_mapping   |
|---------------------|
| query_id PK         |
| tenant_id FK        |
| query               |
| mapped_action       |
| created_at          |
+---------------------+
```

This schema supports multi-tenancy through the `tenant_id` field in most tables, ensuring data isolation between tenants.

---

## **Features**

### **Current Features (MVP)**
- Full CRUD functionality for:
  - Inventory (blanks, guides, threads, reel seats, winding checks, etc.)
  - Customer management
  - Quotes, Orders, and Payments
  - AI Model metadata and NLP query mappings
- Multi-tenant architecture with `tenant_id` ensuring data separation.
- Dockerized deployment for consistent development and production environments.

### **Planned Features**
- **Authentication**: Add user authentication and role-based access control.
- **Crafty HTML Interface**: Design a user-friendly front-end interface for CRUD operations.
- **Analytics**: Add advanced reporting for customer and order data.
- **API Enhancements**: Include filtering, sorting, and pagination for large datasets.

---

## **Installation and Setup**

### **Requirements**
- Docker
- Docker Compose
- Python 3.9

### **Steps**
1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd rodgenix-ai
   ```

2. Build and run the Docker containers:
   ```bash
   docker-compose up --build
   ```

3. Verify the application is running:
   ```bash
   curl http://127.0.0.1:5001/customers
   ```

4. Populate the database with dummy data (optional):
   ```bash
   docker exec -i <db_container_name> mysql -u root -p rodgenix-ai < dummy_data.sql
   ```

---

## **Usage**

### **API Endpoints**
#### **Customers**
- `GET /customers`: Retrieve all customers.
- `POST /customers`: Add a new customer.
- `PUT /customers/<customer_id>`: Update a customer.
- `DELETE /customers/<customer_id>`: Delete a customer.

#### **Quotes**
- `GET /quotes`: Retrieve all quotes.
- `POST /quotes`: Add a new quote.

(Additional endpoints follow a similar pattern for other resources.)

### **HTML Interface**
#### **Landing Page**
The landing page provides access to the admin dashboard and tenant management:
- **URL**: `http://127.0.0.1:5001/`

#### **API Explorer**
A dynamic page for exploring API endpoints:
- **URL**: `http://127.0.0.1:5001/api_explorer.html`

---

## **Postman Setup**
#### **Postman Collection**
A preconfigured Postman collection is available for testing API endpoints:
- **File**: `postman_collection.json`
- **Steps to Import**:
  1. Open Postman.
  2. Click **Import**.
  3. Select the `postman_collection.json` file.
  4. Use the configured requests to interact with the API.

#### **Example Requests**
- **GET Customers**:
  - Method: `GET`
  - URL: `http://127.0.0.1:5001/customers`
  - Headers:
    - `Tenant-ID: tenant-12345`

---

## **Contributing**
We welcome contributions! Please follow these steps:
1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes and push:
   ```bash
   git push origin feature-name
   ```
4. Open a pull request.

---

## **License**
This project is licensed under the MIT License. See the `LICENSE` file for details.
