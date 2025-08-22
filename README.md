# News Hub - Personalized News Website

A Flask-based news website that integrates with NewsAPI to provide personalized news content based on user preferences.

## Features

- **Personalized News**: Choose from multiple categories (Business, Technology, Sports, Health, etc.)
- **Country Selection**: Get news from different countries (US, UK, Canada, India, etc.)
- **Search Functionality**: Search for specific news topics
- **Responsive Design**: Mobile-friendly interface using Bootstrap
- **User Preferences**: Save and manage your news preferences
- **Real-time Updates**: Dynamic loading of news articles

## Setup Instructions

### 1. Get Your News API Key

1. Visit [NewsAPI.org](https://newsapi.org/register)
2. Sign up for a free account
3. Get your API key from the dashboard

### 2. Configure Environment Variables

1. Open the `.env` file in your project root
2. Replace `your_api_key_here` with your actual News API key:
   ```
   NEWS_API_KEY=your_actual_api_key_here
   DEBUG=True
   ```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Locally

```bash
python main.py
```

The application will be available at `http://localhost:5000`

## Deployment on Render

### Step 1: Prepare Your Code
1. Push your code to a GitHub repository
2. Make sure your `.env` file is NOT committed (it's in .gitignore)

### Step 2: Deploy on Render
1. Go to [Render.com](https://render.com) and sign up
2. Click "New" → "Web Service"
3. Connect your GitHub repository
4. Configure the deployment:
   - **Name**: `news-hub` (or any name you prefer)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn main:app`
   - **Python Version**: `3.11.0` (or your preferred version)

### Step 3: Set Environment Variables
In Render dashboard, go to your service → Environment:
- Add `NEWS_API_KEY` with your actual API key
- Add `DEBUG` with value `False`

### Step 4: Deploy
Click "Deploy" and wait for the deployment to complete.

## Project Structure

```
news_app/
├── main.py                 # Flask application
├── requirements.txt        # Python dependencies
├── Procfile               # Render deployment config
├── build.sh               # Build script
├── .env                   # Environment variables (not in git)
├── templates/
│   ├── base.html          # Base template
│   ├── index.html         # Main news page
│   ├── preferences.html   # User preferences page
│   └── error.html         # Error page
└── README.md              # This file
```

## API Endpoints

- `GET /` - Main news page with category selection
- `GET /news` - API endpoint to fetch news (accepts category, country, search params)
- `GET /preferences` - User preferences page

## News Categories Available

- General
- Business
- Entertainment
- Health
- Science
- Sports
- Technology

## Supported Countries

- United States (US)
- United Kingdom (GB)
- Canada (CA)
- Australia (AU)
- India (IN)
- Germany (DE)
- France (FR)
- Japan (JP)

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **API**: NewsAPI.org
- **Deployment**: Render
- **Dependencies**: requests, python-dotenv, gunicorn

## Usage

1. **Home Page**: Select your preferred news category and country, then click "Load News"
2. **Search**: Use the search bar to find specific news topics
3. **Preferences**: Visit the preferences page to save your favorite categories and regions
4. **Read Articles**: Click "Read More" on any article to visit the original source

## Troubleshooting

### API Key Issues
- Make sure your News API key is valid and active
- Check that you haven't exceeded your API rate limits (free tier has limits)

### Deployment Issues
- Ensure all environment variables are set correctly in Render
- Check the build logs for any dependency issues

### No News Loading
- Verify your internet connection
- Check if NewsAPI.org is accessible
- Review browser console for JavaScript errors

## Contributing

Feel free to fork this project and submit pull requests for improvements!

## License

This project is open source and available under the MIT License.
