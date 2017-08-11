import twitter
import requests

import pevy.models

class Twitter:
    def __init__(self, logger, config):
        self.api = twitter.Api(
                consumer_key=config['consumer_key'],
                consumer_secret=config['consumer_secret'],
                access_token_key=config['access_token_key'],
                access_token_secret=config['access_token_secret'])
        logger.info('Verifying twitter credentials...')
        result = self.api.VerifyCredentials()
        logger.info('Twitter verification ok, id = {}'.format(result.id))
        self.hashtag = config['hashtag']

    def poll(self):
        term = '#' + self.hashtag
        results = self.api.GetSearch(term=term, result_type='recent',
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
