# Analytica Web View 📊

**Analytica Web View** is a Flask-based web dashboard designed to analyze and visualize social media metrics interactively. By processing pre-collected data, the application generates insightful charts to track user sentiment, content engagement, and overall volume trends using Plotly.

## 🚀 Features

- **Overview Dashboard:** Get a high-level summary of social media activity, including the number of posts per day and the frequency of top hashtags.
- **Sentiment Analysis:** Track the average sentiment score over time, complete with pie charts classifying sentiment into Positive, Neutral, and Negative categories, and histograms to show score distributions.
- **Engagement Metrics:** Analyze user interactions by breaking down engagement types (likes, retweets, replies, views) over time, identifying peak engagement days and the most impactful hashtags.
- **Interactive Visualizations:** All charts are powered by Plotly, offering a responsive, zoomable, and interactive experience.
- **Modern UI:** A sleek, GitHub-inspired dark theme designed for optimal readability and a professional look.

## 🛠️ Technology Stack

- **Backend:** Python, Flask
- **Data Manipulation:** Pandas
- **Data Visualization:** Plotly (Plotly Express & Plotly Graph Objects)
- **Frontend:** HTML, CSS, Jinja2 (Templates)

## 📁 Project structure

```
Analytica-web-view/
│
├── app.py                   # Main Flask application with routing logic
├── data_loader.py           # Data processing and Plotly chart generation
│
├── data/                    # (Expected) CSV Data files
│   ├── engagement_per_day.csv
│   ├── sentiment_per_day.csv
│   ├── top_hashtags.csv
│   └── tweets_per_day.csv
│
├── static/
│   └── style.css            # Custom CSS for the dark-themed UI
│
└── templates/               # HTML templates (Jinja2)
    ├── base.html            # Base layout template
    ├── dashboard.html / index.html
    ├── engagement.html
    └── sentiment.html
```

## ⚙️ How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/es-salmiadam/Analytica-web-view.git
   cd Analytica-web-view
   ```

2. **Install dependencies:**
   Make sure you have Python installed. Install the required packages using pip:
   ```bash
   pip install flask pandas plotly
   ```

3. **Run the Flask application:**
   ```bash
   python app.py
   ```

4. **Access the dashboard:**
   Open your web browser and navigate to `http://127.0.0.1:5000`

## 📊 Data Format 
This dashboard expects four CSV files for its data sources (typically placed in the root directory relative to `app.py`):
- `tweets_per_day.csv`: Tracks daily post volume.
- `engagement_per_day.csv`: Tracks metrics like `likeCount`, `replyCount`, and `retweetCount`.
- `sentiment_per_day.csv`: Contains the daily `avg_sentiment` score.
- `top_hashtags.csv`: Counts the frequency of various hashtags.

## 📄 License
This project is open-source and available under the MIT License.
