import prawcore
import time
from settings import *

pubsub = redis_db.pubsub()


class Subscriber ():

    def __init__(self):
        pass


    def check_topic(self, topic):
        """
        Verification of topic name correctness in Reddit structure.
        :param topic: channel name
        :return: True if correct, False otherwise
        """
        self.topic = topic
        topic = str(topic.lower())
        try:
            for submission in reddit.subreddit(topic).top(limit=1):
                if submission:
                    return True
        except prawcore.exceptions.NotFound:
            return False
        except prawcore.exceptions.Redirect:
            return False
        except prawcore.exceptions.Forbidden:
            return False


    def subscribe(self, topic):
        """
        Subscription to given channel
        :param topic: channel topic
        :return: void
        """
        self.topic = topic
        topic = str(topic.lower())
        existense = self.check_topic(topic)
        if existense:
            pubsub.subscribe(topic)
        else:
            print(str_notfound)
            main()


    def get_top_news(self, channel):
        self.channel = channel
        channel = str(channel.lower())
        print(str_subscription % channel.upper())
        try:
            for submission in reddit.subreddit(channel).top(limit=5):
                print(str_fullpost % (submission.title, submission.url))
        except prawcore.exceptions.Redirect:
            return None
        except prawcore.exceptions.NotFound:
            return None


def main():
    _topic = input(str_input)
    client = Subscriber()
    client.subscribe(_topic)
    client.get_top_news(_topic)

    while True:
        message = pubsub.get_message()
        if message and message['type'] == 'message':
            message_text = (message['data']).decode('utf-8')
            print(str_new_post % (_topic.upper(), message_text))
        time.sleep(1)


if __name__ == '__main__':
    main()