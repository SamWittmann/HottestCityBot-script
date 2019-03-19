import yaml
import logging
import json
import requests
import meteocalc
from requests_oauthlib import OAuth1Session
from requests import ConnectionError
from datetime import datetime

# Setup logging
logger = logging.getLogger('HottestCityBot-script')
logger.setLevel(logging.INFO)

logger.info("Bot started running")

# API URLs
POST_TWEET_URL = "https://api.twitter.com/1.1/statuses/update.json"
REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"
REQUEST_URL = 'http://api.openweathermap.org/data/2.5/weather'

# YAML config property names
CLIENT_KEY = "client_key"
CLIENT_SECRET = "client_secret"
OWNER_KEY = "resource_owner_key"
OWNER_SECRET = "resource_owner_secret"
WEATHER_API_KEY = "open_weather_api_key"

# Set of required properties
REQUIRED_PROPERTIES = {CLIENT_KEY, CLIENT_SECRET, OWNER_KEY, OWNER_SECRET, WEATHER_API_KEY}


# File paths
CONFIG_FILENAME = 'config.yml'


with open(CONFIG_FILENAME, 'r') as config_yml:
    config = yaml.safe_load(open(CONFIG_FILENAME, 'r'))

if not [prop for prop, val in config.items() if (prop in REQUIRED_PROPERTIES) and val]:
    logger.error("Run failed: A required property is missing from config.yml.")
    exit(-1)


def main():
    try:
        location_temp_tup = find_hottest_city_and_temp()
        tweet = "Today, the hottest city in the U.S is %s with a temperature of %sF" % location_temp_tup
        post_text_tweet(tweet)
        logger.info("Succesfully posted tweet for " + str(datetime.today().date()))
        return
    except ConnectionError:
        logger.exception("Run failed: Could not establish a connection to an external API.")
        exit(-1)


def post_text_tweet(text):
    client_key = config.get(CLIENT_KEY)
    client_secret = config.get(CLIENT_SECRET)
    resource_owner_key = config.get(OWNER_KEY)
    resource_owner_secret = config.get(OWNER_SECRET)

    twitter_auth = OAuth1Session(client_key,
                                       client_secret=client_secret,
                                       resource_owner_key=resource_owner_key,
                                       resource_owner_secret=resource_owner_secret)

    twitter_auth.post(url=POST_TWEET_URL, data={"status": text})
    logger.info("Tweet posted!")


def find_hottest_city_and_temp():
    hottest = ('', 0)
    logger.info("Finding today's hottest city")
    with open('resources/top1000CitiesToIds.json') as f:
        city_and_state_to_id = json.load(f)
        for city_and_state in city_and_state_to_id.keys():
            temperature = query_temperature(city_and_state_to_id[city_and_state])

            if hottest[1] < temperature:
                hottest = (city_and_state, temperature)
    logger.info("Today's hottest city is: %s - %s F" % (str(hottest[0]), str(round(hottest[1], 2))))
    return hottest


def query_temperature(city_id):
    query_params = {'appid': config.get(WEATHER_API_KEY),
                    'units': 'imperial',
                    'id': city_id}
    response = requests.get(REQUEST_URL, params=query_params)
    if response.status_code == 200:
        weather_data = response.json()
        temperature = int(weather_data['main']['temp_max'])
        humidity = int(weather_data['main']['humidity'])
        return meteocalc.heat_index(temperature, humidity).f
    else:
        logger.debug("API request for location code %s failed.\nResponse code is %s.",
                          str(city_id), str(response.status_code))
        return -1000
