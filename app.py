from flask import Flask, render_template
from data_loader import generate_charts, load_data
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.utils
import json
import os

app = Flask(__name__)

@app.route('/')
def dashboard():
    chart_data = generate_charts()
    return render_template('index.html', chart_data=chart_data, active_page='dashboard')

@app.route('/sentiment')
def sentiment():
    chart_data = generate_charts()
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    sentiment_per_day = pd.read_csv(os.path.join(base_dir, 'sentiment_per_day.csv'))
    
    # Classify sentiment scores into categories
    # avg_sentiment is 0..1, with higher = more positive
    def classify(score):
        if score >= 0.11:
            return 'Positive'
        elif score >= 0.085:
            return 'Neutral'
        else:
            return 'Negative'
    
    sentiment_per_day['category'] = sentiment_per_day['avg_sentiment'].apply(classify)
    
    # Pie chart of sentiment category distribution
    cat_counts = sentiment_per_day['category'].value_counts().reset_index()
    cat_counts.columns = ['category', 'days']
    fig_pie = px.pie(cat_counts, names='category', values='days',
                     title='Sentiment Category Distribution',
                     template='plotly_white',
                     color='category',
                     color_discrete_map={'Positive': '#3fb950', 'Neutral': '#d29922', 'Negative': '#f85149'})
    fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                          font_color='#c9d1d9', margin=dict(t=40, b=0, l=0, r=0))
    pie_json = json.dumps(fig_pie, cls=plotly.utils.PlotlyJSONEncoder)
    
    # Histogram of sentiment score distribution using go.Histogram for explicit control
    scores = sentiment_per_day['avg_sentiment'].astype(float).tolist()
    fig_hist = go.Figure(go.Histogram(
        x=scores,
        nbinsx=25,
        marker_color='#58a6ff',
        marker_line=dict(color='#21262d', width=1)
    ))
    fig_hist.update_layout(
        title='Distribution of Daily Sentiment Scores',
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font_color='#c9d1d9', margin=dict(t=40, b=0, l=0, r=0),
        xaxis=dict(gridcolor='#30363d', title='Sentiment Score', range=[0, 0.22]),
        yaxis=dict(gridcolor='#30363d', title='Number of Days'),
        bargap=0.05
    )
    hist_json = json.dumps(fig_hist, cls=plotly.utils.PlotlyJSONEncoder)
    
    # Compute sentiment insight stats
    avg_score = sentiment_per_day['avg_sentiment'].mean()
    best_idx = sentiment_per_day['avg_sentiment'].idxmax()
    worst_idx = sentiment_per_day['avg_sentiment'].idxmin()
    best_day = sentiment_per_day.loc[best_idx, 'day']
    best_score = sentiment_per_day.loc[best_idx, 'avg_sentiment']
    worst_day = sentiment_per_day.loc[worst_idx, 'day']
    worst_score = sentiment_per_day.loc[worst_idx, 'avg_sentiment']
    
    pos_days = int((sentiment_per_day['category'] == 'Positive').sum())
    neu_days = int((sentiment_per_day['category'] == 'Neutral').sum())
    neg_days = int((sentiment_per_day['category'] == 'Negative').sum())
    total_days = len(sentiment_per_day)
    
    sent_stats = {
        'avg_score': round(avg_score, 4),
        'best_day': best_day,
        'best_score': round(best_score, 4),
        'worst_day': worst_day,
        'worst_score': round(worst_score, 4),
        'pos_days': pos_days,
        'neu_days': neu_days,
        'neg_days': neg_days,
        'total_days': total_days,
        'pos_pct': round(pos_days / total_days * 100, 1),
        'neu_pct': round(neu_days / total_days * 100, 1),
        'neg_pct': round(neg_days / total_days * 100, 1),
    }
    
    sentiment_data = {
        'line_chart': chart_data['sentiment_chart'],
        'pie_chart': pie_json,
        'hist_chart': hist_json,
        'stats': sent_stats
    }
    
    return render_template('sentiment.html', sentiment_data=sentiment_data, active_page='sentiment')

