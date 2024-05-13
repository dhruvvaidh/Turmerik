# Turmerik
Internship Task for ML Intern at Turmerik

**Objective**: The objective of this project is to demonstrate your ability to ethically scrape and analyze web data, utilize sentiment analysis, and leverage AI to personalize communication. You will focus on identifying potential participants for a clinical trial by analyzing sentiments expressed on Reddit.

**Evironment Setup**: Install all packages using `requirements.txt` by running the command `pip install -r requirements.txt`. Then create a `.env` file and type `OPENAI_API_KEY=your_secret_key` to setup your OpenAI environment and perform Authentication via OAuth using the PRAW Documentation. After reading the documentation, enter the credentials to your reddit account and application details in the file `init.py`.
(Refer: https://praw.readthedocs.io/en/stable/getting_started/authentication.html).

**Data Collection**: Run the script `get_data.py` to scrape the data from Reddit using the PRAW API. This will generate a file called `clinical_data_csv` which contains the scraped data and a file called `subreddits.csv` which contains the names, description and similarity scores of the relevant subreddits.

**Sentiment Analysis and User Segmentation**: Run the script `user-profile.py` to perform sentiment analysis using vader OR Run the script `openai-user-profile.py` to perform sentiment analysis using Open AI's `chatgpt-3.5-turbo`. This creates a JSON structure with the sentiment labels, author usernames, the comments they wrote and the subreddit they wrote in.

**Message Generation**: Run the script `message_generation` to generate personalized messages for every user who commented on the subreddits to increase personalization in communication inorder to increase participation levels in clinical trials. The final output is in a JSON file called `personalized-messages-vader.json`.






