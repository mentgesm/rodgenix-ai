import requests

BASE_URL = "http://127.0.0.1:5001"  # Updated hostname and port
TENANT_ID = "tenant-12345"  # Replace with the actual tenant ID

HEADERS = {
    "Tenant-ID": TENANT_ID,
    "Content-Type": "application/json",
}

ENDPOINTS = {
    "customers": f"{BASE_URL}/customers",
    "quotes": f"{BASE_URL}/quotes",
    "orders": f"{BASE_URL}/orders",
    "payments": f"{BASE_URL}/payments",
    "photos": f"{BASE_URL}/photos",
    "user_interactions": f"{BASE_URL}/user_interactions",
    "compatibility": f"{BASE_URL}/compatibility",
    "forecasts": f"{BASE_URL}/forecasts",
    "nlp_queries": f"{BASE_URL}/nlp_queries",
    "ai_models": f"{BASE_URL}/ai_models",
}

def test_endpoint(endpoint, method="GET", data=None):
    try:
        if method == "GET":
            response = requests.get(endpoint, headers=HEADERS)
        elif method == "POST":
            response = requests.post(endpoint, headers=HEADERS, json=data)
        elif method == "PUT":
            response = requests.put(endpoint, headers=HEADERS, json=data)
        elif method == "DELETE":
            response = requests.delete(endpoint, headers=HEADERS)
        else:
            print(f"Unsupported HTTP method: {method}")
            return

        print(f"Endpoint: {endpoint}")
        print(f"Status Code: {response.status_code}")
        try:
            print(f"Response: {response.json()}\n")
        except ValueError:
            print("Response is not JSON.\n")
    except Exception as e:
        print(f"Error testing {endpoint}: {e}")

def run_tests():
    # Test GET for all endpoints
    for name, url in ENDPOINTS.items():
        print(f"Testing GET on {name}...")
        test_endpoint(url)

    # Example POST data for creating a new resource
    test_data = {
        "customers": {"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com", "address": "123 Main St"},
        "quotes": {"customer_id": 1, "total_price": 100.50, "status": "Pending"},
        "orders": {"customer_id": 1, "total_price": 100.50, "status": "Shipped"},
        "payments": {"order_id": 1, "amount_paid": 100.50, "payment_method": "Credit Card"},
        "photos": {"related_table": "orders", "related_id": 1, "photo_url": "http://example.com/photo.jpg"},
        "user_interactions": {"user_id": 1, "component_id": 2, "action_type": "view"},
        "compatibility": {"component_a_id": 1, "component_b_id": 2, "compatibility_score": 0.95},
        "forecasts": {"component_id": 1, "forecast_date": "2024-01-01", "predicted_demand": 10},
        "nlp_queries": {"query": "show customers", "mapped_action": '{"action": "fetch_customers"}'},
        "ai_models": {"model_name": "Test Model", "version": "1.0", "last_trained": "2024-01-01", "metrics": '{"accuracy": 95}'},
    }

    # Test POST for each endpoint with example data
    for name, url in ENDPOINTS.items():
        if name in test_data:
            print(f"Testing POST on {name}...")
            test_endpoint(url, method="POST", data=test_data[name])

if __name__ == "__main__":
    run_tests()
