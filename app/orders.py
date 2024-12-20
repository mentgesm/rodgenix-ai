from flask import Blueprint, request, jsonify
from db import db_connect
import pymysql


orders_bp = Blueprint("orders", __name__)

@orders_bp.route('/orders', methods=['GET', 'POST'])
def list_or_create_orders():
    conn = db_connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    if request.method == 'GET':
        try:
            tenant_id = request.headers.get("Tenant-ID")
            cursor.execute("SELECT * FROM orders WHERE tenant_id=%s", (tenant_id,))
            orders = cursor.fetchall()
            return jsonify(orders), 200
        except pymysql.Error as e:
            return jsonify({"error": f"Database error: {e}"}), 500
        finally:
            conn.close()

    if request.method == 'POST':
        data = request.json
        required_fields = ["customer_id", "total_price", "status"]

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
                    data["status"],
                ),
            )
            conn.commit()
            return jsonify({"message": "Order created successfully.", "order_id": cursor.lastrowid}), 201
        except pymysql.Error as e:
            return jsonify({"error": f"Database error: {e}"}), 500
        finally:
            conn.close()

@orders_bp.route('/orders/<int:order_id>', methods=['GET', 'PUT', 'DELETE'])
def manage_order(order_id):
    conn = db_connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    tenant_id = request.headers.get("Tenant-ID")

    if not tenant_id:
        return jsonify({"error": "Tenant-ID is required."}), 400

    if request.method == 'GET':
        try:
            cursor.execute("SELECT * FROM orders WHERE tenant_id=%s AND order_id=%s", (tenant_id, order_id))
            order = cursor.fetchone()
            if not order:
                return jsonify({"error": "Order not found."}), 404
            return jsonify(order), 200
        except pymysql.Error as e:
            return jsonify({"error": f"Database error: {e}"}), 500
        finally:
            conn.close()

    if request.method == 'PUT':
        data = request.json
        required_fields = ["total_price", "status"]

        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        if missing_fields:
            return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

        try:
            cursor.execute(
                """
                UPDATE orders
                SET total_price=%s, status=%s
                WHERE tenant_id=%s AND order_id=%s
                """,
                (
                    data["total_price"],
                    data["status"],
                    tenant_id,
                    order_id,
                ),
            )
            conn.commit()
            if cursor.rowcount == 0:
                return jsonify({"error": "Order not found or no changes made."}), 404
            return jsonify({"message": "Order updated successfully."}), 200
        except pymysql.Error as e:
            return jsonify({"error": f"Database error: {e}"}), 500
        finally:
            conn.close()

    if request.method == 'DELETE':
        try:
            cursor.execute("DELETE FROM orders WHERE tenant_id=%s AND order_id=%s", (tenant_id, order_id))
            conn.commit()
            if cursor.rowcount == 0:
                return jsonify({"error": "Order not found."}), 404
            return jsonify({"message": "Order deleted successfully."}), 200
        except pymysql.Error as e:
            return jsonify({"error": f"Database error: {e}"}), 500
        finally:
            conn.close()