@app.route('/engagement')
def engagement():
    chart_data = generate_charts()
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    engagement_per_day = pd.read_csv(os.path.join(base_dir, 'engagement_per_day.csv'))
    top_hashtags = pd.read_csv(os.path.join(base_dir, 'top_hashtags.csv'))
    
    # Engagement stacked bar chart
    fig_bar = px.bar(engagement_per_day, x=engagement_per_day.columns[0], y=engagement_per_day.columns[1:],
                     title='Daily Engagement Breakdown',
                     barmode='stack',
                     template='plotly_white',
                     color_discrete_sequence=['#58a6ff', '#8957e5', '#3fb950', '#d29922'])
    fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                          font_color='#c9d1d9', margin=dict(t=40, b=0, l=0, r=0),
                          xaxis=dict(gridcolor='#30363d'), yaxis=dict(gridcolor='#30363d'))
    bar_json = json.dumps(fig_bar, cls=plotly.utils.PlotlyJSONEncoder)
    
    # Horizontal bar chart for top hashtags using go.Bar for explicit control
    top_hashtags['count'] = top_hashtags['count'].astype(int)
    th_sorted = top_hashtags.sort_values('count', ascending=True)
    fig_hash = go.Figure(go.Bar(
        x=th_sorted['count'].tolist(),
        y=th_sorted['hashtag'].tolist(),
        orientation='h',
        marker=dict(
            color=th_sorted['count'].tolist(),
            colorscale=[[0, '#30363d'], [0.5, '#58a6ff'], [1, '#8957e5']]
        ),
        text=th_sorted['count'].tolist(),
        textposition='outside',
        textfont=dict(color='#8b949e', size=11)
    ))
    max_count = th_sorted['count'].max()
    fig_hash.update_layout(
        title='Most Engaging Hashtags',
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font_color='#c9d1d9', margin=dict(t=40, b=0, l=0, r=60),
        height=500,
        yaxis=dict(gridcolor='#30363d', dtick=1),
        xaxis=dict(gridcolor='#30363d', range=[0, max_count * 1.15], type='linear'),
        showlegend=False
    )
    hash_json = json.dumps(fig_hash, cls=plotly.utils.PlotlyJSONEncoder)
    
    # Compute insight stats
    total_likes = int(engagement_per_day['likeCount'].sum())
    total_retweets = int(engagement_per_day['retweetCount'].sum())
    total_replies = int(engagement_per_day['replyCount'].sum())
    avg_daily_likes = int(engagement_per_day['likeCount'].mean())
    
    # Peak engagement day
    engagement_per_day['total_eng'] = engagement_per_day[['likeCount', 'replyCount', 'retweetCount']].sum(axis=1)
    peak_idx = engagement_per_day['total_eng'].idxmax()
    peak_day = engagement_per_day.loc[peak_idx, 'day']
    peak_value = int(engagement_per_day.loc[peak_idx, 'total_eng'])
    
    # Top hashtag
    top_tag = top_hashtags.iloc[0]['hashtag'] if not top_hashtags.empty else 'N/A'
    top_tag_count = int(top_hashtags.iloc[0]['count']) if not top_hashtags.empty else 0
    
    eng_stats = {
        'total_likes': total_likes,
        'total_retweets': total_retweets,
        'total_replies': total_replies,
        'avg_daily_likes': avg_daily_likes,
        'peak_day': peak_day,
        'peak_value': peak_value,
        'top_hashtag': top_tag,
        'top_hashtag_count': top_tag_count
    }
    
    engagement_data = {
        'line_chart': chart_data['engagement_chart'],
        'bar_chart': bar_json,
        'hashtag_chart': hash_json,
        'stats': eng_stats
    }
    
    return render_template('engagement.html', engagement_data=engagement_data, active_page='engagement')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
