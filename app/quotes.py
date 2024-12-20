from flask import Blueprint, request, jsonify
from db import db_connect
import pymysql

quotes_bp = Blueprint("quotes", __name__)

@quotes_bp.route('/quotes', methods=['GET', 'POST'])
def list_or_create_quotes():
    conn = db_connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    if request.method == 'GET':
        try:
            tenant_id = request.headers.get("Tenant-ID")
            cursor.execute("SELECT * FROM quotes WHERE tenant_id=%s", (tenant_id,))
            quotes = cursor.fetchall()
            return jsonify(quotes), 200
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
                INSERT INTO quotes (tenant_id, customer_id, total_price, status)
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
            return jsonify({"message": "Quote created successfully.", "quote_id": cursor.lastrowid}), 201
        except pymysql.Error as e:
            return jsonify({"error": f"Database error: {e}"}), 500
        finally:
            conn.close()

@quotes_bp.route('/quotes/<int:quote_id>', methods=['GET', 'PUT', 'DELETE'])
def manage_quote(quote_id):
    conn = db_connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    tenant_id = request.headers.get("Tenant-ID")

    if not tenant_id:
        return jsonify({"error": "Tenant-ID is required."}), 400

    if request.method == 'GET':
        try:
            cursor.execute("SELECT * FROM quotes WHERE tenant_id=%s AND quote_id=%s", (tenant_id, quote_id))
            quote = cursor.fetchone()
            if not quote:
                return jsonify({"error": "Quote not found."}), 404
            return jsonify(quote), 200
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
                UPDATE quotes
                SET total_price=%s, status=%s
                WHERE tenant_id=%s AND quote_id=%s
                """,
                (
                    data["total_price"],
                    data["status"],
                    tenant_id,
                    quote_id,
                ),
            )
            conn.commit()
            if cursor.rowcount == 0:
                return jsonify({"error": "Quote not found or no changes made."}), 404
            return jsonify({"message": "Quote updated successfully."}), 200
        except pymysql.Error as e:
            return jsonify({"error": f"Database error: {e}"}), 500
        finally:
            conn.close()

    if request.method == 'DELETE':
        try:
            cursor.execute("DELETE FROM quotes WHERE tenant_id=%s AND quote_id=%s", (tenant_id, quote_id))
            conn.commit()
            if cursor.rowcount == 0:
                return jsonify({"error": "Quote not found."}), 404
            return jsonify({"message": "Quote deleted successfully."}), 200
        except pymysql.Error as e:
            return jsonify({"error": f"Database error: {e}"}), 500
        finally:
            conn.close()
