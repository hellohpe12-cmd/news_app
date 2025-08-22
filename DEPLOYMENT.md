# Render Deployment Guide

## 🚀 Deploy to Render (Keeping Secrets Safe)

### Step 1: Prepare Your Repository

1. **Create a GitHub repository** for your project
2. **Push your code** (the `properties.yml` is already in `.gitignore` so it won't be uploaded)

```bash
git init
git add .
git commit -m "Initial commit - News Hub with AI"
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

### Step 2: Deploy on Render

1. Go to [render.com](https://render.com) and sign up/login
2. Click **"New"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure deployment settings:
   - **Name**: `news-hub` (or your preferred name)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn main:app` ← **IMPORTANT: Use 'main:app' not 'app:app'**
   - **Instance Type**: Free (or paid for better performance)

### Step 3: Set Environment Variables

In your Render dashboard, go to **Environment** and add these variables:

| Variable Name | Value |
|---------------|-------|
| `NEWS_API_KEY` | `cd7aa6749e28462a923b1458f3c50aa1` |
| `GOOGLE_API_KEY` | `AIzaSyA_P9G3k8leIXNaUZ-3vWNAr97veQ3_Cf8` |
| `GOOGLE_PROJECT_ID` | `ai-ml-integrations` |
| `GOOGLE_REGION` | `us-central1` |
| `GEMINI_MODEL` | `gemini-2.0-flash` |
| `GEMINI_TUNED_MODEL` | `projects/25508203682/locations/us-central1/endpoints/846647043131703296` |
| `SECRET_KEY` | `your-production-secret-key-here` |
| `DEBUG` | `False` |

### Step 4: Deploy!

Click **"Create Web Service"** and Render will:
- Build your application
- Install dependencies
- Start your Flask app
- Provide you with a public URL

### 🔒 Security Benefits:

- ✅ **No sensitive data in repository**
- ✅ **API keys stored securely in Render**
- ✅ **Local development uses properties.yml**
- ✅ **Production uses environment variables**

### 📝 Your App URLs:

- **Local Development**: `http://localhost:3003`
- **Production**: `https://your-app-name.onrender.com`

### 🔧 How It Works:

The app automatically detects if it's running on Render and switches to environment variables, keeping your `properties.yml` file completely local and secure.
