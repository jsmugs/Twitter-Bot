import requests
import json
import tweepy
from apscheduler.schedulers.blocking import BlockingScheduler

alchemy_url = "https://eth-mainnet.g.alchemy.com/nft/v2/tbAnw_7jhfqSRckj30gJWDaGodVygOUH/getFloorPrice?contractAddress=0x5078981549A1CC18673eb76fb47468f546aAdc51"
etherscan = "https://api.etherscan.io/api?module=stats&action=ethprice&apikey=8F324IPAF5BT4TU7CGN8X8CFJS189UXZ3T"
headers = {"accept": "application/json"}

consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

def send_message(): 
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    #Alchemy API to get current floor price
    alchemy_response = requests.get(alchemy_url, headers=headers)
    floor_data = alchemy_response.json()
    nft_floor = floor_data['openSea']['floorPrice']
    currency = floor_data['openSea']['priceCurrency']
    collection_url= floor_data['openSea']['collectionUrl']

    final = str(nft_floor) + ' ' + currency

    #Etherscan API to lookup Ethereum price in USD
    etherscan_response = requests.get(etherscan, headers=headers)
    eth_data = etherscan_response.json()
    price = eth_data['result']['ethusd']
    USD = float(price) * float(nft_floor)

    new_floor = final + " ($" + "{:.2f}".format(USD) + ")"

    #send tweet
    tweet_text = "The feetpix current floor is " + new_floor + '\n' + "Send it to zero with haste!! 📉📉📉" + '\n' + "#feetpix #nfts #ethereum" + '\n' + "https://opensea.io/collection/feetpixwtf?search[sortAscending]=true&search[sortBy]=UNIT_PRICE&search[toggles][0]=BUY_NOW"
    api.update_status(tweet_text)

sched = BlockingScheduler(timezone='EST')

sched.add_job(send_message, 'cron', hour='0-23', minute='0')

sched.start()
