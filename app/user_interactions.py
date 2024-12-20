from flask import Blueprint, request, jsonify
from db import db_connect
import pymysql

user_interactions_bp = Blueprint("user_interactions", __name__)

@user_interactions_bp.route('/user_interactions', methods=['GET', 'POST'])
def list_or_create_user_interactions():
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
            return jsonify({"message": "User interaction logged successfully.", "interaction_id": cursor.lastrowid}), 201
        except pymysql.Error as e:
            return jsonify({"error": f"Database error: {e}"}), 500
        finally:
            conn.close()

@user_interactions_bp.route('/user_interactions/<int:interaction_id>', methods=['GET', 'PUT', 'DELETE'])
def manage_user_interaction(interaction_id):
    conn = db_connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    tenant_id = request.headers.get("Tenant-ID")

    if not tenant_id:
        return jsonify({"error": "Tenant-ID is required."}), 400

    if request.method == 'GET':
        try:
            cursor.execute("SELECT * FROM user_interactions WHERE tenant_id=%s AND id=%s", (tenant_id, interaction_id))
            interaction = cursor.fetchone()
            if not interaction:
                return jsonify({"error": "Interaction not found."}), 404
            return jsonify(interaction), 200
        except pymysql.Error as e:
            return jsonify({"error": f"Database error: {e}"}), 500
        finally:
            conn.close()

    if request.method == 'PUT':
        data = request.json
        required_fields = ["action_type"]

        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        if missing_fields:
            return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

        try:
            cursor.execute(
                """
                UPDATE user_interactions
                SET action_type=%s
                WHERE tenant_id=%s AND id=%s
                """,
                (
                    data["action_type"],
                    tenant_id,
                    interaction_id,
                ),
            )
            conn.commit()
            if cursor.rowcount == 0:
                return jsonify({"error": "Interaction not found or no changes made."}), 404
            return jsonify({"message": "Interaction updated successfully."}), 200
        except pymysql.Error as e:
            return jsonify({"error": f"Database error: {e}"}), 500
        finally:
            conn.close()

    if request.method == 'DELETE':
        try:
            cursor.execute("DELETE FROM user_interactions WHERE tenant_id=%s AND id=%s", (tenant_id, interaction_id))
            conn.commit()
            if cursor.rowcount == 0:
                return jsonify({"error": "Interaction not found."}), 404
            return jsonify({"message": "Interaction deleted successfully."}), 200
        except pymysql.Error as e:
            return jsonify({"error": f"Database error: {e}"}), 500
        finally:
            conn.close()
