```
            if __char_num_i == 0:
                if int(name_stroke_count_list[j][1][__char_num_i]) > int(
                        name_stroke_count_list[j + 1][1][__char_num_i]):
                    name_stroke_count_list[j], name_stroke_count_list[j + 1] = name_stroke_count_list[j + 1], \
                                                                               name_stroke_count_list[j]
            else:
                # 处理笔画数列表长度不同的情况
                try:
                    if int(name_stroke_count_list[j][1][__char_num_i]) == 0:
                        name_stroke_count_list[j][1].append('0')
                except IndexError:
                    name_stroke_count_list[j][1].append('0')
                try:
                    if int(name_stroke_count_list[j + 1][1][__char_num_i]) == 0:
                        name_stroke_count_list[j + 1][1].append('0')
                except IndexError:
                    name_stroke_count_list[j + 1][1].append('0')
                if int(name_stroke_count_list[j][1][__char_num_i - 1]) == int(
                        name_stroke_count_list[j + 1][1][__char_num_i - 1]) and int(
                    name_stroke_count_list[j][1][__char_num_i]) > int(
                    name_stroke_count_list[j + 1][1][__char_num_i]):
                    name_stroke_count_list[j], name_stroke_count_list[j + 1] = name_stroke_count_list[j + 1], \
                                                                               name_stroke_count_list[j]
```