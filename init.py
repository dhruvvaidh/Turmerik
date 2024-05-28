from praw import Reddit
from requests import Session
from dotenv import load_dotenv

def start():
    session = Session()
    # Set your company SSL certificate path here to enable SSL verification
    session.verify = False # Disable SSL verification 
    reddit = Reddit(
        client_id="YhkXjhlaKvBFLHssk81Zkg",
        client_secret="FFLawg1SIc_TY7RzUk14_UWzNwjEDQ",
        password="password",
        requestor_kwargs={"session": session},  # pass the custom Session instance
        user_agent="TrialTune by u/deathstroke_139",
        username="deathstroke_139",
    )
    print("Reddit instance created successfully!")
    load_dotenv()
    print("OpenAI API key loaded successfully!")
    return reddit




