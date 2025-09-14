import requests

def debug_api():
    base_url = "http://127.0.0.1:5000"
    
    print("🔍 Debugging API responses...")
    
    # Test root endpoint
    try:
        response = requests.get(f"{base_url}/")
        print(f"\n📊 Root Endpoint (/):")
        print(f"Status: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        print(f"Content: {response.text[:500]}...")
    except Exception as e:
        print(f"Root Error: {e}")
    
    # Test registration endpoint
    try:
        response = requests.get(f"{base_url}/api/hive-register")
        print(f"\n📊 Registration Endpoint (/api/hive-register):")
        print(f"Status: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        print(f"Content: {response.text[:500]}...")
    except Exception as e:
        print(f"Registration Error: {e}")
        
    # Try posting to registration endpoint
    try:
        test_data = {"fullName": "Test"}
        response = requests.post(f"{base_url}/api/hive-register", json=test_data)
        print(f"\n📊 Registration POST:")
        print(f"Status: {response.status_code}")
        print(f"Content: {response.text[:500]}...")
    except Exception as e:
        print(f"Registration POST Error: {e}")

if __name__ == "__main__":
    debug_api()