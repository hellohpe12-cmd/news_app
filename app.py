from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import requests
import os
import yaml
import google.generativeai as genai
import json

# Load configuration from properties.yml or environment variables
def load_config():
    # Check if we're in production (Render sets PORT env var, or we can check for other indicators)
    # Also check if properties.yml exists for local development
    config_path = os.path.join(os.path.dirname(__file__), 'properties.yml')

    # If properties.yml doesn't exist OR we're in production, use environment variables
    if not os.path.exists(config_path) or os.getenv('PORT') or os.getenv('RENDER_INSTANCE_ID'):
        return None  # Use environment variables

    # For local development, try to load properties.yml
    try:
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)
    except Exception as e:
        print(f"Warning: Could not load properties.yml: {e}. Using environment variables as fallback.")
        return None

# Load configuration
config = load_config()

app = Flask(__name__)

# Configuration setup
if config:
    app.config['SECRET_KEY'] = config['app']['secret_key']
    NEWS_API_KEY = config['news_api']['api_key']
    NEWS_API_BASE_URL = config['news_api']['base_url']
    GOOGLE_API_KEY = config['google_ai']['api_key']
    GOOGLE_PROJECT_ID = config['google_ai']['project_id']
    GOOGLE_REGION = config['google_ai']['region']
    GEMINI_MODEL = config['google_ai']['gemini_model']
    GEMINI_TUNED_MODEL = config['google_ai']['gemini_tuned_model']
    DEBUG_MODE = config['app']['debug']
    PORT = config['deployment']['port']
    HOST = config['deployment']['host']
else:
    # Fallback to environment variables
    from dotenv import load_dotenv
    load_dotenv()
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
    NEWS_API_KEY = os.getenv('NEWS_API_KEY')
    NEWS_API_BASE_URL = 'https://newsapi.org/v2'
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    GOOGLE_PROJECT_ID = os.getenv('GOOGLE_PROJECT_ID')
    GOOGLE_REGION = os.getenv('GOOGLE_REGION')
    GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-pro')
    GEMINI_TUNED_MODEL = os.getenv('GEMINI_TUNED_MODEL')
    DEBUG_MODE = os.getenv('DEBUG', 'False').lower() == 'true'
    PORT = int(os.getenv('PORT', 5000))
    HOST = os.getenv('HOST', '0.0.0.0')

# Initialize Google AI
try:
    if GOOGLE_API_KEY:
        genai.configure(api_key=GOOGLE_API_KEY)
        print("Gemini AI configured successfully from properties.yml")
    else:
        print("Warning: GOOGLE_API_KEY not found. AI content generation will use fallback.")
except Exception as e:
    print(f"Warning: Gemini AI initialization failed: {e}")

# News categories with descriptions
NEWS_CATEGORIES = {
    'technology': {
        'name': 'Technology',
        'description': 'Latest tech news, gadgets, AI, and innovation',
        'icon': 'laptop-code'
    },
    'business': {
        'name': 'Business',
        'description': 'Market updates, finance, and business strategies',
        'icon': 'briefcase'
    },
    'science': {
        'name': 'Science',
        'description': 'Scientific discoveries and research breakthroughs',
        'icon': 'microscope'
    },
    'health': {
        'name': 'Health',
        'description': 'Medical news, wellness tips, and health research',
        'icon': 'heartbeat'
    },
    'sports': {
        'name': 'Sports',
        'description': 'Sports news, scores, and athletic achievements',
        'icon': 'football-ball'
    },
    'entertainment': {
        'name': 'Entertainment',
        'description': 'Movies, music, celebrities, and pop culture',
        'icon': 'film'
    },
    'general': {
        'name': 'General',
        'description': 'Breaking news and current events worldwide',
        'icon': 'globe'
    }
}

COUNTRIES = {
    'us': 'United States',
    'gb': 'United Kingdom',
    'ca': 'Canada',
    'au': 'Australia',
    'in': 'India',
    'de': 'Germany',
    'fr': 'France',
    'jp': 'Japan'
}

class NewsService:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = NEWS_API_BASE_URL

    def get_top_headlines(self, category=None, country='us', page_size=20):
        """Fetch top headlines from News API"""
        url = f"{self.base_url}/top-headlines"
        params = {
            'apiKey': self.api_key,
            'country': country,
            'pageSize': page_size
        }

        if category and category != 'general':
            params['category'] = category

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'status': 'error', 'message': str(e)}

