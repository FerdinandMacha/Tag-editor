import tags_model
import logging

# contains the instances of tags_model.TagCategory
tag_configuration = list()
flat_tags = dict()


def load_tag_configuration(config_file_name):
    with open(config_file_name, mode='r', encoding='utf-8-sig') as f:
        is_heading=True
        current_heading_index = -1

        for line in f:
            tag_line = line.strip()
            if not tag_line:
                is_heading = True

                # An empty line is marking the category end.
                # The next line is the other category beginning.
                continue

            if is_heading:
                tag_configuration.append(tags_model.TagCategoryBase((tag_line, None)))
                current_heading_index += 1
                is_heading = False
            else :
                tag_configuration[current_heading_index].add_item(tag_line)
                tag_key = tag_line.upper()
                if not tag_key in flat_tags:
                    flat_tags[tag_key] = tag_configuration[current_heading_index]

    log_tags('Loaded configuration:', tag_configuration)
    logging.debug('Loaded tag keys:')
    for k in flat_tags:
        logging.debug(k)


def load_tags(tags_file_name):
    def load_current_tags():
        with open(tags_file_name, mode='r', encoding='utf-8-sig') as f:
            # Skip <!DOCTYPE html> header line
            next(f)
            
            # strip '<div>' from left and '</div>\n' from right for the tag name
            result = {line[5:-7]: True for line in f}
        return result


    current_tags = load_current_tags()
    for t in current_tags:
        logging.debug(f'Tag from file: {t}')

    result = list()
    for tag_category in tag_configuration:
        category_tags = tags_model.TagCategory((tag_category.name, None))
        result.append(category_tags)
        for tag in tag_category.items:
            current_tag = category_tags.add_item((tag.name, category_tags))
            current_tag.included = True if current_tags.pop(tag.name, False) else False

    for tag_name in current_tags:
        
        if flat_tags.get(tag_name.upper(), None):

    log_tags('Loaded file tags:', result)
    return result
                

def save_tags(tags_file_name, tag_categories):
    with open(tags_file_name, mode='w', encoding='utf-8-sig') as f:
        f.write('<!DOCTYPE html>\n')
        for tag in tag_categories:
            _ = f.write('<div>'+tag+'</div>\n')        



def log_tags(list_type, tag_list):
    logging.debug(list_type)
    for category in tag_list:
        for tag in category.items:
            logging.debug(f'{category.name} : {tag.__dict__}')


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
