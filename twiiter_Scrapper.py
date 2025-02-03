import streamlit as st
import pandas as pd
import tweepy

# Twitter API credentials (replace with your own)
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAGIhygEAAAAANbZ2aFCiwQSk0YkjEN412MPgtac%3D6wNUoq3ofcDuRCvzzVv4JwSUqGxFlSYtzFLZ2VmePoGeQipgkC"

# Function for Twitter API scraper
def scrape_twitter_api(keyword, max_tweets=10):
    # Authenticate with the Twitter API
    client = tweepy.Client(bearer_token=BEARER_TOKEN)

    # Search for tweets
    query = f"{keyword} -is:retweet"  # Exclude retweets
    tweets = client.search_recent_tweets(query=query, max_results=max_tweets, tweet_fields=["created_at", "author_id"])

    # Extract tweet data
    tweets_data = []
    for tweet in tweets.data:
        tweets_data.append({
            "tweet_id": tweet.id,
            "text": tweet.text,
            "created_at": tweet.created_at,
            "author_id": tweet.author_id,
        })

    return pd.DataFrame(tweets_data)

# Streamlit app
def main():
    st.title("Twitter Scraper 🐦")
    st.write("Enter a keyword to scrape tweets.")

    # Input fields
    keyword = st.text_input("Enter a keyword:", "web scraping")
    max_tweets = st.number_input("Number of tweets to scrape:", min_value=1, max_value=100, value=10)

    # Scrape button
    if st.button("Scrape Tweets"):
        st.write(f"Scraping tweets for '{keyword}'...")
        
        df = scrape_twitter_api(keyword, max_tweets=max_tweets)

        # Display results
        st.write(f"Found {len(df)} tweets:")
        st.dataframe(df)

        # Download button
        st.download_button(
            label="Download as CSV",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="tweets.csv",
            mime="text/csv",
        )

# Run the app
if __name__ == "__main__":
    main()