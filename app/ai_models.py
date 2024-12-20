from flask import Blueprint, request, jsonify
from db import db_connect
import pymysql


ai_models_bp = Blueprint("ai_models", __name__)

@ai_models_bp.route('/ai_models', methods=['GET', 'POST'])
def list_or_create_ai_models():
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
            return jsonify({"message": "AI model metadata created successfully.", "id": cursor.lastrowid}), 201
        except pymysql.Error as e:
            return jsonify({"error": f"Database error: {e}"}), 500
        finally:
            conn.close()

@ai_models_bp.route('/ai_models/<int:model_id>', methods=['GET', 'PUT', 'DELETE'])
def manage_ai_model(model_id):
    conn = db_connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    if request.method == 'GET':
        try:
            cursor.execute("SELECT * FROM ai_model_metadata WHERE id=%s", (model_id,))
            model = cursor.fetchone()
            if not model:
                return jsonify({"error": "AI model not found."}), 404
            return jsonify(model), 200
        except pymysql.Error as e:
            return jsonify({"error": f"Database error: {e}"}), 500
        finally:
            conn.close()

    if request.method == 'PUT':
        data = request.json
        required_fields = ["version", "last_trained", "metrics"]

        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        if missing_fields:
            return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

        try:
            cursor.execute(
                """
                UPDATE ai_model_metadata
                SET version=%s, last_trained=%s, metrics=%s
                WHERE id=%s
                """,
                (
                    data["version"],
                    data["last_trained"],
                    data["metrics"],
                    model_id,
                ),
            )
            conn.commit()
            if cursor.rowcount == 0:
                return jsonify({"error": "AI model not found or no changes made."}), 404
            return jsonify({"message": "AI model updated successfully."}), 200
        except pymysql.Error as e:
            return jsonify({"error": f"Database error: {e}"}), 500
        finally:
            conn.close()

    if request.method == 'DELETE':
        try:
            cursor.execute("DELETE FROM ai_model_metadata WHERE id=%s", (model_id,))
            conn.commit()
            if cursor.rowcount == 0:
                return jsonify({"error": "AI model not found."}), 404
            return jsonify({"message": "AI model deleted successfully."}), 200
        except pymysql.Error as e:
            return jsonify({"error": f"Database error: {e}"}), 500
        finally:
            conn.close()
