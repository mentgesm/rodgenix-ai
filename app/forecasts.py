from flask import Blueprint, request, jsonify
from db import db_connect
import pymysql


forecasts_bp = Blueprint("forecasts", __name__)

@forecasts_bp.route('/forecasts', methods=['GET', 'POST'])
def list_or_create_forecasts():
    conn = db_connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    if request.method == 'GET':
        try:
            tenant_id = request.headers.get("Tenant-ID")
            cursor.execute("SELECT * FROM inventory_forecasts WHERE tenant_id=%s", (tenant_id,))
            forecasts = cursor.fetchall()
            return jsonify(forecasts), 200
        except pymysql.Error as e:
            return jsonify({"error": f"Database error: {e}"}), 500
        finally:
            conn.close()

    if request.method == 'POST':
        data = request.json
        required_fields = ["component_id", "forecast_date", "predicted_demand"]

        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        if missing_fields:
            return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

        try:
            cursor.execute(
                """
                INSERT INTO inventory_forecasts (tenant_id, component_id, forecast_date, predicted_demand, actual_demand)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    request.headers.get("Tenant-ID"),
                    data["component_id"],
                    data["forecast_date"],
                    data["predicted_demand"],
                    data.get("actual_demand"),
                ),
            )
            conn.commit()
            return jsonify({"message": "Forecast record created successfully.", "id": cursor.lastrowid}), 201
        except pymysql.Error as e:
            return jsonify({"error": f"Database error: {e}"}), 500
        finally:
            conn.close()

@forecasts_bp.route('/forecasts/<int:forecast_id>', methods=['GET', 'PUT', 'DELETE'])
def manage_forecast(forecast_id):
    conn = db_connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    tenant_id = request.headers.get("Tenant-ID")

    if not tenant_id:
        return jsonify({"error": "Tenant-ID is required."}), 400

    if request.method == 'GET':
        try:
            cursor.execute("SELECT * FROM inventory_forecasts WHERE tenant_id=%s AND id=%s", (tenant_id, forecast_id))
            forecast = cursor.fetchone()
            if not forecast:
                return jsonify({"error": "Forecast record not found."}), 404
            return jsonify(forecast), 200
        except pymysql.Error as e:
            return jsonify({"error": f"Database error: {e}"}), 500
        finally:
            conn.close()

    if request.method == 'PUT':
        data = request.json
        required_fields = ["predicted_demand", "actual_demand"]

        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        if missing_fields:
            return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

        try:
            cursor.execute(
                """
                UPDATE inventory_forecasts
                SET predicted_demand=%s, actual_demand=%s
                WHERE tenant_id=%s AND id=%s
                """,
                (
                    data["predicted_demand"],
                    data["actual_demand"],
                    tenant_id,
                    forecast_id,
                ),
            )
            conn.commit()
            if cursor.rowcount == 0:
                return jsonify({"error": "Forecast record not found or no changes made."}), 404
            return jsonify({"message": "Forecast record updated successfully."}), 200
        except pymysql.Error as e:
            return jsonify({"error": f"Database error: {e}"}), 500
        finally:
            conn.close()

    if request.method == 'DELETE':
        try:
            cursor.execute("DELETE FROM inventory_forecasts WHERE tenant_id=%s AND id=%s", (tenant_id, forecast_id))
            conn.commit()
            if cursor.rowcount == 0:
                return jsonify({"error": "Forecast record not found."}), 404
            return jsonify({"message": "Forecast record deleted successfully."}), 200
        except pymysql.Error as e:
            return jsonify({"error": f"Database error: {e}"}), 500
        finally:
            conn.close()
