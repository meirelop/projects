import sys

class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items) - 1]

    def size(self):
        return len(self.items)

    def get_element(self, index):
        return self.items[index]


class StreamParser():
    """
    Class which processes simple xpath query
    """

    def __init__(self, algorithm, query_list):
        self.stack = Stack()
        self.result = []
        self.node_number = 0
        self.algorithm = algorithm
        self.query_list = query_list


    def process_line(self, line):
        """
        Method to process every line of input file
        :param line: input line of type: 0 a
        """
        element_id = int(line[0])
        element_name = str(line[1])

        if element_id == 0:
            # print('node:', self.node_number)
            self.stack.push(element_name)
            if self.stack.size() >= len(self.query_list):
                if self.algorithm == 'simple':
                    if_matched = self.check_match_simple()
                else:
                    if_matched = self.check_match_complex()
                if if_matched:
                    self.result.append(self.node_number)
            self.node_number += 1
        if element_id == 1:
            self.stack.pop()


    def check_match_complex(self):
        """
         Method to check whether current node matches given query (for complex queries)
        :return: True if node matches to given query, False otherwise
        """
        match = True
        old_node = ''

        for i in range(len(self.query_list)):
            current_node = self.stack.get_element(self.stack.size() - 1 - i)
            if current_node == old_node:
                j = i + 1
                while current_node == old_node:
                    current_node = self.stack.get_element(self.stack.size() - 1 - j)
                    j += 1
                    if j == self.stack.size():
                        break
            if (self.query_list[len(self.query_list) - 1 - i] != current_node):
                match = False
                break

            old_node = current_node
        return match


    def check_match_simple(self):
        """
        Method to check whether current node matches given query (for simple queries)
        :return: True if node matches to given query, False otherwise
        """
        match = True
        for i in range(len(self.query_list)):
            if (self.query_list[len(self.query_list) - 1 - i] !=
                    self.stack.get_element(self.stack.size() - 1 - i)):
                match = False
                break
        return match


def preprocess():
    """
    preprocessing of input parameters
    :return:
     algortihm - string represesnting complexity of algorithm
     query_list - query given by user, splitted to list
    """
    input_file = '/Users/meirkhan/Desktop/saclay/1 semester/Web Data Models/Practices/Project/My implementation/generated files/input3.txt'
    query_xpath = '//a'

    # input_file = sys.argv[1]
    # query_xpath = sys.argv[2]

    query_complexity = query_xpath.count('//')
    if query_complexity > 1:
        algorithm = 'complex'
        query_xpath = query_xpath.replace('/', '')
        query_list = list(query_xpath)
    else:
        algorithm = 'simple'
        query_list = query_xpath[2:].split('/')
    return algorithm, query_list, input_file

from memory_profiler import memory_usage
def main():
    try:
        algorithm, query_list, input_file = preprocess()
        streaming_instance = StreamParser(algorithm, query_list)
        c = 0
        with open(input_file, 'r') as file:
            for whole_line in file:
                line = whole_line.split()
                streaming_instance.process_line(line)
                c += 1
        # print matched nodes line by line
        # for node in streaming_instance.result:
        #     print(node)
        print('doc size:', c)
    except:
        print('Please, check your input file or query for correctness')


if __name__ == '__main__':
    mem_usage = memory_usage(main())
    print('Memory usage (in chunks of .1 seconds): %s' % mem_usage)
    print('Maximum memory usage: %s' % max(mem_usage))
    # main()