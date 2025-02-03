import streamlit as st
import pandas as pd
# from playwright.sync_api import sync_playwright
import tweepy
import time

# Twitter API credentials (replace with your own)
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAGIhygEAAAAANbZ2aFCiwQSk0YkjEN412MPgtac%3D6wNUoq3ofcDuRCvzzVv4JwSUqGxFlSYtzFLZ2VmePoGeQipgkC"

# # Function for Playwright scraper
# def scrape_twitter_playwright(keyword, max_tweets=10, browser_type="chromium"):
#     tweets = []

#     with sync_playwright() as p:
#         # Launch the selected browser
#         if browser_type == "chromium":
#             browser = p.chromium.launch(headless=True)  # Run in headless mode
#         elif browser_type == "firefox":
#             browser = p.firefox.launch(headless=True)
#         elif browser_type == "webkit":
#             browser = p.webkit.launch(headless=True)
#         else:
#             raise ValueError("Unsupported browser type. Choose 'chromium', 'firefox', or 'webkit'.")

#         page = browser.new_page()

#         # Navigate to Twitter search results
#         page.goto(f"https://twitter.com/search?q={keyword}&src=typed_query")

#         # Wait for tweets to load
#         page.wait_for_selector('article[role="article"]')

#         # Scroll and load more tweets
#         tweets_loaded = 0
#         while tweets_loaded < max_tweets:
#             # Extract tweet data
#             tweet_elements = page.query_selector_all('article[role="article"]')
#             for tweet in tweet_elements[tweets_loaded:]:
#                 content = tweet.inner_text()
#                 tweets.append({"content": content})
#                 tweets_loaded += 1
#                 if tweets_loaded >= max_tweets:
#                     break

#             # Scroll down to load more tweets
#             page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
#             time.sleep(2)  # Wait for new tweets to load

#             # Check if no more tweets are loading
#             new_tweet_elements = page.query_selector_all('article[role="article"]')
#             if len(new_tweet_elements) == len(tweet_elements):
#                 st.warning("No more tweets found.")
#                 break

#         # Close the browser
#         browser.close()

#     return pd.DataFrame(tweets)

#Function for Twitter API scraper
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
    scraper_type = st.radio("Choose a scraper type:", ("Twitter API")), #"Playwright",

    if scraper_type == "Playwright":
        browser_type = st.selectbox("Select browser:", ("chromium", "firefox", "webkit"))
    else:
        browser_type = None

    # Scrape button
    if st.button("Scrape Tweets"):
        st.write(f"Scraping tweets for '{keyword}'...")

        if scraper_type == "Playwright":
            df = scrape_twitter_playwright(keyword, max_tweets=max_tweets, browser_type=browser_type)
        else:
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