class ContentGenerator:
    def __init__(self):
        self.model_name = GEMINI_MODEL

    def generate_personalized_content(self, selected_articles, user_preferences=None):
        """Generate personalized content using Gemini AI"""
        try:
            # Prepare the prompt with selected articles
            articles_text = ""
            for i, article in enumerate(selected_articles, 1):
                title = article.get('title', 'No title')
                description = article.get('description', 'No description')
                content = article.get('content', 'No content')[:500] if article.get('content') else 'No content'
                source_name = 'Unknown'
                if article.get('source') and isinstance(article.get('source'), dict):
                    source_name = article.get('source', {}).get('name', 'Unknown')

                articles_text += f"""
Article {i}:
Title: {title}
Description: {description}
Content: {content}...
Source: {source_name}
---
"""

            prompt = f"""
You are an AI content creator that generates personalized news summaries and insights.

Based on the following news articles that the user has selected as interesting, create a comprehensive, engaging, and personalized content piece that:

1. Summarizes the key points from all articles
2. Identifies common themes and trends
3. Provides unique insights and analysis
4. Connects the stories in a meaningful way
5. Offers a personalized perspective based on the user's interests

Selected Articles:
{articles_text}

User Preferences: {user_preferences or 'General interest in selected topics'}

Please create a well-structured, engaging article (800-1200 words) that synthesizes these news stories into valuable, personalized content. Include:
- An engaging headline
- A compelling introduction
- Main insights and analysis
- Key takeaways
- A thoughtful conclusion

Format the response as a proper article with clear sections.
"""

            # Try to use Gemini AI
            try:
                model = genai.GenerativeModel(self.model_name)
                response = model.generate_content(prompt)

                # Check if response has text
                if hasattr(response, 'text') and response.text:
                    return {
                        'status': 'success',
                        'content': response.text,
                        'articles_count': len(selected_articles),
                        'generation_method': 'gemini_ai'
                    }
                else:
                    # If no text in response, use fallback
                    return {
                        'status': 'success',
                        'content': self._generate_fallback_content(selected_articles, user_preferences),
                        'articles_count': len(selected_articles),
                        'generation_method': 'fallback',
                        'ai_error': 'No text in AI response'
                    }

            except Exception as ai_error:
                print(f"AI generation failed: {ai_error}")
                # Fall back to template-based generation
                return {
                    'status': 'success',
                    'content': self._generate_fallback_content(selected_articles, user_preferences),
                    'articles_count': len(selected_articles),
                    'generation_method': 'fallback',
                    'ai_error': str(ai_error)
                }

        except Exception as e:
            print(f"Content generation error: {e}")
            return {
                'status': 'success',
                'content': self._generate_fallback_content(selected_articles, user_preferences),
                'articles_count': len(selected_articles),
                'generation_method': 'fallback',
                'error': str(e)
            }

    def _generate_fallback_content(self, articles, user_preferences=None):
        """Generate enhanced fallback content if AI fails"""
        content = "# Your Personalized News Summary\n\n"

        if user_preferences:
            content += f"*Based on your interests: {user_preferences}*\n\n"

        content += f"We've analyzed {len(articles)} articles you selected and created this personalized summary:\n\n"

        # Group articles by topic if available
        topics = {}
        for article in articles:
            topic = article.get('topic_name', 'General')
            if topic not in topics:
                topics[topic] = []
            topics[topic].append(article)

        # Generate content by topic
        for topic, topic_articles in topics.items():
            content += f"## {topic} News\n\n"

            for article in topic_articles:
                title = article.get('title', 'Untitled')
                description = article.get('description', 'No description available')
                source = article.get('source', {}).get('name', 'Unknown Source')

                content += f"### {title}\n"
                content += f"*Source: {source}*\n\n"
                content += f"{description}\n\n"

        # Add insights section
        content += "## Key Insights\n\n"
        content += "- These stories reflect current trends in the topics you're interested in\n"
        content += "- The news sources provide diverse perspectives on important developments\n"
        content += "- Stay informed with these carefully selected articles that match your preferences\n\n"

        content += "## What This Means For You\n\n"
        content += "Based on your selected articles, here are the key takeaways:\n\n"
        content += "1. **Stay Updated**: These stories represent the most current developments in your areas of interest\n"
        content += "2. **Informed Decisions**: Use these insights to make better personal and professional choices\n"
        content += "3. **Broader Perspective**: Understanding these trends helps you see the bigger picture\n\n"

        content += "*This summary was generated based on your article selections and preferences.*"

        return content

