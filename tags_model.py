
class TagsModel:
    class TagModel:
        def __init__(self, tag_name):
            self.name = tag_name
            self.included = False
    
    def __init__(self, category_name):
        self.category = category_name
        self.tags = list()

    def add_tag_name(self, tag_name):
        result = TagsModel.TagModel(tag_name)
        self.tags.append(result)
        return result

