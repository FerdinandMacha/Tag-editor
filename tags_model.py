from typing import Dict, List, Tuple, Type
import logging

class TagCategoryBaseItem:
    name: str
    category: str

    def __init__(self: TagCategoryBaseItem, properties: Tuple[str, int]):
        self.name, self.category = properties


class TagItem(TagCategoryBaseItem):
    _included: bool

    def __init__(self: TagItem, properties: Tuple[str, str]):
        super().__init__(properties)
        self._included = False

    @property
    def included(self: TagItem) -> bool : 
        return self._included 

    @included.setter 
    def included(self: TagItem, value: bool)-> None: 
        self._included = value 



class TagCategoryBase(TagCategoryBaseItem):
    items: List[Type[TagCategoryBaseItem]]

    def __init__(self: TagCategoryBase, properties: Tuple[str, str]):
        super().__init__(properties)
        self.items = list()


    def create_tag_item(self: TagCategoryBase, tag_name: str)-> TagCategoryBaseItem:
        return TagCategoryBaseItem((tag_name, self))


    def add_item(self: TagCategoryBase, tag_name: str)-> Type[TagCategoryBaseItem]:
        result = self.create_tag_item(tag_name)
        self.items.append(result)
        return result



class TagCategory(TagCategoryBase):

    def create_tag_item(self, properties):
        return TagItem((properties, self))

