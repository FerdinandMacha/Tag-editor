import copy

tags = []

def load_all_tags(all_tags_file_name):
    with open(all_tags_file_name, mode='r', encoding='utf-8-sig') as f:
        is_heading=True
        current_heading_index = -1
        for line in f:
            tag_line = line.strip()
            if not tag_line:
                is_heading = True
                continue

            if is_heading:
                tags.append([tag_line])
                current_heading_index += 1
                is_heading = False
            else :
                tags[current_heading_index].append([tag_line])


def load_tags(tags_file_name):
    def load_current_tags(current_tags):
        with open(tags_file_name, mode='r', encoding='utf-8-sig') as f:
            is_header_ignored = False
            for line in f:
                if not is_header_ignored:
                    is_header_ignored = True
                    continue

                # strip '<div>' from left and '</div>\n' from right
                current_tags.append(line[5:-7])

    current_tags = []
    load_current_tags(current_tags)

    all_tags = copy.deepcopy(tags)
    for tag_category in all_tags:
        for tag in tag_category[1:]:
            tag.append(True if tag[0] in current_tags else False)

    return all_tags
                

def save_tags(tags_file_name, tags):
    with open(tags_file_name, mode='w', encoding='utf-8-sig') as f:
        f.write('<!DOCTYPE html>\n')
        for tag in tags:
               n = f.write('<div>'+tag+'</div>\n')        

