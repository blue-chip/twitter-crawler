import os
import time
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import yaml


class Listener(StreamListener):
    def __init__(self, path=None):
        self.path = path

    def on_data(self, data):
        tweet = data.split(',"text":"')[1].split('","source":"')[0]
        print(time.strftime("%Y%m%d_%H%M%S"), tweet)

        # Open, Write then Close the file
        savefile = open(self.path, 'a')
        savefile.write(data)
        savefile.close()


config = yaml.safe_load(open("./config.yaml"))

consumerkey = config["twitter"]["consumerkey"]
consumersecret = config["twitter"]["consumersecret"]
accesstoken = config["twitter"]["accesstoken"]
accesstokensecret = config["twitter"]["accesstokensecret"]

authorization = OAuthHandler(consumerkey, consumersecret)
authorization.set_access_token(accesstoken, accesstokensecret)

filename = config["filename"]

script_dir = os.path.dirname(__file__)
rel_path = filename + ".json"
file_path = os.path.join(script_dir, rel_path)

twitterStream = Stream(
    authorization,
    Listener(
        path=file_path,
    )
)

twitterStream.filter(
    locations=[
        config["bounding-box"]["lower-left"]["lon"],
        config["bounding-box"]["lower-left"]["lat"],
        config["bounding-box"]["upper-right"]["lon"],
        config["bounding-box"]["upper-right"]["lat"]
    ]
)
