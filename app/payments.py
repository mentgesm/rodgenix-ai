from flask import Blueprint, request, jsonify
from db import db_connect
import pymysql


payments_bp = Blueprint("payments", __name__)

@payments_bp.route('/payments', methods=['GET', 'POST'])
def list_or_create_payments():
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
            return jsonify({"message": "Payment created successfully.", "payment_id": cursor.lastrowid}), 201
        except pymysql.Error as e:
            return jsonify({"error": f"Database error: {e}"}), 500
        finally:
            conn.close()

@payments_bp.route('/payments/<int:payment_id>', methods=['GET', 'PUT', 'DELETE'])
def manage_payment(payment_id):
    conn = db_connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    tenant_id = request.headers.get("Tenant-ID")

    if not tenant_id:
        return jsonify({"error": "Tenant-ID is required."}), 400

    if request.method == 'GET':
        try:
            cursor.execute("SELECT * FROM payments WHERE tenant_id=%s AND payment_id=%s", (tenant_id, payment_id))
            payment = cursor.fetchone()
            if not payment:
                return jsonify({"error": "Payment not found."}), 404
            return jsonify(payment), 200
        except pymysql.Error as e:
            return jsonify({"error": f"Database error: {e}"}), 500
        finally:
            conn.close()

    if request.method == 'PUT':
        data = request.json
        required_fields = ["amount_paid", "payment_method"]

        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        if missing_fields:
            return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

        try:
            cursor.execute(
                """
                UPDATE payments
                SET amount_paid=%s, payment_method=%s
                WHERE tenant_id=%s AND payment_id=%s
                """,
                (
                    data["amount_paid"],
                    data["payment_method"],
                    tenant_id,
                    payment_id,
                ),
            )
            conn.commit()
            if cursor.rowcount == 0:
                return jsonify({"error": "Payment not found or no changes made."}), 404
            return jsonify({"message": "Payment updated successfully."}), 200
        except pymysql.Error as e:
            return jsonify({"error": f"Database error: {e}"}), 500
        finally:
            conn.close()

    if request.method == 'DELETE':
        try:
            cursor.execute("DELETE FROM payments WHERE tenant_id=%s AND payment_id=%s", (tenant_id, payment_id))
            conn.commit()
            if cursor.rowcount == 0:
                return jsonify({"error": "Payment not found."}), 404
            return jsonify({"message": "Payment deleted successfully."}), 200
        except pymysql.Error as e:
            return jsonify({"error": f"Database error: {e}"}), 500
        finally:
            conn.close()
