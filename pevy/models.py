class Item:
    def __init__(self, id, text, image=None):
        self.id = id
        self.text = text
        self.image = image

    def __str__(self):
        return 'Item(id={}, text={}, image={}'.format(self.id, self.text,
                'yes' if self.image else 'no')
