```
def sort_by_stroke(name_list_input):
    global __char_num_i
    __char_num_i = 0
    name_stroke_count_list = __init_name_stroke_count_list__(name_list_input, __read_bh__())

    while True:
        name_stroke_count_list = __sort__(name_stroke_count_list)
        if not __find_char_num_i_change__(name_stroke_count_list):
            break

    name_result_list = __remove_stroke_count__(name_stroke_count_list)
    return name_result_list
```