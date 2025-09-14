import os
from datetime import datetime
from twilio.rest import Client
from twilio.base.exceptions import TwilioException

# Hardcoded phone numbers - Add your phone numbers here
BEEKEEPER_PHONES = [
    "+94763942788",  # Replace with actual phone number
     # Add more numbers if needed
]

def send_threat_sms(threat_data):
    """Send SMS alert for threat detection"""
    
    # Twilio credentials from environment variables
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN') 
    from_number = os.getenv('TWILIO_PHONE_NUMBER')
    
    # Check if credentials are available
    if not all([account_sid, auth_token, from_number]):
        print("Twilio credentials not found in environment variables")
        return False
    
    # Don't send SMS for No_Threat
    threat_type = threat_data.get('threat_type', '')
    if threat_type == 'No_Threat':
        return True
    
    # Create Twilio client
    try:
        client = Client(account_sid, auth_token)
    except Exception as e:
        print(f"Failed to create Twilio client: {e}")
        return False
    
    # Format message
    probability = threat_data.get('probability', 0)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Get threat-specific emoji and message
    threat_messages = {
        'Wax_Moth': {'emoji': '🦋', 'message': 'Wax Moth detected in hive!'},
        'Predator': {'emoji': '🦊', 'message': 'Predator threat detected near hive!'}, 
        'Environmental': {'emoji': '🌡️', 'message': 'Environmental threat detected!'},
    }
    
    threat_info = threat_messages.get(threat_type, {
        'emoji': '⚠️',
        'message': f'{threat_type} threat detected'
    })
    
    message = f"""🐝 HIVE ALERT {threat_info['emoji']}

{threat_info['message']}
Confidence: {probability*100:.1f}%
Time: {timestamp}

Please check your hive immediately!

- BeeGuard Alert System"""
    
    # Send SMS to each phone number
    success_count = 0
    for phone_number in BEEKEEPER_PHONES:
        try:
            message_instance = client.messages.create(
                body=message,
                from_=from_number,
                to=phone_number
            )
            print(f"SMS sent successfully to {phone_number}, SID: {message_instance.sid}")
            success_count += 1
            
        except TwilioException as e:
            print(f"Twilio error sending to {phone_number}: {e}")
        except Exception as e:
            print(f"General error sending to {phone_number}: {e}")
    
    return success_count > 0