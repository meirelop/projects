**Author - Rakhmetzhanov Meirkhan**


**General info** 
Implemented subscription to "Reddit" website with given topic name.
Topic name will be given within ineraction with user.
After subscription, user will receive TOP-5 posts in Reddit in given topic. 

Then, Server scans new posts every second to according topic in Reddit and forwards to pubsub channel. 
While doing inserts unique ID of latest post to redis container, for future verifications.
Scanner stops, if post with such ID already published to particular channel. (Key - channel name, Value - latest post ID)
Also, implemented archiving. All incoming posts will store at DB for one day.

**HOW TO RUN**
Required: Python 3
- Run REDDIT_CLIENT.PY and write any interesting topic for you
- Run REDDIT_SERVER.PY

To simulate multiple client subscription, run multiple reddit_server.py module.
Suggestions: subscribe to channel "all", Reddit's most frequently updated channel, if you dont want to wait new post.


**Module info**
# settings.py
- Default values and settings, API tokens. No functionality.

# reddit_server.py 
- Pubsub server. In charge of getting news from Reddit
main():         Scans for new posts every sec. 
get_channels(): Select all existing channel names.
get_news():     Scanner of new posts, with respect to post freshness. Returns only fresh news. 
publish_to_channel: Publish to channel in redis

# reddit_client.py 
- Pubsub client. User interaction and subscription to topics.

main():         Listens new publishments and checks redis every sec.
check_topic():  Verification of topic name correctness in Reddit structure.
subscribe():    Subscription to given channel


**Clone a repository**
git clone https://rakhmetzhanov@bitbucket.org/rakhmetzhanov/architecture.git