from flask import Blueprint, request, jsonify
from db import db_connect
import pymysql


customers_bp = Blueprint("customers", __name__)

@customers_bp.route('/customers', methods=['GET', 'POST'])
def list_or_create_customers():
    conn = db_connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    if request.method == 'GET':
        try:
            tenant_id = request.headers.get("Tenant-ID")
            cursor.execute("SELECT * FROM customers WHERE tenant_id=%s", (tenant_id,))
            customers = cursor.fetchall()
            return jsonify(customers), 200
        except pymysql.Error as e:
            return jsonify({"error": f"Database error: {e}"}), 500
        finally:
            conn.close()

    if request.method == 'POST':
        data = request.json
        required_fields = ["first_name", "last_name", "email", "address"]

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
            return jsonify({"message": "Customer created successfully.", "customer_id": cursor.lastrowid}), 201
        except pymysql.Error as e:
            return jsonify({"error": f"Database error: {e}"}), 500
        finally:
            conn.close()

@customers_bp.route('/customers/<int:customer_id>', methods=['GET', 'PUT', 'DELETE'])
def manage_customer(customer_id):
    conn = db_connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    tenant_id = request.headers.get("Tenant-ID")

    if not tenant_id:
        return jsonify({"error": "Tenant-ID is required."}), 400

    if request.method == 'GET':
        try:
            cursor.execute("SELECT * FROM customers WHERE tenant_id=%s AND customer_id=%s", (tenant_id, customer_id))
            customer = cursor.fetchone()
            if not customer:
                return jsonify({"error": "Customer not found."}), 404
            return jsonify(customer), 200
        except pymysql.Error as e:
            return jsonify({"error": f"Database error: {e}"}), 500
        finally:
            conn.close()

    if request.method == 'PUT':
        data = request.json
        required_fields = ["first_name", "last_name", "email", "address"]

        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        if missing_fields:
            return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

        try:
            cursor.execute(
                """
                UPDATE customers
                SET first_name=%s, last_name=%s, email=%s, phone=%s, address=%s
                WHERE tenant_id=%s AND customer_id=%s
                """,
                (
                    data["first_name"],
                    data["last_name"],
                    data["email"],
                    data.get("phone", ""),
                    data["address"],
                    tenant_id,
                    customer_id,
                ),
            )
            conn.commit()
            if cursor.rowcount == 0:
                return jsonify({"error": "Customer not found or no changes made."}), 404
            return jsonify({"message": "Customer updated successfully."}), 200
        except pymysql.Error as e:
            return jsonify({"error": f"Database error: {e}"}), 500
        finally:
            conn.close()

    if request.method == 'DELETE':
        try:
            cursor.execute("DELETE FROM customers WHERE tenant_id=%s AND customer_id=%s", (tenant_id, customer_id))
            conn.commit()
            if cursor.rowcount == 0:
                return jsonify({"error": "Customer not found."}), 404
            return jsonify({"message": "Customer deleted successfully."}), 200
        except pymysql.Error as e:
            return jsonify({"error": f"Database error: {e}"}), 500
        finally:
            conn.close()
