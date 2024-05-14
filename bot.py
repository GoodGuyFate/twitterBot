import tweepy
import json
import mysql.connector




def load_config():
    """Loads configuration data from the JSON file."""
    try:
        with open("config.json") as config_file:
            config = json.load(config_file)
            return config
    except FileNotFoundError:
        print("Error: config.json file not found!")
        exit()


config = load_config()

twitter_config = config["twitter"]
database_config = config["database"]

# Load configuration
config = load_config()

# Connect to MySQL database (replace credentials with your own)
mydb = mysql.connector.connect(
    host=database_config["host"],
    user=database_config["user"],
    password=database_config["password"],
    database=database_config["database_name"],
)

mycursor = mydb.cursor()


def get_random_non_retweeted_fact(mycursor):
    """Retrieves a single random non-retweeted fact from the database.

    Returns:
        tuple: A tuple containing the fact's ID (index 0) and text (index 1),
            or None if no non-retweeted facts are found.
    """

    mycursor.execute(
        "SELECT * FROM facts WHERE tweeted = FALSE ORDER BY RAND() LIMIT 1"
    )
    # Fetch one random row from the result
    random_fact = mycursor.fetchone()
    return random_fact


def tweet_random_fact(mycursor, api):
    """Gets a random non-retweeted fact and tweets it.

    Args:
        mycursor: The MySQL database cursor object.
        api: The authenticated Tweepy API object.
    """

    random_fact = get_random_non_retweeted_fact(mycursor)

    if random_fact is not None:
        # Extract the fact ID and text from the random_fact tuple
        fact_id, fact_text, fact_category, fact_bool = random_fact

        # Update the tweeted flag for the chosen fact
        mycursor.execute("UPDATE facts SET tweeted = TRUE WHERE id = %s", (fact_id,))
        mydb.commit()

        tweet_text = f"{fact_text} #history"
        # Tweet the fact
        client.create_tweet(text=tweet_text)
        print(f"Tweeted: {fact_text}")
    else:
        print("No more non-retweeted facts found.")


client = tweepy.Client(
    twitter_config["bearer_token"],
    twitter_config["api_key"],
    twitter_config["api_secret_key"],
    twitter_config["access_token"],
    twitter_config["access_token_secret"],
)


def main():
    """Prompts user to confirm tweet and calls tweet_random_fact."""

    valid_inputs = ["y", "n"]

    while True:
        # Prompt user for confirmation
        send_tweet = input("Would you like to send a tweet today? (y/n): ").lower()

        if send_tweet in valid_inputs:
            if send_tweet == "y":
                auth = tweepy.OAuth1UserHandler(
                    twitter_config["api_key"],
                    twitter_config["api_secret_key"],
                    twitter_config["access_token"],
                    twitter_config["access_token_secret"],
                )
                api = tweepy.API(auth, wait_on_rate_limit=True)
                tweet_random_fact(mycursor, api)
            else:
                print("No tweet sent.")
            break  # Exit the loop if valid input is received
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

    # Close the database connection
    mydb.close()

if __name__ == '__main__':
    main()
