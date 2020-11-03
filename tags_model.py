from __future__ import annotations
from typing import Dict, List, Tuple, Type


class TagCategoryBaseItem:
    name: str
    category: TagCategoryBase

    def __init__(self, properties: Tuple[str, TagCategoryBase])-> None:
        self.name, self.category = properties


class TagItem(TagCategoryBaseItem):
    _included: bool

    def __init__(self, properties: Tuple[str, TagCategoryBase])-> None:
        super().__init__(properties)
        self._included = False

    @property
    def included(self: TagItem) -> bool : 
        return self._included 

    @included.setter 
    def included(self: TagItem, value: bool)-> None: 
        self._included = value 



class TagCategoryBase(TagCategoryBaseItem):
    items: List[TagCategoryBaseItem]

    def __init__(self, properties: Tuple[str, TagCategoryBase])-> None:
        super().__init__(properties)
        self.items = list()


    def create_tag_item(self: TagCategoryBase, tag_name: str)-> TagCategoryBaseItem:
        return TagCategoryBaseItem((tag_name, self))


    def add_item(self: TagCategoryBase, tag_name: str)-> TagCategoryBaseItem:
        result = self.create_tag_item(tag_name)
        self.items.append(result)
        return result



class TagCategory(TagCategoryBase):

    def create_tag_item(self: TagCategory, tag_name: str):
        return TagItem((tag_name, self))

