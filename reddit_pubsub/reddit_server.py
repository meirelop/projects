import time
import prawcore
from settings import *

pubsub = redis_db.pubsub()

class Server():
    def __init__(self):
        pass

    def get_channels(self):
        """
        Select all existing channel names.
        """
        all_channels = (redis_db.pubsub_channels())
        all_channels = [i.decode('utf-8') for i in all_channels]
        # print('all_channels: %s' % all_channels)
        return all_channels


    def get_news(self, channel):
        """
        Scanner of new posts, with respect to post freshness. Returns only fresh news.
        :param channel: channel name
        :return: new post text if exists, None otherwise
        """
        self.channel = channel
        channel = str(channel.lower())
        try:
            for submission in reddit.subreddit(channel).new(limit=1):
                new_post_id = str(submission.id)
                last_post_id = redis_db.get(channel)
                if last_post_id:
                    last_post_id = last_post_id.decode('utf-8')
                if new_post_id == last_post_id:
                    return None
                redis_db.set(channel, new_post_id)
                # redis_db_archive.set(channel + new_post_id, )
                post_key = channel + '|' + new_post_id
                post_value = submission.title + submission.url
                redis_db_archive.set(post_key, post_value, ttl)
                result = (str_fullpost % (submission.title, submission.url))
                return result
        except prawcore.exceptions.Redirect:
            return None
        except prawcore.exceptions.NotFound:
            return None


    def publish_to_channel(self, channel, msg):
        """
        Publish to channel in redis
        :param channel: channel name
        :param msg: post body
        """
        self.channel = channel
        redis_db.publish(channel, msg)
        subscriber_count = redis_db.execute_command('PUBSUB', 'NUMSUB', channel)
        print('Published new post to channel "%s". Subscribers: %s' % (channel, subscriber_count[1]))


def main():
    while True:
        pubsub_server = Server()
        all_channels = pubsub_server.get_channels()
        for channel_name in all_channels:
            new_post = pubsub_server.get_news(channel_name)
            if new_post:
                pubsub_server.publish_to_channel(channel_name, new_post)
        time.sleep(1)


if __name__ == '__main__':
    main()





