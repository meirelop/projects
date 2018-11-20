import redis
import praw

REDDIT_CLIENT_ID = 'dkCva_Zwhpz4sQ'
REDDIT_TOKEN = 'pRJsvuI1NAvA3fl36trHVTmaHC0'
REDDIT_AGENT = 'user_agent'
str_notfound = 'Sorry, we could not find anything on your interest or access to topic restricted. Try again..'
str_input = 'Welcome to Reddit. Write your interest: '
str_subscription = 'You subscribed to %s news'
str_new_post = 'New post on %s: "%s"\n '
str_fullpost = '%s. Check out full post on %s\n'

redis_db = redis.StrictRedis(host='localhost', port=6379, db=1)
redis_db_archive = redis.StrictRedis(host='localhost', port=6379, db=2)
reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID,
                     client_secret=REDDIT_TOKEN,
                     user_agent=REDDIT_AGENT)
ttl = 86400
pubsub = redis_db.pubsub()

