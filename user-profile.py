import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import re
import json

# Ensure required NLTK resources are downloaded
nltk.download('vader_lexicon')

# Load the dataset
file_path = 'clinical_trial_data.csv'
data = pd.read_csv(file_path)

# Function to clean and preprocess text
def clean_text(text):
    # Remove URLs
    text = re.sub(r'http\S+', '', text)
    # Remove non-alphabetic characters
    text = re.sub(r'[^a-zA-Z\s]', '', text, re.MULTILINE)
    # Convert to lowercase
    text = text.lower().strip()
    return text

# Apply the cleaning function to the 'Comment' column
data['Comment'] = data['Comment'].apply(clean_text)

# Initialize the VADER sentiment intensity analyzer
sia = SentimentIntensityAnalyzer()

# Function to get sentiment scores
def get_sentiment(text):
    return sia.polarity_scores(text)['compound']

# Apply sentiment analysis on 'Comment'
data['Comment Sentiment'] = data['Comment'].apply(get_sentiment)

# Function to label sentiment based on the average score
def label_sentiment(score):
    if score > 0.75:
        return 'highly positive'
    elif score > 0.25:
        return 'moderately positive'
    elif score > -0.25:
        return 'neutral'
    elif score > -0.75:
        return 'moderately negative'
    else:
        return 'highly negative'

# Export ungrouped data to a CSV
data.to_csv('individual_comment_sentiments.csv', index=False)

# Group by Subreddit and Comment Author
grouped_data = data.groupby(['Subreddit', 'Comment Author'])

# Build a JSON structure including the subreddit name and comments
results = {}
for (subreddit, author), group in grouped_data:
    author_data = results.setdefault(author, {})
    author_data[subreddit] = {
        'average_sentiment': group['Comment Sentiment'].mean(),
        'sentiment_label': label_sentiment(group['Comment Sentiment'].mean()),
        'comments': group['Comment'].tolist()
    }

# Save the JSON results
with open('grouped_author_comments_by_subreddit_using_vader.json', 'w') as outfile:
    json.dump(results, outfile, indent=4)