from flask import Blueprint, request, jsonify
from db import db_connect
import pymysql


photos_bp = Blueprint("photos", __name__)

@photos_bp.route('/photos', methods=['GET', 'POST'])
def list_or_create_photos():
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
            return jsonify({"message": "Photo created successfully.", "photo_id": cursor.lastrowid}), 201
        except pymysql.Error as e:
            return jsonify({"error": f"Database error: {e}"}), 500
        finally:
            conn.close()

@photos_bp.route('/photos/<int:photo_id>', methods=['GET', 'PUT', 'DELETE'])
def manage_photo(photo_id):
    conn = db_connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    tenant_id = request.headers.get("Tenant-ID")

    if not tenant_id:
        return jsonify({"error": "Tenant-ID is required."}), 400

    if request.method == 'GET':
        try:
            cursor.execute("SELECT * FROM photos WHERE tenant_id=%s AND photo_id=%s", (tenant_id, photo_id))
            photo = cursor.fetchone()
            if not photo:
                return jsonify({"error": "Photo not found."}), 404
            return jsonify(photo), 200
        except pymysql.Error as e:
            return jsonify({"error": f"Database error: {e}"}), 500
        finally:
            conn.close()

    if request.method == 'PUT':
        data = request.json
        required_fields = ["photo_url"]

        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        if missing_fields:
            return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

        try:
            cursor.execute(
                """
                UPDATE photos
                SET photo_url=%s
                WHERE tenant_id=%s AND photo_id=%s
                """,
                (
                    data["photo_url"],
                    tenant_id,
                    photo_id,
                ),
            )
            conn.commit()
            if cursor.rowcount == 0:
                return jsonify({"error": "Photo not found or no changes made."}), 404
            return jsonify({"message": "Photo updated successfully."}), 200
        except pymysql.Error as e:
            return jsonify({"error": f"Database error: {e}"}), 500
        finally:
            conn.close()

    if request.method == 'DELETE':
        try:
            cursor.execute("DELETE FROM photos WHERE tenant_id=%s AND photo_id=%s", (tenant_id, photo_id))
            conn.commit()
            if cursor.rowcount == 0:
                return jsonify({"error": "Photo not found."}), 404
            return jsonify({"message": "Photo deleted successfully."}), 200
        except pymysql.Error as e:
            return jsonify({"error": f"Database error: {e}"}), 500
        finally:
            conn.close()
