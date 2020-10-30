import logging

class TagCategoryBaseItem:
    def __init__(self, properties):
        self.name, self.category = properties


class TagItem(TagCategoryBaseItem):
    def __init__(self, properties):
        super().__init__(properties)
        self._included = False

    @property
    def included(self): 
        return self._included 

    @included.setter 
    def included(self, value): 
        self._included = value 



class TagCategoryBase(TagCategoryBaseItem):
    def __init__(self, properties):
        super().__init__(properties)
        self.items = list() # items of TagCategoryBaseItem


    def create_tag_item(self, tag_name):
        return TagCategoryBaseItem((tag_name, self))


    def add_item(self, tag_name):
        result = self.create_tag_item(tag_name)
        self.items.append(result)
        return result



class TagCategory(TagCategoryBase):

    def create_tag_item(self, properties):
        return TagItem((properties, self))

