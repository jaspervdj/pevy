import twitter
import requests

import pevy.models

class Twitter:
    def __init__(self, logger, config):
        self.logger = logger
        self.consumer_key = config['consumer_key']
        self.consumer_secret = config['consumer_secret']
        self.access_token_key = config['access_token_key']
        self.access_token_secret = config['access_token_secret']
        self.hashtag = config['hashtag']

    def poll(self):
        api = twitter.Api(
                consumer_key=self.consumer_key,
                consumer_secret=self.consumer_secret,
                access_token_key=self.access_token_key,
                access_token_secret=self.access_token_secret)

        self.logger.info('Verifying twitter credentials...')
        credentials = api.VerifyCredentials()
        self.logger.info(
                'Twitter verification ok, id = {}'.format(credentials.id))

        term = '#' + self.hashtag
        results = api.GetSearch(term=term, result_type='recent',
                include_entities=True, count=100)
        for result in results:
            yield self.__tweet_to_item(result)

    def __tweet_to_item(self, tweet):
        id = 'twitter/' + str(tweet.id)
        author = tweet.user.screen_name
        text = tweet.text
        image = None

        if tweet.media:
            photos = [m for m in tweet.media if m.type == 'photo']
            if photos:
                photo = photos[0]
                image = requests.get(photo.media_url).content

        return pevy.models.Item(id=id, author=author, text=text, image=image)

    def __str__(self):
        return 'Twitter ({})'.format(self.hashtag)
