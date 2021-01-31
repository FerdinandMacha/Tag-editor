import logging
from typing import Callable, Union

from tags_model import (TagCategory, TagCategoryBase, TagCategoryBaseItem, TagItem)

tag_configuration: list[TagCategoryBase] = list()


def load_tag_configuration(config_file_name: str) -> None:
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
            else:
                tag_configuration[current_heading_index].add_item(tag_line)

    log_tags('Loaded configuration:', tag_configuration)


def load_tag_category(loaded_categories: list[TagCategory], tag_config: TagCategoryBase,
                      included_predicate: Callable[[TagItem], bool]) -> TagCategory:

    def initialize_tag(tag_category: TagCategory, tag_config: TagCategoryBaseItem,
                       included_predicate: Callable[[TagItem], bool]) -> TagItem:
        result: TagItem = TagItem((tag_config.name, tag_category))
        # Use a predicate or an included property initializer?
        result.included = included_predicate(result)
        return result

    result: TagCategory = TagCategory((tag_config.name, None))
    loaded_categories.append(result)
    result.items = [initialize_tag(result, tag, included_predicate) for tag in tag_config.items]
    return result


def load_tags(tags_file_name: str) -> list[TagCategory]:
    def load_current_tags() -> set[str]:
        with open(tags_file_name, mode='r', encoding='utf-8-sig') as f:
            # Skip <!DOCTYPE html> header line
            next(f)

            # strip '<div>' from left and '</div>\n' from right for the tag name
            result: set[str] = {get_tag_key(line[5:-7]) for line in f}
        return result

    def get_tag_key(tag_name: str) -> str:
        return tag_name.upper()

    def unregister_tag(tag: str) -> bool:
        result: bool = tag in current_tags
        if result:
            current_tags.remove(tag)
        return result

    current_tags: set[str] = load_current_tags()
    result: list[TagCategory] = list()
    for tag_category in tag_configuration:
        load_tag_category(result, tag_category, lambda tag: unregister_tag(get_tag_key(tag.name)))

    if len(current_tags):
        additional: TagCategoryBase = TagCategoryBase(('Additional tags', None))
        additional.items = [TagCategoryBaseItem((tag_name, additional)) for tag_name in current_tags]
        load_tag_category(result, additional, lambda t: True)

    log_tags('Loaded file tags:', result)
    return result


def save_tags(tags_file_name: str, tag_categories: list[str]) -> None:
    with open(tags_file_name, mode='w', encoding='utf-8-sig') as f:
        f.write('<!DOCTYPE html>\n')
        for tag in tag_categories:
            _ = f.write(f'<div>{tag}</div>\n')


def log_tags(list_description: str, tag_list: Union[list[TagCategoryBase], list[TagCategory]]) -> None:
    logging.debug(list_description)
    for category in tag_list:
        [logging.debug(f'{category.name} : {tag.__dict__}') for tag in category.items]


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
