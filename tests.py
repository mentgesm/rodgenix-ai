import requests

BASE_URL = "http://127.0.0.1:5001"  # API base URL
TENANTS = ["tenant-12345", "tenant-67890"]  # Test multiple tenants

HEADERS_TEMPLATE = {
    "Content-Type": "application/json",
}

INVENTORY_TABLES = [
    "blanks",
    "guides",
    "threads",
    "reel_seats",
    "winding_checks",
]

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


def setup_test_data(tenant_id):
    """Ensure all required foreign key references exist before testing."""
    headers = {"Tenant-ID": tenant_id, "Content-Type": "application/json"}
    test_customers = [
        {"first_name": "John", "last_name": "Doe", "email": f"john.doe-{tenant_id}@example.com", "address": "123 Main St"},
        {"first_name": "Jane", "last_name": "Smith", "email": f"jane.smith-{tenant_id}@example.com", "address": "456 Elm St"},
    ]
    for customer in test_customers:
        response = requests.post(f"{BASE_URL}/customers", headers=headers, json=customer)
        if response.status_code not in {200, 201}:
            print(f"Failed to set up customer for {tenant_id}: {response.json()}")


def test_endpoint(endpoint, method="GET", tenant_id=None, data=None):
    """Test an API endpoint with the specified method and payload."""
    headers = HEADERS_TEMPLATE.copy()
    if tenant_id:
        headers["Tenant-ID"] = tenant_id

    try:
        if method == "GET":
            response = requests.get(endpoint, headers=headers)
        elif method == "POST":
            response = requests.post(endpoint, headers=headers, json=data)
        elif method == "PUT":
            response = requests.put(endpoint, headers=headers, json=data)
        elif method == "DELETE":
            response = requests.delete(endpoint, headers=headers)
        else:
            print(f"Unsupported HTTP method: {method}")
            return False

        success = response.status_code in {200, 201}
        print(f"Endpoint: {endpoint}, Method: {method}, Status: {response.status_code}")
        try:
            print(f"Response: {response.json()}")
        except ValueError:
            print("Response is not JSON.")
        return success
    except Exception as e:
        print(f"Error testing {endpoint}: {e}")
        return False


def run_tests():
    results = []  # Store test results for summary

    # Set up test data for each tenant
    for tenant_id in TENANTS:
        print(f"\n=== Setting up test data for Tenant: {tenant_id} ===")
        setup_test_data(tenant_id)

    # Test each endpoint for each tenant
    for tenant_id in TENANTS:
        print(f"\n=== Testing for Tenant: {tenant_id} ===\n")
        tenant_results = {"tenant": tenant_id, "success": 0, "failure": 0}

        # Test CRUD operations for standard endpoints
        test_data = {
            "customers": {"first_name": "John", "last_name": "Doe", "email": f"new.doe-{tenant_id}@example.com", "address": "789 Elm St"},
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

        for name, url in ENDPOINTS.items():
            # Test GET
            print(f"Testing GET on {name}...")
            if test_endpoint(url, method="GET", tenant_id=tenant_id):
                tenant_results["success"] += 1
            else:
                tenant_results["failure"] += 1

            # Test POST
            if name in test_data:
                print(f"Testing POST on {name}...")
                if test_endpoint(url, method="POST", tenant_id=tenant_id, data=test_data[name]):
                    tenant_results["success"] += 1
                else:
                    tenant_results["failure"] += 1

        # Test CRUD operations for inventory tables
        inventory_data = {
            "blanks": {
                "qb_item_id": "BLANK004",
                "name": "New Blank",
                "brand": "TestBrand",
                "length": 6.5,
                "power": "Light",
                "action": "Moderate",
                "quantity": 15,
                "price": 20.50,
            },
            "guides": {
                "qb_item_id": "GUIDE004",
                "name": "New Guide",
                "brand": "TestBrand",
                "size": "L",
                "material": "Aluminum",
                "vendor": "VendorZ",
                "cost": 4.50,
                "quantity": 25,
                "price": 6.00,
            },
            "threads": {
                "qb_item_id": "THREAD004",
                "thread_color_id": "YEL001",
                "color_name": "Yellow",
                "brand": "TestBrand",
                "type": "Polyester",
                "quantity": 200,
                "price": 2.00,
            },
            "reel_seats": {
                "qb_item_id": "REEL004",
                "name": "Carbon Reel Seat",
                "brand": "TestBrand",
                "type": "Spinning",
                "material": "Carbon Fiber",
                "color": "Gray",
                "quantity": 30,
                "price": 14.99,
            },
            "winding_checks": {
                "qb_item_id": "WIND004",
                "size": "S",
                "material": "Rubber",
                "color": "Red",
                "quantity": 50,
                "price": 1.50,
            },
        }

        for table in INVENTORY_TABLES:
            inventory_url = f"{BASE_URL}/inventory/{table}"
            print(f"Testing Inventory Table: {table} (GET)...")
            if test_endpoint(inventory_url, method="GET", tenant_id=tenant_id):
                tenant_results["success"] += 1
            else:
                tenant_results["failure"] += 1

            print(f"Testing Inventory Table: {table} (POST)...")
            if test_endpoint(inventory_url, method="POST", tenant_id=tenant_id, data=inventory_data[table]):
                tenant_results["success"] += 1
            else:
                tenant_results["failure"] += 1

        results.append(tenant_results)

    # Print summary
    print("\n=== Test Summary ===")
    for result in results:
        print(f"Tenant: {result['tenant']}, Success: {result['success']}, Failure: {result['failure']}")


if __name__ == "__main__":
    run_tests()
