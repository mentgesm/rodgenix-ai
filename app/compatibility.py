from flask import Blueprint, request, jsonify
from db import db_connect
import pymysql


compatibility_bp = Blueprint("compatibility", __name__)

@compatibility_bp.route('/compatibility', methods=['GET', 'POST'])
def list_or_create_compatibility():
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
            return jsonify({"message": "Compatibility record created successfully.", "id": cursor.lastrowid}), 201
        except pymysql.Error as e:
            return jsonify({"error": f"Database error: {e}"}), 500
        finally:
            conn.close()

@compatibility_bp.route('/compatibility/<int:record_id>', methods=['GET', 'PUT', 'DELETE'])
def manage_compatibility(record_id):
    conn = db_connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    tenant_id = request.headers.get("Tenant-ID")

    if not tenant_id:
        return jsonify({"error": "Tenant-ID is required."}), 400

    if request.method == 'GET':
        try:
            cursor.execute("SELECT * FROM component_compatibility WHERE tenant_id=%s AND id=%s", (tenant_id, record_id))
            record = cursor.fetchone()
            if not record:
                return jsonify({"error": "Compatibility record not found."}), 404
            return jsonify(record), 200
        except pymysql.Error as e:
            return jsonify({"error": f"Database error: {e}"}), 500
        finally:
            conn.close()

    if request.method == 'PUT':
        data = request.json
        required_fields = ["compatibility_score"]

        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        if missing_fields:
            return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

        try:
            cursor.execute(
                """
                UPDATE component_compatibility
                SET compatibility_score=%s
                WHERE tenant_id=%s AND id=%s
                """,
                (
                    data["compatibility_score"],
                    tenant_id,
                    record_id,
                ),
            )
            conn.commit()
            if cursor.rowcount == 0:
                return jsonify({"error": "Compatibility record not found or no changes made."}), 404
            return jsonify({"message": "Compatibility record updated successfully."}), 200
        except pymysql.Error as e:
            return jsonify({"error": f"Database error: {e}"}), 500
        finally:
            conn.close()

    if request.method == 'DELETE':
        try:
            cursor.execute("DELETE FROM component_compatibility WHERE tenant_id=%s AND id=%s", (tenant_id, record_id))
            conn.commit()
            if cursor.rowcount == 0:
                return jsonify({"error": "Compatibility record not found."}), 404
            return jsonify({"message": "Compatibility record deleted successfully."}), 200
        except pymysql.Error as e:
            return jsonify({"error": f"Database error: {e}"}), 500
        finally:
            conn.close()
