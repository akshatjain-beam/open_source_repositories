import os
import unittest

from .chinese_stroke_sorting import sort_by_stroke, write_sort_result_to_human, write_sort_result_to_file, \
    read_name_list_from_file, __sort__


class SortByNameTest(unittest.TestCase):
    def read_name_list_from_file_test(self, input_test):
        """Check if the input name list matches the expected list from the file."""
        right_result = ['张三', '李四', '王五', '赵六', '王一', '王一二']
        self.assertEqual(input_test, right_result)

    def sort_by_stroke_test(self, input_test):
        """Verify that the sorted list of names matches the expected order based on stroke counts."""
        right_result = ['王一', '王一二', '王五', '李四', '张三', '赵六']
        self.assertEqual(input_test, right_result)

    def write_sort_result_to_human_test(self, input_test):
        """Check if the human-readable result format matches the expected output."""
        right_result = '王一|王一二|王五|李四|张三|赵六'
        self.assertEqual(input_test, right_result)

    def testDefaultStopwords(self):
        """Test reading a name list from a file, sorting it, and writing the results to an output file."""
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


class TestSortFunction(unittest.TestCase):
    def setUp(self):
        """Set up the test case by initializing the global variable __char_num_i."""
        global __char_num_i
        # Set a default value for __char_num_i for each test
        __char_num_i = 0

    def test_empty_list(self):
        """Test the sorting function with an empty list; expect an empty list as the result."""
        global __char_num_i
        __char_num_i = 0
        result = __sort__([])
        self.assertEqual(result, [])

    def test_single_element(self):
        """Test the sorting function with a single element; expect the same element in the result."""
        global __char_num_i
        __char_num_i = 0
        result = __sort__([('name1', ['3'])])
        self.assertEqual(result, [('name1', ['3'])])

    def test_basic_sorting(self):
        """Test the sorting function with a basic list; expect it to be sorted correctly by stroke counts."""
        input_list = [['Name1', ['5', '3']], ['Name2', ['3', '4']], ['Name3', ['4', '2']]]
        expected_output = [['Name1', ['5', '3', '0']], ['Name2', ['3', '4', '0']], ['Name3', ['4', '2', '0']]]
        self.assertEqual(__sort__(input_list), expected_output)
    
    def test_equal_first_char(self):
        """Test sorting when the first character's stroke count is equal; expect sorting by subsequent counts."""
        global __char_num_i
        __char_num_i = 1
        input_list = [['Name1', ['3', '5']], ['Name2', ['3', '3']], ['Name3', ['3', '4']]]
        expected_output = [['Name1', ['3', '5', '0']], ['Name2', ['3', '3', '0']], ['Name3', ['3', '4', '0']]]
        self.assertEqual(__sort__(input_list), expected_output)
    
    def test_different_length_lists(self):
        """Test sorting with lists of different lengths; expect missing counts to be filled with '0'."""
        input_list = [['Name1', ['5']], ['Name2', ['3', '4']], ['Name3', ['4', '2', '1']]]
        expected_output = [['Name1', ['5', '0', '0']], ['Name2', ['3', '4', '0']], ['Name3', ['4', '2', '1']]]
        self.assertEqual(__sort__(input_list), expected_output)

    def test_all_equal(self):
        """Test sorting when all elements are equal; expect them to remain in the original order with '0' appended."""
        input_list = [['Name1', ['3', '2']], ['Name2', ['3', '2']], ['Name3', ['3', '2']]]
        expected_output = [['Name1', ['3', '2', '0']], ['Name2', ['3', '2', '0']], ['Name3', ['3', '2', '0']]]
        self.assertEqual(__sort__(input_list), expected_output)

if __name__ == "__main__":
    unittest.main()
