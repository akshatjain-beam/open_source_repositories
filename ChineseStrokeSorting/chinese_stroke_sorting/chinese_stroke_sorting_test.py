import os
import unittest

from .chinese_stroke_sorting import sort_by_stroke, write_sort_result_to_human, write_sort_result_to_file, \
    read_name_list_from_file, __read_bh__


class SortByNameTest(unittest.TestCase):
    def read_name_list_from_file_test(self, input_test):
        right_result = ['张三', '李四', '王五', '赵六', '王一', '王一二']
        self.assertEqual(input_test, right_result)

    def sort_by_stroke_test(self, input_test):
        right_result = ['王一', '王一二', '王五', '李四', '张三', '赵六']
        self.assertEqual(input_test, right_result)

    def write_sort_result_to_human_test(self, input_test):
        right_result = '王一|王一二|王五|李四|张三|赵六'
        self.assertEqual(input_test, right_result)

    def testDefaultStopwords(self):
        current_package_path = os.path.dirname(os.path.abspath(__file__))
        name_list_file_path = str("".join([current_package_path, '/test_name_list.txt']))
        name_list = read_name_list_from_file(name_list_file_path)  # 从文件中读取
        print(name_list)
        self.read_name_list_from_file_test(name_list)

        sort_result = sort_by_stroke(name_list)  # 按笔画数排序
        print(sort_result)
        self.sort_by_stroke_test(sort_result)

        result_for_human = write_sort_result_to_human(sort_result, split_char='|')  # 获取以指定分隔符分割的可读文本
        print(result_for_human)
        self.write_sort_result_to_human_test(result_for_human)

        output_file = 'result.txt'
        write_sort_result_to_file(sort_result, output_file, split_char='\n')  # 将排序结果写入到文件

    def test_empty_name_list(self):
        name_list = []
        result = sort_by_stroke(name_list)
        self.assertEqual(result, [])

    def test_single_name(self):
        name_list = ['王一']
        result = sort_by_stroke(name_list)
        self.assertEqual(result, ['王一'])

    def test_names_with_identical_strokes(self):
        name_list = ['王五', '李四', '赵六', '张三']
        result_name_list = ['王五', '李四', '张三', '赵六']
    
        result = sort_by_stroke(name_list)
        self.assertEqual(result, result_name_list)

    def test_large_input(self):
        name_list = ['一'] * 100 + ['二'] * 100
        # With a large input of identical characters, the result should be sorted by stroke counts
        result = sort_by_stroke(name_list)
        self.assertEqual(result, ['一'] * 100 + ['二'] * 100)

    def test_sorting_edge_cases(self):
        # Edge cases like names with only one character or names with stroke counts that are the same
        name_list = ['一', '丨', '亅', '丿', '丶', '乀', '乁', '乙']
        result = sort_by_stroke(name_list)
        expected_result = sorted(
            name_list, key=lambda x: int(__read_bh__().get(x, '0')))
        self.assertEqual(result, expected_result)

    def test_invalid_input(self):
        # Test handling of unexpected input types or values
        with self.assertRaises(TypeError):
            sort_by_stroke(None)  # Passing None should raise an error
        with self.assertRaises(TypeError):
            # Passing a list with mixed types should raise an error
            sort_by_stroke(['王五', 123])


if __name__ == "__main__":
    unittest.main()
