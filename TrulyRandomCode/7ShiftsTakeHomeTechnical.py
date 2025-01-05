import unittest
import re

def Input_Handler(input_string):
    # Takes in a string as input and outputs a delimited list of strings
    if input_string[:2] != "//":
        delimiter = ','
    else:
        delimiter = input_string[2:input_string.find("\n")]
        input_string = input_string[input_string.find("\n") + 1:]

    # Remove newlines once instead of splitting
    input_string = input_string.replace('\n', '')
    
    # Use compiled regex pattern for better performance
    pattern = re.compile('[' + delimiter + ']+')
    output_list = pattern.split(input_string)

    return output_list

def Add(numbers):
    # Takes in a string of delimited integers, passes the list to a helper function
    # which breaks the string by the delimiter and hands list of strings back
    # the list is iterated through, empty strings are set to zero, negatives added to
    # a list that will be checked for ValueErrors and any positive integers are summed.
    str_list_to_convert = Input_Handler(numbers)
    running_sum = 0
    negative_numbers = []

    # Single pass through numbers instead of multiple lists
    for num_as_str in str_list_to_convert:
        if not num_as_str:
            continue
            
        num = int(num_as_str)
        if num < 0:
            negative_numbers.append(num)
        elif num <= 1000:
            running_sum += num

    if negative_numbers:
        raise Exception('Negative(s) not allowed: ' + ', '.join(map(str, negative_numbers)))

    return running_sum

class TestSum(unittest.TestCase):

    def test_add(self):
        # Part 1
        self.assertEqual(Add("1, 2, 3"), 6, "Testing Normal input. Should be 6")
        self.assertEqual(Add(",, 3"), 3, "Testing empty strings. Should be 3")
        self.assertEqual(Add(""), 0, "Testing all strings. Should be 0")
        self.assertEqual(Add("1"), 1, "Testing single strings. Should be 1")

        # Part 2
        self.assertEqual(Add("1\n, 2, 3"), 6, "Testing given tests. Should be 6")
        self.assertEqual(Add("1, \n2, 4"), 7, "Testing given tests. Should be 7")
        self.assertEqual(Add("\n\n\n"), 0, "Single with newlines. Should be 0")

        # Part 3
        self.assertEqual(Add("//;\n1;3;4"), 8, "Testing single delimiter.Should be 8")
        self.assertEqual(Add("//$$\n1$$ 2$$ 3"), 6, "Testing plural delimiter")
        self.assertEqual(Add("//delimiter\n2delimiter 3delimiter 8"), 13, "Testing plural delimiter. Should be 13")

        # Part 4
        self.assertRaises(Exception, Add, "-1, 2, 3")
        self.assertRaises(Exception, Add, "-1, -2, -3")

        # Bonus
        self.assertEqual(Add("1000, 999, 1001"), 1999, "Testing >1000 input. Should be 1999")
        self.assertEqual(Add("//$e\n1$ 2e 3"), 6, "Testing multiple delimiter")
        self.assertEqual(Add("//$e%\n1$% 2$e% 3"), 6, "Testing multiple, plural delimiter")

if __name__ == '__main__':
    unittest.main()