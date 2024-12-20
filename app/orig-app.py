from flask import Flask, request, jsonify, send_from_directory
import pymysql
from flask_cors import CORS
import os

# Initialize Flask app
app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

# MariaDB Configuration
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "mentges99"),
    "database": os.getenv("DB_NAME", "rodgenix"),
    "port": int(os.getenv("DB_PORT", 3306)),
}

def db_connect():
    """Connect to the MariaDB database."""
    return pymysql.connect(**DB_CONFIG)

### Serve Static Files ###
@app.route('/')
def index():
    """Serve the main page."""
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/src/js/<path:filename>')
def serve_js(filename):
    """Serve JavaScript files."""
    return send_from_directory(f"{app.static_folder}/src/js", filename)

@app.route('/src/css/<path:filename>')
def serve_css(filename):
    """Serve CSS files."""
    return send_from_directory(f"{app.static_folder}/src/css", filename)

### Customers Management ###
@app.route('/customers', methods=['GET', 'POST'])
def customers():
    conn = db_connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    if request.method == 'GET':
        try:
            cursor.execute("SELECT * FROM customers WHERE tenant_id=%s", (request.headers.get("Tenant-ID"),))
            customers = cursor.fetchall()
            return jsonify(customers), 200
        except pymysql.Error as e:
            return jsonify({"error": f"Database error: {e}"}), 500
        finally:
            conn.close()

    if request.method == 'POST':
        data = request.json
        required_fields = ["first_name", "last_name", "email", "address"]

        # Validate request data
        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        if missing_fields:
            return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

        try:
            cursor.execute(
                """
                INSERT INTO customers (tenant_id, first_name, last_name, email, phone, address)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    request.headers.get("Tenant-ID"),
                    data["first_name"],
                    data["last_name"],
                    data["email"],
                    data.get("phone", ""),
                    data["address"],
                ),
            )
            conn.commit()
            return jsonify({"message": "Customer added successfully", "customer_id": cursor.lastrowid}), 201
        except pymysql.Error as e:
            return jsonify({"error": f"Database error: {e}"}), 500
        finally:
            conn.close()

### Quotes Management ###
@app.route('/quotes', methods=['GET', 'POST'])
def quotes():
    conn = db_connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    if request.method == 'GET':
        try:
            cursor.execute("SELECT * FROM quotes WHERE tenant_id=%s", (request.headers.get("Tenant-ID"),))
            quotes = cursor.fetchall()
            return jsonify(quotes), 200
        except pymysql.Error as e:
            return jsonify({"error": f"Database error: {e}"}), 500
        finally:
            conn.close()

    if request.method == 'POST':
        data = request.json
        required_fields = ["customer_id", "total_price"]

        # Validate request data
        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        if missing_fields:
            return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

        try:
            cursor.execute(
                """
                INSERT INTO quotes (tenant_id, customer_id, total_price, status)
                VALUES (%s, %s, %s, %s)
                """,
                (
                    request.headers.get("Tenant-ID"),
                    data["customer_id"],
                    data["total_price"],
                    data.get("status", "Pending"),
                ),
            )
            conn.commit()
            return jsonify({"message": "Quote created successfully", "quote_id": cursor.lastrowid}), 201
        except pymysql.Error as e:
            return jsonify({"error": f"Database error: {e}"}), 500
        finally:
            conn.close()

### Orders Management ###
@app.route('/orders', methods=['GET', 'POST'])
def orders():
    conn = db_connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    if request.method == 'GET':
        try:
            cursor.execute("SELECT * FROM orders WHERE tenant_id=%s", (request.headers.get("Tenant-ID"),))
            orders = cursor.fetchall()
            return jsonify(orders), 200
        except pymysql.Error as e:
            return jsonify({"error": f"Database error: {e}"}), 500
        finally:
            conn.close()

    if request.method == 'POST':
        data = request.json
        required_fields = ["customer_id", "total_price"]

        # Validate request data
        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        if missing_fields:
            return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

        try:
            cursor.execute(
                """
                INSERT INTO orders (tenant_id, customer_id, total_price, status)
                VALUES (%s, %s, %s, %s)
                """,
                (
                    request.headers.get("Tenant-ID"),
                    data["customer_id"],
                    data["total_price"],
                    data.get("status", "Pending"),
                ),
            )
            conn.commit()
            return jsonify({"message": "Order created successfully", "order_id": cursor.lastrowid}), 201
        except pymysql.Error as e:
            return jsonify({"error": f"Database error: {e}"}), 500
        finally:
            conn.close()

### Inventory Management ###
@app.route('/inventory/<item_type>', methods=['GET'])
def inventory(item_type):
    valid_tables = ["blanks", "reel_seats", "guides", "threads", "winding_checks"]
    if item_type not in valid_tables:
        return jsonify({"error": "Invalid inventory type"}), 400

    # Get Tenant-ID and optional blank_id from query parameters
    tenant_id = request.headers.get("Tenant-ID") or request.args.get("tenant_id")
    blank_id = request.args.get("blank_id")  # Optional blank_id

    if not tenant_id:
        return jsonify({"error": "Tenant-ID is required"}), 400

    conn = db_connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    try:
        if blank_id:  # Filter for a specific blank_id
            query = f"SELECT * FROM {item_type} WHERE tenant_id = %s AND blank_id = %s"
            cursor.execute(query, (tenant_id, blank_id))
        else:  # Fetch all blanks for tenant
            query = f"SELECT * FROM {item_type} WHERE tenant_id = %s"
            cursor.execute(query, (tenant_id,))
        
        items = cursor.fetchall()
        return jsonify(items), 200
    except pymysql.Error as e:
        return jsonify({"error": f"Database error: {e}"}), 500
    finally:
        conn.close()

@app.route('/tenants/<tenant_id>/customers', methods=['GET'])
def get_customers(tenant_id):
    # Validate tenant_id
    if not tenant_id:
        return jsonify({"error": "Tenant ID is required"}), 400

    conn = db_connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        # Query to filter customers by tenant_id
        query = "SELECT * FROM customers WHERE tenant_id = %s"
        cursor.execute(query, (tenant_id,))
        customers = cursor.fetchall()
        return jsonify(customers), 200
    except pymysql.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/payments', methods=['GET', 'POST'])
def payments():
    conn = db_connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    if request.method == 'GET':
        try:
            tenant_id = request.headers.get("Tenant-ID")
            cursor.execute("SELECT * FROM payments WHERE tenant_id=%s", (tenant_id,))
            payments = cursor.fetchall()
            return jsonify(payments), 200
        except pymysql.Error as e:
            return jsonify({"error": f"Database error: {e}"}), 500
        finally:
            conn.close()

    if request.method == 'POST':
        data = request.json
        required_fields = ["order_id", "amount_paid", "payment_method"]

        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        if missing_fields:
            return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

        try:
            cursor.execute(
                """
                INSERT INTO payments (tenant_id, order_id, amount_paid, payment_method, payment_date)
                VALUES (%s, %s, %s, %s, NOW())
                """,
                (
                    request.headers.get("Tenant-ID"),
                    data["order_id"],
                    data["amount_paid"],
                    data["payment_method"],
                ),
            )
            conn.commit()
            return jsonify({"message": "Payment added successfully", "payment_id": cursor.lastrowid}), 201
        except pymysql.Error as e:
            return jsonify({"error": f"Database error: {e}"}), 500
        finally:
            conn.close()

@app.route('/photos', methods=['GET', 'POST'])
def photos():
    conn = db_connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    if request.method == 'GET':
        try:
            tenant_id = request.headers.get("Tenant-ID")
            cursor.execute("SELECT * FROM photos WHERE tenant_id=%s", (tenant_id,))
            photos = cursor.fetchall()
            return jsonify(photos), 200
        except pymysql.Error as e:
            return jsonify({"error": f"Database error: {e}"}), 500
        finally:
            conn.close()

    if request.method == 'POST':
        data = request.json
        required_fields = ["related_table", "related_id", "photo_url"]

        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        if missing_fields:
            return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

        try:
            cursor.execute(
                """
                INSERT INTO photos (tenant_id, related_table, related_id, photo_url)
                VALUES (%s, %s, %s, %s)
                """,
                (
                    request.headers.get("Tenant-ID"),
                    data["related_table"],
                    data["related_id"],
                    data["photo_url"],
                ),
            )
            conn.commit()
            return jsonify({"message": "Photo added successfully", "photo_id": cursor.lastrowid}), 201
        except pymysql.Error as e:
            return jsonify({"error": f"Database error: {e}"}), 500
        finally:
            conn.close()

@app.route('/user_interactions', methods=['GET', 'POST'])
def user_interactions():
    conn = db_connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    if request.method == 'GET':
        try:
            tenant_id = request.headers.get("Tenant-ID")
            cursor.execute("SELECT * FROM user_interactions WHERE tenant_id=%s", (tenant_id,))
            interactions = cursor.fetchall()
            return jsonify(interactions), 200
        except pymysql.Error as e:
            return jsonify({"error": f"Database error: {e}"}), 500
        finally:
            conn.close()

    if request.method == 'POST':
        data = request.json
        required_fields = ["user_id", "component_id", "action_type"]

        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        if missing_fields:
            return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

        try:
            cursor.execute(
                """
                INSERT INTO user_interactions (tenant_id, user_id, component_id, action_type, timestamp)
                VALUES (%s, %s, %s, %s, NOW())
                """,
                (
                    request.headers.get("Tenant-ID"),
                    data["user_id"],
                    data["component_id"],
                    data["action_type"],
                ),
            )
            conn.commit()
            return jsonify({"message": "Interaction logged successfully", "interaction_id": cursor.lastrowid}), 201
        except pymysql.Error as e:
            return jsonify({"error": f"Database error: {e}"}), 500
        finally:
            conn.close()

@app.route('/compatibility', methods=['GET', 'POST'])
def compatibility():
    conn = db_connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    if request.method == 'GET':
        try:
            tenant_id = request.headers.get("Tenant-ID")
            cursor.execute("SELECT * FROM component_compatibility WHERE tenant_id=%s", (tenant_id,))
            compatibility = cursor.fetchall()
            return jsonify(compatibility), 200
        except pymysql.Error as e:
            return jsonify({"error": f"Database error: {e}"}), 500
        finally:
            conn.close()

    if request.method == 'POST':
        data = request.json
        required_fields = ["component_a_id", "component_b_id", "compatibility_score"]

        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        if missing_fields:
            return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

        try:
            cursor.execute(
                """
                INSERT INTO component_compatibility (tenant_id, component_a_id, component_b_id, compatibility_score)
                VALUES (%s, %s, %s, %s)
                """,
                (
                    request.headers.get("Tenant-ID"),
                    data["component_a_id"],
                    data["component_b_id"],
                    data["compatibility_score"],
                ),
            )
            conn.commit()
            return jsonify({"message": "Compatibility score added successfully", "compatibility_id": cursor.lastrowid}), 201
        except pymysql.Error as e:
            return jsonify({"error": f"Database error: {e}"}), 500
        finally:
            conn.close()

@app.route('/forecasts', methods=['GET', 'POST'])
def forecasts():
    conn = db_connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    if request.method == 'GET':
        try:
            tenant_id = request.headers.get("Tenant-ID")
            cursor.execute("SELECT * FROM inventory_forecasts WHERE tenant_id=%s", (tenant_id,))
            forecasts = cursor.fetchall()
            return jsonify(forecasts), 200
        except pymysql.Error as e:
            return jsonify({"error": f"Database error: {e}"}), 500
        finally:
            conn.close()

    if request.method == 'POST':
        data = request.json
        required_fields = ["component_id", "forecast_date", "predicted_demand"]

        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        if missing_fields:
            return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

        try:
            cursor.execute(
                """
                INSERT INTO inventory_forecasts (tenant_id, component_id, forecast_date, predicted_demand, actual_demand)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    request.headers.get("Tenant-ID"),
                    data["component_id"],
                    data["forecast_date"],
                    data["predicted_demand"],
                    data.get("actual_demand"),  # Optional
                ),
            )
            conn.commit()
            return jsonify({"message": "Forecast added successfully", "forecast_id": cursor.lastrowid}), 201
        except pymysql.Error as e:
            return jsonify({"error": f"Database error: {e}"}), 500
        finally:
            conn.close()

