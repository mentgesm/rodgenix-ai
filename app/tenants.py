from flask import Blueprint, request, jsonify
from db import db_connect
import pymysql

tenants_bp = Blueprint("tenants", __name__)

@tenants_bp.route('/tenants', methods=['GET', 'POST'])
def list_or_create_tenants():
    conn = db_connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    if request.method == 'GET':
        try:
            cursor.execute("SELECT * FROM customers_metadata")
            tenants = cursor.fetchall()
            return jsonify(tenants), 200
        except pymysql.Error as e:
            return jsonify({"error": f"Database error: {e}"}), 500
        finally:
            conn.close()

    if request.method == 'POST':
        data = request.json
        required_fields = ["tenant_id", "db_host", "db_name", "db_user", "db_password"]

        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        if missing_fields:
            return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

        try:
            cursor.execute(
                """
                INSERT INTO customers_metadata (tenant_id, db_host, db_name, db_user, db_password)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    data["tenant_id"],
                    data["db_host"],
                    data["db_name"],
                    data["db_user"],
                    data["db_password"],
                ),
            )
            conn.commit()
            return jsonify({"message": "Tenant created successfully.", "tenant_id": data["tenant_id"]}), 201
        except pymysql.Error as e:
            return jsonify({"error": f"Database error: {e}"}), 500
        finally:
            conn.close()

@tenants_bp.route('/tenants/<tenant_id>', methods=['GET', 'PUT', 'DELETE'])
def manage_tenant(tenant_id):
    conn = db_connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    if request.method == 'GET':
        try:
            cursor.execute("SELECT * FROM customers_metadata WHERE tenant_id=%s", (tenant_id,))
            tenant = cursor.fetchone()
            if not tenant:
                return jsonify({"error": "Tenant not found."}), 404
            return jsonify(tenant), 200
        except pymysql.Error as e:
            return jsonify({"error": f"Database error: {e}"}), 500
        finally:
            conn.close()

    if request.method == 'PUT':
        data = request.json
        required_fields = ["db_host", "db_name", "db_user", "db_password"]

        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        if missing_fields:
            return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

        try:
            cursor.execute(
                """
                UPDATE customers_metadata
                SET db_host=%s, db_name=%s, db_user=%s, db_password=%s
                WHERE tenant_id=%s
                """,
                (
                    data["db_host"],
                    data["db_name"],
                    data["db_user"],
                    data["db_password"],
                    tenant_id,
                ),
            )
            conn.commit()
            if cursor.rowcount == 0:
                return jsonify({"error": "Tenant not found or no changes made."}), 404
            return jsonify({"message": "Tenant updated successfully."}), 200
        except pymysql.Error as e:
            return jsonify({"error": f"Database error: {e}"}), 500
        finally:
            conn.close()

    if request.method == 'DELETE':
        try:
            cursor.execute("DELETE FROM customers_metadata WHERE tenant_id=%s", (tenant_id,))
            conn.commit()
            if cursor.rowcount == 0:
                return jsonify({"error": "Tenant not found."}), 404
            return jsonify({"message": "Tenant deleted successfully."}), 200
        except pymysql.Error as e:
            return jsonify({"error": f"Database error: {e}"}), 500
        finally:
            conn.close()
