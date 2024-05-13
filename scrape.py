import init
import praw
import pandas as pd
from tqdm import tqdm
import spacy
import numpy as np

def get_relevant_subreddits():
    # Install using python -m spacy download en_core_web_lg in your terminal
    nlp = spacy.load('en_core_web_lg')

    reddit = init.start()

    # Specify the keywords you want to search for
    keywords = ['clinical trials', 'clinical trial demographics', 'clinical trial results']

    # Create an empty dictionary to store the subreddit names and descriptions
    subreddits = {}

    # Search for subreddits related to each keyword
    for keyword in keywords:
        for subreddit in tqdm(reddit.subreddits.search(keyword, limit=100), desc=f"Searching subreddits for keyword '{keyword}'"):
            subreddits[subreddit.display_name] = subreddit.public_description

    # Convert the dictionary to a list of tuples
    subreddit_name = list(subreddits.keys())
    subreddit_description = list(subreddits.values())

    # Create a DataFrame from the list of subreddits
    df = pd.DataFrame({'Name': subreddit_name, 'Description': subreddit_description})
    #df.to_csv('subreddits.csv', index=False)

    # Calculate the similarity between the description and the keywords
    df['Similarity'] = df['Description'].apply(lambda desc: nlp(desc).similarity(nlp(' '.join(keywords))))

    # Sort the DataFrame by the similarity in descending order
    df = df.sort_values('Similarity', ascending=False)

    df.to_csv('subreddits.csv', index=False)

    # Choose the names of top 10 subreddits
    #relevant_subreddits = df.head(10)['Name'].tolist()

    relevant_subreddits = df[df['Similarity'] > 0.65]['Name'].tolist()
    return relevant_subreddits
    #print(relevant_subreddits)
    

# Scrape posts and comments from each subreddit
def scrape_posts(reddit, subreddit_name):
    # Create an empty list to store the data
    data = []
    subreddit = reddit.subreddit(subreddit_name)
    
    # Scrape posts
    for post in tqdm(subreddit.new(limit=300), desc=f"Scraping posts from subreddit '{subreddit_name}'"):  # Change the limit as per your requirement
        # Scrape comments
        post.comments.replace_more(limit=None)
        for comment in post.comments.list():
            # Append the data to the list
            data.append({"Subreddit": subreddit_name, "Post Title": post.title, "Post URL": post.url, "Post Score": post.score, "Post Comments": post.num_comments, "Comment": comment.body, "Comment Author": comment.author})

    # Convert the list into a DataFrame
    reddit_df = pd.DataFrame(data)
    return reddit_df

#reddit_df.to_csv('reddit_data.csv', index=False)
# Print the DataFrame
#print(df)