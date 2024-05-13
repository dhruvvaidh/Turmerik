import pandas as pd
import json
from openai import OpenAI
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()
client = OpenAI()

# Load the dataset
file_path = 'clinical_trial_data.csv'
data = pd.read_csv(file_path)

# Group by Subreddit and Comment Author
grouped_data = data.groupby(['Subreddit', 'Comment Author'])

# Build a JSON structure including the subreddit name and comments
results = {}
for (subreddit, author), group in tqdm(grouped_data, desc="Grouping data"):
    author_data = results.setdefault(author, {})
    author_data[subreddit] = {
        'comments': group['Comment'].tolist()
    }

# Function to get sentiment scores using GPT-3.5-turbo
def get_sentiment(text):
    response = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Analyze the sentiment of this text in respective of clinical trials: '{text}'. Is it positive, negative, or neutral?"}
        ]
    )
    if response.choices[0].message.content is not None:
        sentiment_text = response.choices[0].message.content.strip().lower()
    return sentiment_text

# Apply sentiment analysis on 'Comment' for each author in each subreddit
for author, subreddits in tqdm(results.items(), desc="Applying sentiment analysis"):
    for subreddit, data in subreddits.items():
        sentiments = [get_sentiment(comment) for comment in tqdm(data['comments'], desc=f"Analyzing comments in {subreddit} for {author}")]
        data['Sentiment_label'] = max(sentiments, key=sentiments.count)

# Save the JSON results
with open('grouped_author_comments_by_subreddit_using_openai.json', 'w') as outfile:
    json.dump(results, outfile, indent=4)
