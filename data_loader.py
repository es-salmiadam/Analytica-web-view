import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.utils
import json
import os

def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    tweets_per_day = pd.read_csv(os.path.join(base_dir, 'tweets_per_day.csv'))
    engagement_per_day = pd.read_csv(os.path.join(base_dir, 'engagement_per_day.csv'))
    sentiment_per_day = pd.read_csv(os.path.join(base_dir, 'sentiment_per_day.csv'))
    top_hashtags = pd.read_csv(os.path.join(base_dir, 'top_hashtags.csv'))
    
    return tweets_per_day, engagement_per_day, sentiment_per_day, top_hashtags

def generate_charts():
    tweets_per_day, engagement_per_day, sentiment_per_day, top_hashtags = load_data()
    
    # 1. Tweets Per Day - Line Chart
    fig_tweets = px.line(tweets_per_day, x=tweets_per_day.columns[0], y=tweets_per_day.columns[1], 
                         title='Number of Tweets Per Day',
                         template='plotly_white',
                         line_shape='spline')
    fig_tweets.update_traces(line_color='#58a6ff')
    fig_tweets.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                             font_color='#c9d1d9', margin=dict(t=40, b=0, l=0, r=0),
                             xaxis=dict(gridcolor='#30363d'), yaxis=dict(gridcolor='#30363d'))
    tweets_json = json.dumps(fig_tweets, cls=plotly.utils.PlotlyJSONEncoder)

    # 2. Engagement Per Day - Line Chart
    fig_eng = px.line(engagement_per_day, x='day', y=['likeCount', 'replyCount', 'retweetCount', 'viewCount'], 
                      title='Engagement Over Time',
                      template='plotly_white',
                      color_discrete_sequence=['#58a6ff', '#f85149', '#3fb950', '#8957e5'])
    fig_eng.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                          font_color='#c9d1d9', margin=dict(t=40, b=0, l=0, r=0),
                          xaxis=dict(gridcolor='#30363d'), yaxis=dict(gridcolor='#30363d'))
    eng_json = json.dumps(fig_eng, cls=plotly.utils.PlotlyJSONEncoder)
    
    # 3. Sentiment Per Day - Line chart with colored zones
    # avg_sentiment is a score between 0 and 1. Higher = more positive.
    fig_sent = px.line(sentiment_per_day, x='day', y='avg_sentiment',
                       title='Average Sentiment Score Over Time',
                       template='plotly_white')
    fig_sent.update_traces(line_color='#3fb950', fill='tozeroy', 
                           fillcolor='rgba(63, 185, 80, 0.1)')
    # Add a reference line for the overall average
    avg_val = sentiment_per_day['avg_sentiment'].mean()
    fig_sent.add_hline(y=avg_val, line_dash="dash", line_color="#d29922",
                       annotation_text=f"Avg: {avg_val:.3f}", annotation_position="top right")
    fig_sent.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                           font_color='#c9d1d9', margin=dict(t=40, b=0, l=0, r=0),
                           xaxis=dict(gridcolor='#30363d'), yaxis=dict(gridcolor='#30363d'))
    sent_json = json.dumps(fig_sent, cls=plotly.utils.PlotlyJSONEncoder)
    
    # 4. Top Hashtags - Horizontal Bar using go.Bar for explicit control
    top_hashtags['count'] = top_hashtags['count'].astype(int)
    # Sort ascending for horizontal bar display
    th_sorted = top_hashtags.sort_values('count', ascending=True)
    fig_hash = go.Figure(go.Bar(
        x=th_sorted['count'].tolist(),
        y=th_sorted['hashtag'].tolist(),
        orientation='h',
        marker=dict(
            color=th_sorted['count'].tolist(),
            colorscale=[[0, '#30363d'], [0.5, '#58a6ff'], [1, '#8957e5']]
        )
    ))
    max_count = th_sorted['count'].max()
    fig_hash.update_layout(
        title='Top Hashtags by Frequency',
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font_color='#c9d1d9', margin=dict(t=40, b=0, l=0, r=0),
        height=500,
        yaxis=dict(gridcolor='#30363d', dtick=1),
        xaxis=dict(gridcolor='#30363d', range=[0, max_count * 1.1], type='linear'),
        showlegend=False
    )
    hash_json = json.dumps(fig_hash, cls=plotly.utils.PlotlyJSONEncoder)
    
    # Summary stats
    summary_stats = {
        'total_tweets': int(tweets_per_day[tweets_per_day.columns[1]].sum()),
        'total_engagement': int(engagement_per_day[engagement_per_day.columns[1:]].sum().sum()),
    }
    
    try:
        summary_stats['top_hashtag'] = top_hashtags.iloc[0, 0]
    except Exception:
        summary_stats['top_hashtag'] = "N/A"

    return {
        'tweets_chart': tweets_json,
        'engagement_chart': eng_json,
        'sentiment_chart': sent_json,
        'hashtag_chart': hash_json,
        'stats': summary_stats
    }
