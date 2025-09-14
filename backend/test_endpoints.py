import requests

def test_api_endpoints():
    base_url = "http://127.0.0.1:5000"
    
    # Test root endpoint
    print("🔍 Testing root endpoint...")
    try:
        response = requests.get(f"{base_url}/")
        print(f"Root Status: {response.status_code}")
        print(f"Root Response: {response.json()}")
    except Exception as e:
        print(f"Root Error: {e}")
    
    # Test routes endpoint
    print("\n🔍 Testing routes endpoint...")
    try:
        response = requests.get(f"{base_url}/api/routes")
        print(f"Routes Status: {response.status_code}")
        print(f"Routes Response: {response.json()}")
    except Exception as e:
        print(f"Routes Error: {e}")
    
    # Test health endpoint
    print("\n🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/api/health")
        print(f"Health Status: {response.status_code}")
        print(f"Health Response: {response.json()}")
    except Exception as e:
        print(f"Health Error: {e}")

if __name__ == "__main__":
    test_api_endpoints()