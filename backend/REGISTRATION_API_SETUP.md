# 🐝 BeeSync Registration API - Main Backend Setup

## New Location
The registration API has been moved to the main backend folder:
`c:\bee-hive-management-system\backend\registration_api.py`

## Quick Start

### Step 1: Run the Registration API
```powershell
cd c:\bee-hive-management-system\backend
python registration_api.py
```

### Step 2: Start Frontend
```powershell
cd c:\bee-hive-management-system\frontend
npm start
```

### Step 3: Test Registration
1. Go to: `http://localhost:3000/packages`
2. Click "Get started" on any package
3. Fill out registration form
4. Click "Register" button
5. Success popup + automatic emails sent!

## API Details

### Endpoint
- **URL:** `http://127.0.0.1:5000/api/hive-register`
- **Method:** POST
- **Port:** 5000

### Email Configuration
- ✅ **Admin Email:** beehivemanagementsystem1@gmail.com
- ✅ **Password:** beehive123 (configured)
- ✅ **Automatic sending:** No Outlook opening

### Features
- 📧 Automatic admin notification email
- 🎉 Automatic user thank you email
- ✅ Professional HTML email templates
- 🚫 No email client opening
- 📝 Form validation and error handling

## Commands

### Start API Only
```bash
cd c:\bee-hive-management-system\backend
python registration_api.py
```

### Health Check
```bash
curl http://127.0.0.1:5000/api/health
```

### Test Registration
- Frontend will automatically use: `http://127.0.0.1:5000/api/hive-register`
- No frontend changes needed - endpoint remains the same!

## Success Indicators
- ✅ Console shows: "Email sent successfully to..."
- ✅ Frontend shows success popup
- ✅ Both admin and user receive emails
- ✅ No email client windows open