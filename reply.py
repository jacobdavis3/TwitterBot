import twitter_bot
import random
import tweepy
import keys
import os

def post_reply(api, reply):
    try:
        api.create_tweet(text=reply, in_reply_to_tweet_id='1812360607397773591')
        print(f"Tweeted: {reply}")
    except tweepy.TweepyException as e:
        print(f"Error: {e}")



def main():
    api = tweepy.Client(bearer_token=keys.Bearer_Token,
                       consumer_key=keys.API_Key,
                       consumer_secret=keys.API_Key_Secret,
                       access_token=keys.Access_Token,
                       access_token_secret=keys.Access_Token_Secret)
    reply = twitter_bot.tweet_creation()
    post_reply(api, reply)




if __name__ == '__main__':
    main()