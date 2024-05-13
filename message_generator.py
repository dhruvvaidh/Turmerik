import pandas as pd
import json
from openai import OpenAI
from load_dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()
client = OpenAI()

# Load the sentiment analysis results
with open('grouped_author_comments_by_subreddit_using_vader.json', 'r') as file:
    sentiment_data = json.load(file)

# Load subreddit descriptions from CSV
subreddit_descriptions = pd.read_csv('subreddits.csv')

# Convert the subreddit descriptions to a dictionary for easier lookup
subreddit_info = subreddit_descriptions.set_index('Name').to_dict()['Description']

def generate_message(subreddit, sentiment, subreddit_description):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content":  f"Create a personalized message for a Reddit user interested in {subreddit} which is about '{subreddit_description}'. They have a '{sentiment}' sentiment about participating in clinical trials. The message should encourage participation or provide informative feedback."},
        ],
        max_tokens=150,
        temperature=0.7
    )
    if response.choices[0].message.content is not None:
        # Extracting the text from the response
        message = response.choices[0].message.content.strip().lower()
    return message

# Dictionary to store messages by user and subreddit
messages = {}

# Generate and store messages
for user in tqdm(sentiment_data.keys(), desc="Processing users"):
    messages[user] = {}
    for subreddit, details in tqdm(sentiment_data[user].items(), desc=f"Processing subreddits for user {user}"):
        sentiment_label = details['sentiment_label']
        # Fetch the subreddit description from the dictionary
        subreddit_desc = subreddit_info.get(subreddit, "No description available")
        message = generate_message(subreddit, sentiment_label, subreddit_desc)
        messages[user][subreddit] = message

# Save the generated messages to a JSON file
with open('personalized_messages_vader.json', 'w') as outfile:
    json.dump(messages, outfile, indent=4)

print("Messages generated and saved successfully.")
