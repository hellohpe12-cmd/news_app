# News Hub Application - Wireframe Design

## Overview
A 3-step personalized news application that curates content based on user interests and generates AI-powered summaries.

---

## Page Flow Architecture

```
[Landing Page] → [News Feed] → [Personalized Content]
     ↓              ↓              ↓
[Topic Selection] [Article Selection] [AI Generated Summary]
```

---

## 1. Landing Page - Topic Selection (`/`)

### Header Section
```
┌─────────────────────────────────────────────────────────────┐
│                        News Hub                              │
│                   🎯 Choose Your News Interests             │
│    Select the topics you're most interested in, and         │
│         we'll find the latest news for you                  │
└─────────────────────────────────────────────────────────────┘
```

### Region Selection
```
┌─────────────────────────────────────────────────────────────┐
│                  🌍 Select Your Region                      │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ [Dropdown: United States ▼]                         │   │
│  │ Options: US, UK, Canada, Australia, India,          │   │
│  │          Germany, France, Japan                     │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Topic Selection Grid (3x3 Layout)
```
┌─────────────────────────────────────────────────────────────┐
│                🏷️  Choose Your News Categories               │
│           Select at least one category (multiple OK)        │
│                                                             │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐           │
│ │ 💻 Tech     │ │ 💼 Business │ │ 🔬 Science  │           │
│ │ Latest tech │ │ Market      │ │ Scientific  │           │
│ │ news, AI,   │ │ updates,    │ │ discoveries │           │
│ │ innovation  │ │ finance     │ │ & research  │           │
│ │    [ ]      │ │    [ ]      │ │    [ ]      │           │
│ └─────────────┘ └─────────────┘ └─────────────┘           │
│                                                             │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐           │
│ │ ❤️ Health   │ │ ⚽ Sports   │ │ 🎬 Entertain│           │
│ │ Medical     │ │ Sports news,│ │ Movies,     │           │
│ │ news, well- │ │ scores,     │ │ music,      │           │
│ │ ness tips   │ │ athletics   │ │ celebrities │           │
│ │    [ ]      │ │    [ ]      │ │    [ ]      │           │
│ └─────────────┘ └─────────────┘ └─────────────┘           │
│                                                             │
│ ┌─────────────┐                                           │
│ │ 🌍 General  │                                           │
│ │ Breaking    │                                           │
│ │ news &      │                                           │
│ │ current     │                                           │
│ │ events      │                                           │
│ │    [ ]      │                                           │
│ └─────────────┘                                           │
└─────────────────────────────────────────────────────────────┘
```

### Quick Presets
```
┌─────────────────────────────────────────────────────────────┐
│                   ⚡ Quick Presets                          │
│ [Tech Enthusiast] [Business Pro] [Science Lover] [All News]│
└─────────────────────────────────────────────────────────────┘
```

### Action Buttons
```
┌─────────────────────────────────────────────────────────────┐
│              [Find My News →] (0 selected)                 │
│                                                             │
│           [Select All]    [Clear All]                      │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. News Feed Page (`/news-feed`)

### Header Section
```
┌─────────────────────────────────────────────────────────────┐
│ 📰 Your Personalized News Feed        [← Change Topics]    │
│ Topics: [Tech] [Business] | Country: [United States]       │
└─────────────────────────────────────────────────────────────┘
```

### Selection Controls
```
┌─────────────────────────────────────────────────────────────┐
│ 👆 Select articles you find interesting:                   │
│ We'll use your selected articles to create personalized    │
│ content                                                     │
│                                                             │
│ Selected: 0 articles                                       │
│ [Select All Visible] [Clear Selection] [Generate Content →]│
└─────────────────────────────────────────────────────────────┘
```

### News Articles Grid
```
┌─────────────────────────────────────────────────────────────┐
│                      Loading Articles...                    │
│                    [Loading Spinner]                       │
└─────────────────────────────────────────────────────────────┘

// After loading:

┌─────────────────────────────────────────────────────────────┐
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ [ ] TECH: Revolutionary AI Breakthrough                │ │
│ │     Scientists develop new machine learning algorithm   │ │
│ │     that can...                                        │ │
│ │     📰 TechCrunch | 🕒 2 hours ago                     │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ [ ] BUSINESS: Stock Market Reaches New Heights         │ │
│ │     Market analysts predict continued growth as...      │ │
│ │     📰 Bloomberg | 🕒 1 hour ago                       │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ [✓] TECH: Apple Announces New Product Line             │ │
│ │     The tech giant unveiled its latest innovations...   │ │
│ │     📰 Apple News | 🕒 30 minutes ago                  │ │
│ └─────────────────────────────────────────────────────────┘ │
│                          ...                               │
└─────────────────────────────────────────────────────────────┘
```

