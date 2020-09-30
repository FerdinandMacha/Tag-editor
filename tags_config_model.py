
class TagCategory:
    def __init__(self, category_name):
        self.category = category_name
        self.tags = list() # list of strings representing tag names

    def add_tag_name(self, tag_name):
        self.tags.append(tag_name)

