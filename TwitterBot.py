# Scans through tweets to find and enter competitions

from __future__ import print_function
import tweepy, time, logging, inspect
logging.basicConfig(level=logging.INFO)

# Robbie Barrat https://github.com/robbiebarrat/twitter-contest-enterer

#enter the corresponding information from your Twitter application:

CONSUMER_KEY = 'shpSVvF0zvzUNuBmRCAI2VRtI' #keep the quotes, enter your consumer key
CONSUMER_SECRET = '7WYCHOPR0RpXW4MSYb67f7gMWB7knCyfVGEMSW9B3wttQQlQTv'#keep the quotes, enter your consumer secret key
ACCESS_KEY = '1313166944099422208-8iv7tVnAvUN1DPD5oIjX1lJ0xBQDAL'#keep the quotes, enter your access token
ACCESS_SECRET =  'cPBRvdoQueGzxlwP4pv627hEElPpupqNdP8vhlWAgmLnn'#keep the quotes, enter your access token secret

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
keywords = ["rt to", "rt and win", "retweet and win", "rt for", "rt 4", "retweet to"]

bannedwords = ["vote", "bot", "b0t"]

bannedusers = ['bot', 'spot', 'followandrt2win'] # does not need to be the entire username! you can just put 'bot' for names like 'b0tspotter', etc.

def is_user_bot_hunter(username):
	clean_username = username.replace("0", "o")
	clean_username = clean_username.lower()
	for i in bannedusers:
		if i in clean_username:
			return True
		else:
			return False

def search(twts):
	for i in twts:
		if not any(k in i.text.lower() for k in keywords) or any(k in i.text.lower() for k in bannedwords):
			continue
		if is_user_bot_hunter(str(i.author.screen_name)) == False:
			if not i.retweeted:
				try:
					api.retweet(i.id)
					print("rt " + (i.text))
					
					# huge thanks to github user andrewkerr5 for providing the fix for hashtags
					if "follow" in i.text or "#follow" in i.text or "Follow" in i.text or "#Follow" in i.text or "FOLLOW" in i.text or "#FOLLOW" in i.text or "following" in i.text or "#following" in i.text or "FOLLOWING" in i.text or "#FOLLOWING" or "Following" in i.text or "#Following" in i.text:
						user_id = i.retweeted_status.user.id
						api.create_friendship(user_id)

				except Exception:
					pass
				
			if ("fav" in i.text or "Fav" in i.text or "FAV" in i.text) and not i.favorited:
				try:
					api.create_favorite(i.id)
					print("fav " + (i.text))
				except Exception:
					pass
			



def run():
	for key in ["RT to win", "retweet to win"]:
		print("\nSearching again\n")
		search(api.search(q=key))


if __name__ == '__main__':
	while True:
		run()