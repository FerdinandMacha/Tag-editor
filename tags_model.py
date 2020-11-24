from __future__ import annotations

from typing import List, Optional, Tuple


class TagCategoryBaseItem:
    name: str
    category: Optional[TagCategoryBase]

    def __init__(self, properties: Tuple[str, Optional[TagCategoryBase]])-> None:
        self.name, self.category = properties


class TagItem(TagCategoryBaseItem):
    _included: bool

    def __init__(self, properties: Tuple[str, Optional[TagCategoryBase]])-> None:
        super().__init__(properties)
        self._included = False

    @property
    def included(self) -> bool : 
        return self._included 

    @included.setter 
    def included(self, value: bool)-> None: 
        self._included = value 



class TagCategoryBase(TagCategoryBaseItem):
    items: List[TagCategoryBaseItem]

    def __init__(self, properties: Tuple[str, Optional[TagCategoryBase]])-> None:
        super().__init__(properties)
        self.items = list()


    def create_tag_item(self, tag_name: str)-> TagCategoryBaseItem:
        return TagCategoryBaseItem((tag_name, self))


    def add_item(self, tag_name: str)-> TagCategoryBaseItem:
        result = self.create_tag_item(tag_name)
        self.items.append(result)
        return result



class TagCategory(TagCategoryBase):

    def create_tag_item(self, tag_name: str):
        return TagItem((tag_name, self))

