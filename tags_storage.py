from typing import Dict, Union, cast
import logging

from tags_model import TagCategoryBaseItem, TagItem, TagCategoryBase, TagCategory


tag_configuration: list[TagCategoryBase] = list()


def load_tag_configuration(config_file_name: str)-> None:
    with open(config_file_name, mode='r', encoding='utf-8-sig') as f:
        is_heading: bool = True
        current_heading_index: int = -1

        for line in f:
            tag_line: str = line.strip()
            if not tag_line:
                is_heading = True

                # An empty line is marking the category end.
                # The next line is the other category beginning.
                continue

            if is_heading:
                tag_configuration.append(TagCategoryBase((tag_line, None)))
                current_heading_index += 1
                is_heading = False
            else :
                tag_configuration[current_heading_index].add_item(tag_line)

    log_tags('Loaded configuration:', tag_configuration)


def load_tags(tags_file_name: str)-> list[TagCategory]:
    def load_current_tags()-> Dict[str, bool]:
        with open(tags_file_name, mode='r', encoding='utf-8-sig') as f:
            # Skip <!DOCTYPE html> header line
            next(f)
            
            # strip '<div>' from left and '</div>\n' from right for the tag name
            result = {get_tag_key(line[5:-7]): True for line in f}
        return result

    def get_tag_key(tag_name: str)-> str:
        return tag_name.upper()

    def load_current_tag(tag_config: TagCategoryBase, loaded_tags: list[TagCategory], 
        included_predicate: callable[[TagItem], bool])-> TagCategory:
        result: TagCategory = TagCategory((tag_config.name, None))
        loaded_tags.append(result)
        for tag in tag_config.items:
            current_tag: TagItem = cast(TagItem, result.add_item(tag.name))
            current_tag.included = included_predicate(tag)

    current_tags: Dict[str, bool] = load_current_tags()
    result: list[TagCategory] = list()
    for tag_category in tag_configuration:
        load_current_tag(tag_category, current_tags, 
            lambda t: True if current_tags.pop(get_tag_key(t.name), False) else False)

        """ category_tags: TagCategory = TagCategory((tag_category.name, None))
        result.append(category_tags)
        for tag in tag_category.items:
            current_tag: TagItem = cast(TagItem, category_tags.add_item(tag.name))
            current_tag.included = True if current_tags.pop(get_tag_key(tag.name), False) else False """

    if len(current_tags):
        additional: TagCategory = TagCategory(('Additional tags', None))
        for tag_name in current_tags:
            current_tag: TagItem = cast(TagItem, additional.add_item(tag_name))
            current_tag.included = True


    log_tags('Loaded file tags:', result)
    return result
                

def save_tags(tags_file_name: str, tag_categories: list[str])-> None:
    with open(tags_file_name, mode='w', encoding='utf-8-sig') as f:
        f.write('<!DOCTYPE html>\n')
        for tag in tag_categories:
            _ = f.write(f'<div>{tag}</div>\n')



def log_tags(list_description: str, tag_list: Union[list[TagCategoryBase], list[TagCategory]])-> None:
    logging.debug(list_description)
    for category in tag_list:
        [ logging.debug(f'{category.name} : {tag.__dict__}') for tag in category.items ]


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
