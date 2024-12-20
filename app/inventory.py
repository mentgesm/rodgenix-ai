from flask import Blueprint, request, jsonify
from db import db_connect
import pymysql
import logging

logging.basicConfig(level=logging.INFO)

inventory_bp = Blueprint("inventory", __name__)

@inventory_bp.route('/inventory/<item_type>', methods=['GET', 'POST'])
def list_or_create_inventory(item_type):
    valid_tables = ["blanks", "guides", "threads", "reel_seats", "winding_checks"]

    if item_type not in valid_tables:
        return jsonify({"error": "Invalid inventory type."}), 400

    conn = db_connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    if request.method == 'GET':
        try:
            tenant_id = request.headers.get("Tenant-ID")
            cursor.execute(f"SELECT * FROM {item_type} WHERE tenant_id=%s", (tenant_id,))
            items = cursor.fetchall()
            return jsonify(items), 200
        except pymysql.Error as e:
            logging.error(f"Database error during GET: {e}")
            return jsonify({"error": f"Database error: {e}"}), 500
        finally:
            conn.close()

    if request.method == 'POST':
        data = request.json

        try:
            # Get column names for validation
            cursor.execute(f"DESCRIBE {item_type}")
            columns = [row["Field"] for row in cursor.fetchall() if row["Field"] not in ["tenant_id", "id"]]

            # Validate required fields
            cursor.execute(f"DESCRIBE {item_type}")
            required_fields = [row["Field"] for row in cursor.fetchall() if row["Null"] == "NO" and row["Field"] != "id" and row["Field"] != "tenant_id"]
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

            # Prepare and execute the query
            fields = ", ".join(columns)
            placeholders = ", ".join(["%s"] * len(columns))
            query = f"INSERT INTO {item_type} (tenant_id, {fields}) VALUES (%s, {placeholders})"
            values = [request.headers.get("Tenant-ID")] + [data.get(field) for field in columns]

            logging.info(f"Executing Query: {query}")
            cursor.execute(query, values)
            conn.commit()
            return jsonify({"message": f"{item_type.capitalize()} entry created successfully.", "id": cursor.lastrowid}), 201
        except pymysql.Error as e:
            logging.error(f"Database error during POST: {e}")
            return jsonify({"error": f"Database error: {e}"}), 500
        finally:
            conn.close()

@inventory_bp.route('/inventory/<item_type>/<int:item_id>', methods=['GET', 'PUT', 'DELETE'])
def manage_inventory(item_type, item_id):
    valid_tables = ["blanks", "guides", "threads", "reel_seats", "winding_checks"]

    if item_type not in valid_tables:
        return jsonify({"error": "Invalid inventory type."}), 400

    conn = db_connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    tenant_id = request.headers.get("Tenant-ID")

    if not tenant_id:
        return jsonify({"error": "Tenant-ID is required."}), 400

    if request.method == 'GET':
        try:
            cursor.execute(f"SELECT * FROM {item_type} WHERE tenant_id=%s AND id=%s", (tenant_id, item_id))
            item = cursor.fetchone()
            if not item:
                return jsonify({"error": f"{item_type.capitalize()} item not found."}), 404
            return jsonify(item), 200
        except pymysql.Error as e:
            logging.error(f"Database error during GET by ID: {e}")
            return jsonify({"error": f"Database error: {e}"}), 500
        finally:
            conn.close()

    if request.method == 'PUT':
        data = request.json
        try:
            # Get columns for validation
            cursor.execute(f"DESCRIBE {item_type}")
            columns = [row["Field"] for row in cursor.fetchall() if row["Field"] not in ["tenant_id", "id"]]

            # Validate fields
            updates = ", ".join([f"{field}=%s" for field in columns if field in data])
            if not updates:
                return jsonify({"error": "No valid fields provided for update."}), 400

            query = f"UPDATE {item_type} SET {updates} WHERE tenant_id=%s AND id=%s"
            values = [data[field] for field in columns if field in data] + [tenant_id, item_id]

            logging.info(f"Executing Query: {query}")
            cursor.execute(query, values)
            conn.commit()
            if cursor.rowcount == 0:
                return jsonify({"error": f"{item_type.capitalize()} item not found or no changes made."}), 404
            return jsonify({"message": f"{item_type.capitalize()} item updated successfully."}), 200
        except pymysql.Error as e:
            logging.error(f"Database error during PUT: {e}")
            return jsonify({"error": f"Database error: {e}"}), 500
        finally:
            conn.close()

    if request.method == 'DELETE':
        try:
            cursor.execute(f"DELETE FROM {item_type} WHERE tenant_id=%s AND id=%s", (tenant_id, item_id))
            conn.commit()
            if cursor.rowcount == 0:
                return jsonify({"error": f"{item_type.capitalize()} item not found."}), 404
            return jsonify({"message": f"{item_type.capitalize()} item deleted successfully."}), 200
        except pymysql.Error as e:
            logging.error(f"Database error during DELETE: {e}")
            return jsonify({"error": f"Database error: {e}"}), 500
        finally:
            conn.close()
