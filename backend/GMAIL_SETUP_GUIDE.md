# 🔑 Gmail App Password Setup for BeeSync Registration

## Why App Password is Needed

Gmail requires a special **16-character App Password** for SMTP authentication, not your regular password.
Your regular password `beehive123` won't work for sending emails via SMTP.

## Step-by-Step Setup

### Step 1: Enable 2-Factor Authentication
1. Go to your Google Account: https://myaccount.google.com/
2. Click **Security** on the left
3. Find **2-Step Verification** and turn it ON
4. Follow the setup process (phone verification, etc.)

### Step 2: Generate App Password
1. Still in **Security** section
2. Look for **App passwords** (appears only after 2FA is enabled)
3. Click **App passwords**
4. Select:
   - App: **Mail**
   - Device: **Windows Computer** (or your device)
5. Click **Generate**
6. **Copy the 16-character password** (example: `abcd efgh ijkl mnop`)

### Step 3: Update Registration API
Replace `beehive123` with your 16-character App Password in the file:
`c:\bee-hive-management-system\backend\registration_api.py`

Find line 21:
```python
self.sender_password = "beehive123"
```

Replace with:
```python
self.sender_password = "your_16_char_app_password"
```

## Alternative: Test Without Emails

If you want to test registration without setting up emails immediately, I can modify the code to skip email sending and just show success messages.

## Quick Test Commands

After setting up App Password:
```bash
cd c:\bee-hive-management-system\backend
python registration_api.py
```

Then test registration from the frontend at:
http://localhost:5173/packages

## Troubleshooting

If you still get authentication errors:
1. **Double-check** the App Password is exactly 16 characters
2. **Remove spaces** from the App Password when copying
3. **Make sure** 2-Factor Authentication is enabled
4. **Try generating** a new App Password if the first one doesn't work

## Security Notes
- **Never share** your App Password
- **Use different** App Passwords for different applications
- **Revoke** App Passwords you're no longer using