### Filter and Sort Controls
```
┌─────────────────────────────────────────────────────────────┐
│ Filter: [All Topics ▼] | Sort: [Latest First ▼] | 📊 25 articles��
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Personalized Content Page (`/personalized-content`)

### Loading State
```
┌─────────────────────────────────────────────────────────────┐
│                  [Loading Spinner]                         │
│           Generating Your Personalized Content             │
│    Our AI is analyzing your selected articles and          │
│        creating unique content just for you...             │
└─────────────────────────────────────────────────────────────┘
```

### Generated Content Display
```
┌────────��────────────────────────────────────────────────────┐
│ ✨ Your Personalized Content                [Share] [Download] [← Back]│
│ 🤖 Generated by Gemini AI | 🕒 Generated at 2:30 PM        │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                      GENERATED ARTICLE                      │
│                                                             │
│ # Technology and Business Trends: Your Weekly Digest       │
│                                                             │
│ Based on your selected articles, here are the key insights │
│ and trends shaping the tech and business world this week... │
│                                                             │
│ ## Key Highlights                                          │
│ • Revolutionary AI developments in machine learning         │
│ • Stock market reaches unprecedented heights                │
│ • Apple's latest product innovations                        │
│                                                             │
│ ## Analysis and Insights                                   │
│ [AI-generated detailed analysis of selected articles]      │
│                                                             │
│ ## What This Means For You                                 │
│ [Personalized implications and recommendations]            │
│                                                             │
│ ## Sources                                                 │
│ Based on 3 articles from TechCrunch, Bloomberg, Apple News │
└─────────────────────────────────────────────────────────────┘
```

### Content Actions
```
┌─────────────────────────────────────────────────────────────┐
│ [📧 Email This] [💾 Save to Reading List] [🔗 Get Link]    │
│ [🔄 Generate New Content] [🏠 Start Over]                  │
└─────────────────────────────────────────────────────────────┘
```

---

## 4. Debug/Admin Page (`/debug/config`)

### Configuration Status
```
┌─────────────────────────────────────────────────────────────┐
│                    System Configuration                     │
│                                                             │
│ News API Key: ✅ Set (Length: 32)                          │
│ Google AI API: ✅ Configured                               │
│ Base URL: https://newsapi.org/v2                           │
│ Config Source: environment_variables                       │
│ Render Environment: ✅ Detected                            │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. Error Pages (`/404`, `/500`)

### 404 Error
```
┌─────────────────────────────────────────────────────────────┐
│                        🚫 404                              │
│                   Page Not Found                           │
│                                                             │
│         The page you're looking for doesn't exist          │
│                                                             │
│                 [🏠 Go Home] [📰 Browse News]              │
└─────────────────────────────────────────────────────────────┘
```

### 500 Error
```
┌─────────────────────────────────────────────────────────────┐
│                        ⚠️ 500                              │
│                Internal Server Error                       │
│                                                             │
│        Something went wrong on our end. Please try         │
│                    again later.                            │
│                                                             │
│                 [🔄 Try Again] [🏠 Go Home]                │
└─────────────────────────────────────────────────────────────┘
```

---

## User Experience Flow

### Happy Path
1. **Land on homepage** → See topic selection interface
2. **Select region** → Choose country for news sources
3. **Pick topics** → Select 1+ categories (visual feedback)
4. **Submit** → Navigate to news feed
5. **Browse articles** → See curated news from selected topics
6. **Select articles** → Check interesting articles (counter updates)
7. **Generate content** → AI creates personalized summary
8. **Read/Share** → View generated content, share or download

### Error Handling
- **No topics selected**: Warning message, disabled submit button
- **API failures**: Fallback content generation
- **No articles found**: Helpful message with retry option
- **AI generation fails**: Template-based content generation

### Responsive Design Considerations
- **Mobile**: Stacked cards, single column layout
- **Tablet**: 2-column grid for topics and articles
- **Desktop**: 3-column grid, optimal reading width

### Key Interactive Elements
- **Topic cards**: Hover effects, selection indicators
- **Article cards**: Checkbox selection, visual feedback
- **Loading states**: Spinners and progress indicators
- **Action buttons**: State-dependent enabling/disabling

This wireframe represents a complete 3-step user journey from interest selection to AI-generated personalized content, with robust error handling and responsive design considerations.
