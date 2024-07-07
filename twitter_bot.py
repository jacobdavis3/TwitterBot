import tweepy
import random
import os

# Authenticate to X (Twitter)
def x_authentication():
    return tweepy.Client(bearer_token=os.environ['BEARER_TOKEN'],
                       consumer_key=os.environ['API_KEY'],
                       consumer_secret=os.environ['API_KEY_SECRET'],
                       access_token=os.environ['ACCESS_TOKEN'],
                       access_token_secret=os.environ['ACCESS_TOKEN_SECRET'])


# Function to convert text to bold unicode
def bold_text(text):
    bold_dict = {
        'A': '𝐀', 'B': '𝐁', 'C': '𝐂', 'D': '𝐃', 'E': '𝐄', 'F': '𝐅', 'G': '𝐆',
        'H': '𝐇', 'I': '𝐈', 'J': '𝐉', 'K': '𝐊', 'L': '𝐋', 'M': '𝐌', 'N': '𝐍',
        'O': '𝐎', 'P': '𝐏', 'Q': '𝐐', 'R': '𝐑', 'S': '𝐒', 'T': '𝐓', 'U': '𝐔',
        'V': '𝐕', 'W': '𝐖', 'X': '𝐗', 'Y': '𝐘', 'Z': '𝐙',
        'a': '𝐚', 'b': '𝐛', 'c': '𝐜', 'd': '𝐝', 'e': '𝐞', 'f': '𝐟', 'g': '𝐠',
        'h': '𝐡', 'i': '𝐢', 'j': '𝐣', 'k': '𝐤', 'l': '𝐥', 'm': '𝐦', 'n': '𝐧',
        'o': '𝐨', 'p': '𝐩', 'q': '𝐪', 'r': '𝐫', 's': '𝐬', 't': '𝐭', 'u': '𝐮',
        'v': '𝐯', 'w': '𝐰', 'x': '𝐱', 'y': '𝐲', 'z': '𝐳',
        '0': '𝟎', '1': '𝟏', '2': '𝟐', '3': '𝟑', '4': '𝟒', '5': '𝟓', '6': '𝟔',
        '7': '𝟕', '8': '𝟖', '9': '𝟗'
    }
    return ''.join(bold_dict.get(char, char) for char in text)


def tweet_creation():
    # Read quotes from file
    with open('quotes1.txt', 'r') as file:
        quotes = file.readlines()

    # Format the quote properly
    raw_quote = random.choice(quotes).strip()
    quote, author_raw = raw_quote.split('―') # Note '―' is NOT the hyphen key ('-')

    # Case where there is the author's name and work title
    if ',' in author_raw:
        author, title = author_raw.split(',', maxsplit=1)
        author_bold, title_bold = bold_text(author), bold_text(title)
        return f"{quote}\n― {author_bold}, {title_bold}"
    
    author_bold = bold_text(author_raw)
    return f"{quote}\n― {author_bold}"

def add_hashtag_to_tweet(tweet):
    hashtags = [
    "#Motivation", "#Inspiration", "#Quotes", "#Life", "#Wisdom",
    "#Success", "#Happiness", "#Love", "#Mindset", "#Goals",
    "#PositiveVibes", "#SelfCare", "#SelfLove", "#Leadership",
    "#Growth", "#Believe", "#DreamBig", "#PositiveThinking",
    "#Focus", "#NeverGiveUp", "#Determination", "#Courage",
    "#Strength", "#Mindfulness", "#Gratitude", "#MotivationalQuotes",
    "#InspirationalQuotes", "#DailyInspiration", "#DailyMotivation",
    "#QuoteOfTheDay", "#Quote", "#SuccessQuotes",
    "#LifeLessons", "#Inspire", "#Motivate", "#Achieve", "#Hustle",
    "#Perseverance", "#Ambition", "#Dedication", "#MindsetMatters", 
    "#BookLovers", "#ArtDaily", "#Euro2024", "#Wimbledon", "#CopaAmerica",
    "#Freedom", "#NBA", "#FreeAgency",
]

    # Calculate remaining characters for hashtags
    max_length = 280 - (len(tweet.encode('utf-16-le')) // 2) - 1  # 1 space for separation
    available_hashtags = [h for h in hashtags if len(h) <= max_length]
    
    if available_hashtags:
        random.shuffle(available_hashtags)
        selected_hashtags = []
        total_length = (len(tweet.encode('utf-16-le')) // 2) + 1
        
        for hashtag in available_hashtags:
            if total_length + len(hashtag) + 1 <= 280:
                selected_hashtags.append(hashtag)
                total_length += len(hashtag) + 1
        
        hashtags_str = " ".join(selected_hashtags)
        return f"{tweet}\n\n{hashtags_str}"
    
    return f"{tweet}"


def post_tweet(api, tweet):
    try:
        api.create_tweet(text=tweet)
        print(f"Tweeted: {tweet}")
    except tweepy.TweepyException as e:
        print(f"Error: {e}")


def main():
    api = x_authentication()
    tweet = tweet_creation()
    tweet_with_hashtags = add_hashtag_to_tweet(tweet)

    # Ensure the final tweet length is within the limit
    if len(tweet_with_hashtags) > 280:
        tweet_with_hashtags = tweet_with_hashtags[:279]  # Truncate if necessary
    post_tweet(api, tweet_with_hashtags)


if __name__ == '__main__':
    main()