@app.route('/nlp_queries', methods=['GET', 'POST'])
def nlp_queries():
    conn = db_connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    if request.method == 'GET':
        try:
            tenant_id = request.headers.get("Tenant-ID")
            cursor.execute("SELECT * FROM nlp_query_mapping WHERE tenant_id=%s", (tenant_id,))
            queries = cursor.fetchall()
            return jsonify(queries), 200
        except pymysql.Error as e:
            return jsonify({"error": f"Database error: {e}"}), 500
        finally:
            conn.close()

    if request.method == 'POST':
        data = request.json
        required_fields = ["query", "mapped_action"]

        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        if missing_fields:
            return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

        try:
            cursor.execute(
                """
                INSERT INTO nlp_query_mapping (tenant_id, query, mapped_action, created_at)
                VALUES (%s, %s, %s, NOW())
                """,
                (
                    request.headers.get("Tenant-ID"),
                    data["query"],
                    data["mapped_action"],
                ),
            )
            conn.commit()
            return jsonify({"message": "NLP query added successfully", "query_id": cursor.lastrowid}), 201
        except pymysql.Error as e:
            return jsonify({"error": f"Database error: {e}"}), 500
        finally:
            conn.close()

@app.route('/ai_models', methods=['GET', 'POST'])
def ai_models():
    conn = db_connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    if request.method == 'GET':
        try:
            cursor.execute("SELECT * FROM ai_model_metadata")
            models = cursor.fetchall()
            return jsonify(models), 200
        except pymysql.Error as e:
            return jsonify({"error": f"Database error: {e}"}), 500
        finally:
            conn.close()

    if request.method == 'POST':
        data = request.json
        required_fields = ["model_name", "version", "last_trained", "metrics"]

        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        if missing_fields:
            return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

        try:
            cursor.execute(
                """
                INSERT INTO ai_model_metadata (model_name, version, last_trained, metrics, deployed_at)
                VALUES (%s, %s, %s, %s, NOW())
                """,
                (
                    data["model_name"],
                    data["version"],
                    data["last_trained"],
                    data["metrics"],
                ),
            )
            conn.commit()
            return jsonify({"message": "AI model metadata added successfully", "model_id": cursor.lastrowid}), 201
        except pymysql.Error as e:
            return jsonify({"error": f"Database error: {e}"}), 500
        finally:
            conn.close()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
