import requests
import json

# Test the registration API endpoint
def test_registration_api():
    url = "http://127.0.0.1:5001/api/hive-register"
    
    # Test data
    test_data = {
        "fullName": "Test User",
        "displayName": "TestUser",
        "phoneNumber": "1234567890",
        "email": "test@example.com",
        "password": "testpass123",
        "company": "Test Company",
        "country": "United Kingdom",
        "packageTitle": "1-3 Hives",
        "packagePrice": "£4.99"
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    print("🔍 Testing registration API endpoint...")
    print(f"URL: {url}")
    print(f"Data: {json.dumps(test_data, indent=2)}")
    
    try:
        response = requests.post(url, json=test_data, headers=headers, timeout=10)
        
        print(f"\n📊 Response Status: {response.status_code}")
        print(f"📊 Response Headers: {dict(response.headers)}")
        
        try:
            response_json = response.json()
            print(f"📊 Response Body: {json.dumps(response_json, indent=2)}")
        except:
            print(f"📊 Response Body (raw): {response.text}")
            
        if response.status_code == 200:
            print("✅ Registration API is working!")
        else:
            print("❌ Registration API failed!")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed! Make sure the API is running on port 5000")
    except requests.exceptions.Timeout:
        print("❌ Request timed out!")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

# Test health endpoint
def test_health_endpoint():
    url = "http://127.0.0.1:5001/api/health"
    
    print("\n🔍 Testing health endpoint...")
    try:
        response = requests.get(url, timeout=5)
        print(f"📊 Health Status: {response.status_code}")
        print(f"📊 Health Response: {response.json()}")
        
        if response.status_code == 200:
            print("✅ Health endpoint is working!")
        else:
            print("❌ Health endpoint failed!")
            
    except Exception as e:
        print(f"❌ Health check error: {str(e)}")

if __name__ == "__main__":
    print("🐝 BeeSync Registration API Test")
    print("=" * 40)
    
    # Test health first
    test_health_endpoint()
    
    print("\n" + "=" * 40)
    
    # Test registration
    test_registration_api()
    
    print("\n" + "=" * 40)
    print("🔧 If tests fail, check:")
    print("1. API is running: python registration_api.py")
    print("2. Port 5000 is not blocked")
    print("3. Email password is correct")
    print("4. Internet connection is working")