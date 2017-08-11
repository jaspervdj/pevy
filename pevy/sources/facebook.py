import facebook
import requests

import pevy.models

class Facebook:
    def __init__(self, logger, config):
        self.logger = logger
        self.graph = facebook.GraphAPI(
                access_token=config['access_token'], version='2.7')
        self.group_id = config['group_id']

    def poll(self):
        path = self.group_id + '/feed'
        feed = self.graph.get_object(path)
        for story in feed['data']:
            message = self.graph.get_object(story['id'],
                    fields='from,message,picture')

            if 'message' in message:

                id = 'facebook/' + str(message['id'])
                author = message['from']['name']
                text = message['message']
                image = None

                if 'picture' in message:
                    image = requests.get(message['picture']).content

                yield pevy.models.Item(
                        id=id, author=author, text=text, image=image)