import math


def paginate(all_objects, current_page=1, page_size=5):
    if not current_page:
        current_page = 1
    else:
        current_page = int(current_page)
    page_show_button_num = 2
    object_num = len(all_objects)
    last_page = math.ceil(object_num / page_size)
    if current_page < 1:
        current_page = 1
    elif current_page > last_page and last_page != 0:
        current_page = last_page
    previous_page = current_page-1 if current_page > 1 else 1
    next_page = current_page+1 if current_page < last_page else last_page

    beginpos = page_size*(current_page-1)
    show_object = all_objects[beginpos:beginpos+page_size]
    begin_show_page = 1
    end_show_page = last_page
    if current_page != 1 and current_page - page_show_button_num > 1:
        begin_show_page = current_page - page_show_button_num
    if current_page != last_page and current_page + page_show_button_num < last_page:
        end_show_page = current_page + page_show_button_num
    page_list = [x for x in range(begin_show_page, end_show_page + 1)]

    return show_object, page_list, current_page, previous_page, next_page, last_page
