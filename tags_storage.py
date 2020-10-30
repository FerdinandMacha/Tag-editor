import copy
import tags_model
import logging
import json

# contains the instances of tags_model.TagCategory
tag_categories = list()


def load_tag_categories(config_file_name):
    with open(config_file_name, mode='r', encoding='utf-8-sig') as f:
        is_heading=True
        current_heading_index = -1

        logging.debug('Loading file...')

        for line in f:
            tag_line = line.strip()
            if not tag_line:
                is_heading = True

            if is_heading:
                tag_categories.append(tags_model.TagCategory((tag_line, None)))
                current_heading_index += 1
                is_heading = False
            else :
                tag_categories[current_heading_index].add_item(tag_line)
    for i in tag_categories:
        for t in i.items:
            logging.debug(i.name, ':', t.name)


def load_tags(tags_file_name):
    def load_current_tags():
        with open(tags_file_name, mode='r', encoding='utf-8-sig') as f:
            # Skip <!DOCTYPE html> header line
            next(f)
            
            # strip '<div>' from left and '</div>\n' from right for the tag name
            result = {line[5:-7]: False for line in f}
        return result


    current_tags = load_current_tags()

    # all_tags = copy.deepcopy(tag_categories)
    all_tags = list()
    for tag_category in tag_categories:
        category_tags = tags_model.TagCategory(tag_category.category)
        all_tags.append(category_tags)
        for tag in tag_category.tags:
            current_tag = category_tags.add_tag_name(tag)
            current_tag.included = True if current_tags.pop(tag, False) else False

    return all_tags
                

def save_tags(tags_file_name, tag_categories):
    with open(tags_file_name, mode='w', encoding='utf-8-sig') as f:
        f.write('<!DOCTYPE html>\n')
        for tag in tag_categories:
            _ = f.write('<div>'+tag+'</div>\n')        


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
