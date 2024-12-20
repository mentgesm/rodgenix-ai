from flask import Blueprint, request, jsonify
from db import db_connect
import pymysql


nlp_queries_bp = Blueprint("nlp_queries", __name__)

@nlp_queries_bp.route('/nlp_queries', methods=['GET', 'POST'])
def list_or_create_nlp_queries():
    conn = db_connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    if request.method == 'GET':
        try:
            tenant_id = request.headers.get("Tenant-ID")
            cursor.execute("SELECT * FROM nlp_query_mapping WHERE tenant_id=%s", (tenant_id,))
            queries = cursor.fetchall()
            return jsonify(queries), 200
        except pymysql.Error as e:
            return jsonify({"error": f"Database error: {e}"}), 500
        finally:
            conn.close()

    if request.method == 'POST':
        data = request.json
        required_fields = ["query", "mapped_action"]

        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        if missing_fields:
            return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

        try:
            cursor.execute(
                """
                INSERT INTO nlp_query_mapping (tenant_id, query, mapped_action, created_at)
                VALUES (%s, %s, %s, NOW())
                """,
                (
                    request.headers.get("Tenant-ID"),
                    data["query"],
                    data["mapped_action"],
                ),
            )
            conn.commit()
            return jsonify({"message": "NLP query added successfully.", "id": cursor.lastrowid}), 201
        except pymysql.Error as e:
            return jsonify({"error": f"Database error: {e}"}), 500
        finally:
            conn.close()

@nlp_queries_bp.route('/nlp_queries/<int:query_id>', methods=['GET', 'PUT', 'DELETE'])
def manage_nlp_query(query_id):
    conn = db_connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    tenant_id = request.headers.get("Tenant-ID")

    if not tenant_id:
        return jsonify({"error": "Tenant-ID is required."}), 400

    if request.method == 'GET':
        try:
            cursor.execute("SELECT * FROM nlp_query_mapping WHERE tenant_id=%s AND id=%s", (tenant_id, query_id))
            query = cursor.fetchone()
            if not query:
                return jsonify({"error": "NLP query not found."}), 404
            return jsonify(query), 200
        except pymysql.Error as e:
            return jsonify({"error": f"Database error: {e}"}), 500
        finally:
            conn.close()

    if request.method == 'PUT':
        data = request.json
        required_fields = ["mapped_action"]

        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        if missing_fields:
            return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

        try:
            cursor.execute(
                """
                UPDATE nlp_query_mapping
                SET mapped_action=%s
                WHERE tenant_id=%s AND id=%s
                """,
                (
                    data["mapped_action"],
                    tenant_id,
                    query_id,
                ),
            )
            conn.commit()
            if cursor.rowcount == 0:
                return jsonify({"error": "NLP query not found or no changes made."}), 404
            return jsonify({"message": "NLP query updated successfully."}), 200
        except pymysql.Error as e:
            return jsonify({"error": f"Database error: {e}"}), 500
        finally:
            conn.close()

    if request.method == 'DELETE':
        try:
            cursor.execute("DELETE FROM nlp_query_mapping WHERE tenant_id=%s AND id=%s", (tenant_id, query_id))
            conn.commit()
            if cursor.rowcount == 0:
                return jsonify({"error": "NLP query not found."}), 404
            return jsonify({"message": "NLP query deleted successfully."}), 200
        except pymysql.Error as e:
            return jsonify({"error": f"Database error: {e}"}), 500
        finally:
            conn.close()
