class Item:
    def __init__(self, id, author, text, image=None):
        self.id = id
        self.author = author
        self.text = text
        self.image = image

    def __str__(self):
        return 'Item(id={}, author={}, text={}, image={}'.format(self.id,
                self.author, self.text, 'yes' if self.image else 'no')