# Initialize services
print(f"Initializing news service with API key: {'*' * (len(NEWS_API_KEY) - 4) + NEWS_API_KEY[-4:] if NEWS_API_KEY else 'None'}")
if not NEWS_API_KEY:
    print("ERROR: NEWS_API_KEY is not set! News functionality will not work.")
news_service = NewsService(NEWS_API_KEY)
content_generator = ContentGenerator()

@app.route('/')
def index():
    """Step 1: Topic Selection Page"""
    return render_template('topic_selection.html', categories=NEWS_CATEGORIES, countries=COUNTRIES)

@app.route('/news-feed')
def news_feed():
    """Step 2: Show news from selected topics"""
    selected_topics = request.args.getlist('topics')
    country = request.args.get('country', 'us')

    if not selected_topics:
        return redirect(url_for('index'))

    # Store selections in session
    session['selected_topics'] = selected_topics
    session['selected_country'] = country

    return render_template('news_feed.html',
                         topics=selected_topics,
                         country=country,
                         categories=NEWS_CATEGORIES,
                         countries=COUNTRIES)

@app.route('/debug/config')
def debug_config():
    """Debug endpoint to check configuration on Render"""
    return jsonify({
        'news_api_key_set': bool(NEWS_API_KEY),
        'news_api_key_length': len(NEWS_API_KEY) if NEWS_API_KEY else 0,
        'news_api_base_url': NEWS_API_BASE_URL,
        'render_env': bool(os.getenv('RENDER')),
        'config_source': 'environment_variables' if not config else 'properties_yml'
    })

@app.route('/api/news')
def get_news():
    """API endpoint to fetch news for selected topics"""
    topics = request.args.getlist('topics')
    country = request.args.get('country', 'us')

    if not NEWS_API_KEY:
        return jsonify({
            'status': 'error',
            'message': 'News API key is not configured. Please check environment variables.',
            'articles': [],
            'total': 0
        })

    all_articles = []
    errors = []

    for topic in topics:
        try:
            print(f"Fetching news for topic: {topic}, country: {country}")
            news_data = news_service.get_top_headlines(topic, country, 10)

            if news_data.get('status') == 'ok' and news_data.get('articles'):
                # Add topic info to each article
                for article in news_data['articles']:
                    article['topic'] = topic
                    article['topic_name'] = NEWS_CATEGORIES.get(topic, {}).get('name', topic)
                all_articles.extend(news_data['articles'])
                print(f"Successfully fetched {len(news_data['articles'])} articles for {topic}")
            elif news_data.get('status') == 'error':
                error_msg = f"Error fetching {topic}: {news_data.get('message', 'Unknown error')}"
                print(error_msg)
                errors.append(error_msg)
            else:
                print(f"No articles found for topic: {topic}")

        except Exception as e:
            error_msg = f"Exception fetching {topic}: {str(e)}"
            print(error_msg)
            errors.append(error_msg)

    response = {
        'status': 'ok' if all_articles else 'error',
        'articles': all_articles,
        'total': len(all_articles)
    }

    if errors:
        response['errors'] = errors

    if not all_articles and not errors:
        response['message'] = 'No articles found for the selected topics'

    print(f"Returning {len(all_articles)} total articles")
    return jsonify(response)

@app.route('/generate-content', methods=['POST'])
def generate_content():
    """Step 3: Generate personalized content from selected articles"""
    data = request.get_json()
    selected_articles = data.get('articles', [])
    user_preferences = data.get('preferences', '')

    if not selected_articles:
        return jsonify({'status': 'error', 'message': 'No articles selected'})

    # Generate content using Gemini or fallback
    result = content_generator.generate_personalized_content(selected_articles, user_preferences)

    return jsonify(result)

@app.route('/personalized-content')
def personalized_content():
    """Step 3: Display generated personalized content"""
    return render_template('personalized_content.html')

@app.route('/preferences')
def preferences():
    """User preferences management"""
    return render_template('preferences.html',
                         categories=NEWS_CATEGORIES,
                         countries=COUNTRIES)

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', error="Page not found"), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', error="Internal server error"), 500

if __name__ == '__main__':
    if not NEWS_API_KEY or NEWS_API_KEY == 'your_api_key_here':
        print("Warning: Please set your NEWS_API_KEY in properties.yml")
        print("Get your free API key from: https://newsapi.org/register")

    app.run(debug=DEBUG_MODE, host=HOST, port=PORT)
