from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import logging
import os
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

class EmailService:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.port = 587
        self.sender_email = "beehivemanagementsystem1@gmail.com"
        # Gmail password configured - needs to be 16-character App Password
        self.sender_password = "beehive123"  # Replace with 16-char App Password
        # Set to True to skip email sending for testing
        self.skip_emails = True  # Change to False when App Password is configured
        
    def send_registration_notification(self, user_data, package_info):
        """Send registration notification to beehivemanagementsystem1@gmail.com"""
        if self.skip_emails:
            logger.info("📧 [TEST MODE] Skipping admin email to beehivemanagementsystem1@gmail.com")
            logger.info(f"📧 [TEST MODE] Would send admin notification for {user_data['fullName']} ({user_data['email']})")
            return True  # Simulate success
            
        try:
            subject = f"🐝 New BeeSync Registration - {user_data['fullName']}"
            
            body = f"""
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <div style="background: linear-gradient(135deg, #F59E0B, #D97706); padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 20px;">
                        <h1 style="color: white; margin: 0;">🐝 New BeeSync Registration</h1>
                    </div>
                    
                    <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
                        <h2 style="color: #F59E0B; margin-top: 0;">User Information</h2>
                        <p><strong>Full Name:</strong> {user_data['fullName']}</p>
                        <p><strong>Display Name:</strong> {user_data['displayName']}</p>
                        <p><strong>Email:</strong> {user_data['email']}</p>
                        <p><strong>Phone:</strong> {user_data['phoneNumber']}</p>
                        <p><strong>Company:</strong> {user_data.get('company', 'Not provided')}</p>
                        <p><strong>Country:</strong> {user_data['country']}</p>
                        <p><strong>Registration Date:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    </div>
                    
                    <div style="background: #e8f5e8; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
                        <h2 style="color: #28a745; margin-top: 0;">📦 Package Information</h2>
                        <p><strong>Package:</strong> {package_info.get('title', 'N/A')}</p>
                        <p><strong>Price:</strong> {package_info.get('price', 'N/A')}/month</p>
                    </div>
                    
                    <div style="background: #fff3cd; padding: 15px; border-radius: 8px; border-left: 4px solid #F59E0B;">
                        <h3 style="color: #856404; margin-top: 0;">Next Steps:</h3>
                        <ul style="color: #856404;">
                            <li>Review the registration details</li>
                            <li>Contact the user at {user_data['email']} to complete the setup</li>
                            <li>Prepare the subscription for {package_info.get('title', 'selected package')}</li>
                        </ul>
                    </div>
                </div>
            </body>
            </html>
            """
            
            return self._send_email("beehivemanagementsystem1@gmail.com", subject, body)
            
        except Exception as e:
            logger.error(f"Error sending registration notification: {str(e)}")
            return False
            
    def send_thank_you_email(self, user_data, package_info):
        """Send thank you email to the user"""
        if self.skip_emails:
            logger.info(f"📧 [TEST MODE] Skipping thank you email to {user_data['email']}")
            logger.info(f"📧 [TEST MODE] Would send welcome email to {user_data['fullName']}")
            return True  # Simulate success
            
        try:
            subject = f"🎉 Welcome to BeeSync, {user_data['fullName']}!"
            
            body = f"""
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <div style="background: linear-gradient(135deg, #F59E0B, #D97706); padding: 30px; border-radius: 10px; text-align: center; margin-bottom: 20px;">
                        <h1 style="color: white; margin: 0; font-size: 2.5em;">🐝</h1>
                        <h1 style="color: white; margin: 10px 0 0 0;">Welcome to BeeSync!</h1>
                        <p style="color: #fff8dc; margin: 5px 0 0 0;">Your Intelligent Bee-Hive Management Partner</p>
                    </div>
                    
                    <div style="padding: 20px 0;">
                        <h2 style="color: #F59E0B;">Hello {user_data['fullName']}! 👋</h2>
                        <p>Thank you for choosing BeeSync for your beekeeping journey. We're thrilled to have you join our community of passionate beekeepers!</p>
                    </div>
                    
                    <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
                        <h3 style="color: #F59E0B; margin-top: 0;">📦 Your Registration Details</h3>
                        <p><strong>Package Selected:</strong> {package_info.get('title', 'N/A')}</p>
                        <p><strong>Monthly Fee:</strong> {package_info.get('price', 'N/A')}/month</p>
                        <p><strong>Registration Date:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    </div>
                    
                    <div style="background: #e8f5e8; padding: 20px; border-radius: 8px; margin: 20px 0;">
                        <h3 style="color: #28a745; margin-top: 0;">🚀 What's Next?</h3>
                        <ul>
                            <li><strong>Setup Call:</strong> Our team will contact you within 24 hours to complete your subscription setup</li>
                            <li><strong>Account Activation:</strong> We'll help you get your BeeSync dashboard up and running</li>
                            <li><strong>Training:</strong> Free onboarding session to help you make the most of BeeSync</li>
                            <li><strong>Support:</strong> Our dedicated support team is here to help you succeed</li>
                        </ul>
                    </div>
                    
                    <div style="background: #fff3cd; padding: 20px; border-radius: 8px; margin: 20px 0;">
                        <h3 style="color: #856404; margin-top: 0;">📞 Contact Information</h3>
                        <p style="color: #856404;"><strong>Email:</strong> beehivemanagementsystem1@gmail.com</p>
                        <p style="color: #856404;"><strong>Support:</strong> We're here to help you 24/7</p>
                    </div>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <p style="font-size: 1.1em; color: #F59E0B; font-weight: bold;">Welcome to the BeeSync family! 🐝✨</p>
                        <p>Together, we'll make your beekeeping more efficient, sustainable, and successful.</p>
                    </div>
                    
                    <div style="text-align: center; padding: 20px; border-top: 2px solid #F59E0B; margin-top: 30px;">
                        <p style="color: #666; font-size: 0.9em;">
                            © 2024 BeeSync - Intelligent Bee-Hive Management System<br>
                            This email was sent because you registered for our service.
                        </p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            return self._send_email(user_data['email'], subject, body)
            
        except Exception as e:
            logger.error(f"Error sending thank you email: {str(e)}")
            return False
    
    def _send_email(self, to_email, subject, html_body):
        """Send email using SMTP"""
        try:
            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = self.sender_email
            message["To"] = to_email
            
            # Create HTML part
            html_part = MIMEText(html_body, "html")
            message.attach(html_part)
            
            # Create SMTP session
            context = ssl.create_default_context()
            
            with smtplib.SMTP(self.smtp_server, self.port) as server:
                server.starttls(context=context)
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, to_email, message.as_string())
            
            logger.info(f"Email sent successfully to {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            return False

# Create email service instance
email_service = EmailService()

@app.route('/', methods=['GET'])
def root():
    """Root endpoint to confirm API is running"""
    return jsonify({
        'message': 'BeeSync Registration API is running! 🐝',
        'endpoints': [
            '/api/hive-register (POST)',
            '/api/health (GET)',
            '/api/routes (GET)'
        ]
    }), 200

@app.route('/api/hive-register', methods=['POST'])
def register_user():
    """Handle user registration and send emails automatically"""
    try:
        # Get registration data from request
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'No registration data provided'
            }), 400
        
        # Extract user data
        user_data = {
            'fullName': data.get('fullName', ''),
            'displayName': data.get('displayName', ''),
            'phoneNumber': data.get('phoneNumber', ''),
            'email': data.get('email', ''),
            'password': data.get('password', ''),
            'company': data.get('company', ''),
            'country': data.get('country', '')
        }
        
        # Extract package information
        package_info = {
            'title': data.get('packageTitle', ''),
            'price': data.get('packagePrice', '')
        }
        
        # Validate required fields
        required_fields = ['fullName', 'displayName', 'phoneNumber', 'email', 'password', 'country']
        missing_fields = [field for field in required_fields if not user_data.get(field)]
        
        if missing_fields:
            return jsonify({
                'success': False,
                'message': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400
        
        # Validate email format
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, user_data['email']):
            return jsonify({
                'success': False,
                'message': 'Invalid email format'
            }), 400
        
        logger.info(f"Processing registration for {user_data['fullName']} ({user_data['email']})")
        
        # Send emails automatically
        admin_email_sent = email_service.send_registration_notification(user_data, package_info)
        user_email_sent = email_service.send_thank_you_email(user_data, package_info)
        
        # Log email status
        if admin_email_sent:
            logger.info("Admin notification email sent successfully to beehivemanagementsystem1@gmail.com")
        else:
            logger.warning("Failed to send admin notification email")
            
        if user_email_sent:
            logger.info(f"Thank you email sent successfully to {user_data['email']}")
        else:
            logger.warning(f"Failed to send thank you email to {user_data['email']}")
        
        # Return success response
        if admin_email_sent or user_email_sent:
            return jsonify({
                'success': True,
                'message': 'Registration successful! Emails sent automatically.',
                'details': {
                    'admin_email_sent': admin_email_sent,
                    'user_email_sent': user_email_sent,
                    'user_email': user_data['email']
                }
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Registration processed but failed to send emails. Please check email configuration.'
            }), 500
            
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'An error occurred during registration. Please try again.'
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'BeeSync Registration API',
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }), 200

@app.route('/api/routes', methods=['GET'])
def list_routes():
    """List all available routes for debugging"""
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append({
            'endpoint': rule.endpoint,
            'methods': list(rule.methods),
            'rule': str(rule)
        })
    return jsonify({
        'available_routes': routes,
        'total_routes': len(routes)
    }), 200

if __name__ == '__main__':
    print("🐝 Starting BeeSync Registration API...")
    print("📧 Email service configured for automatic sending")
    print("🌐 API will be available at: http://127.0.0.1:5001")
    print("📝 Registration endpoint: http://127.0.0.1:5001/api/hive-register")
    app.run(debug=True, host='127.0.0.1', port=5001)