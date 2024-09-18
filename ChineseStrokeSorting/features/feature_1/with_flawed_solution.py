```
def sort_by_stroke(name_list_input):
    chinese_char_dict = __read_bh__()
    name_stroke_count_list = __init_name_stroke_count_list__(name_list_input, chinese_char_dict)
    while __find_char_num_i_change__(name_stroke_count_list):
        name_stroke_count_list = __sort__(name_stroke_count_list)
    sort_result_list = __remove_stroke_count__(name_stroke_count_list)
    return sort_result_list
```