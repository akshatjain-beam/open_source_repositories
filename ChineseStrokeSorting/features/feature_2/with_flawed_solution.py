```
            if __char_num_i >= len(name_stroke_count_list[j][1]):
                name_stroke_count_list[j][1].append('0')
            if __char_num_i >= len(name_stroke_count_list[j + 1][1]):
                name_stroke_count_list[j + 1][1].append('0')
            if int(name_stroke_count_list[j][1][__char_num_i]) > int(
                    name_stroke_count_list[j + 1][1][__char_num_i]):
                name_stroke_count_list[j], name_stroke_count_list[j + 1] = name_stroke_count_list[j + 1], \
                                                                           name_stroke_count_list[j]
            elif int(name_stroke_count_list[j][1][__char_num_i]) == int(
                    name_stroke_count_list[j + 1][1][__char_num_i]) and __char_num_i != 0:
                if int(name_stroke_count_list[j][1][__char_num_i - 1]) > int(
                        name_stroke_count_list[j + 1][1][__char_num_i - 1]):
                    name_stroke_count_list[j], name_stroke_count_list[j + 1] = name_stroke_count_list[j + 1], \
                                                                               name_stroke_count_list[j]
```