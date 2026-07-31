class Node:
    """Simple node used for the Huffman heap and tree."""

    def __init__(self, char, frequency, left=None, right=None):
        self.char = char
        self.frequency = frequency
        self.left = left
        self.right = right

    def __lt__(self, other):
        if not isinstance(other, Node):
            return NotImplemented
        return self.frequency < other.frequency


class MinHeap:
    """A min-heap implementation for Node objects ordered by frequency."""

    def __init__(self):
        self.heap = []

    def push(self, node):
        self.heap.append(node)
        self._bubble_up(len(self.heap) - 1)

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty heap")

        min_node = self.heap[0]
        last_node = self.heap.pop()

        if not self.is_empty():
            self.heap[0] = last_node
            self._bubble_down(0)

        return min_node

    def peek(self):
        if self.is_empty():
            raise IndexError("peek from empty heap")
        return self.heap[0]

    def size(self):
        return len(self.heap)

    def is_empty(self):
        return len(self.heap) == 0

    def heapify(self, nodes):
        self.heap = nodes.copy()
        if not self.heap:
            return

        last_parent_index = (len(self.heap) - 2) // 2
        for index in range(last_parent_index, -1, -1):
            self._bubble_down(index)

    def _bubble_up(self, index):
        while index > 0:
            parent_index = (index - 1) // 2
            if self.heap[parent_index].frequency <= self.heap[index].frequency:
                break
            self.heap[parent_index], self.heap[index] = self.heap[index], self.heap[parent_index]
            index = parent_index

    def _bubble_down(self, index):
        while True:
            left_child_index = 2 * index + 1
            right_child_index = 2 * index + 2
            smallest_index = index

            if left_child_index < len(self.heap) and self.heap[left_child_index].frequency < self.heap[smallest_index].frequency:
                smallest_index = left_child_index

            if right_child_index < len(self.heap) and self.heap[right_child_index].frequency < self.heap[smallest_index].frequency:
                smallest_index = right_child_index

            if smallest_index == index:
                break

            self.heap[index], self.heap[smallest_index] = self.heap[smallest_index], self.heap[index]
            index = smallest_index


class FrequencyCounter:
    """Count frequencies of bytes or characters from input data."""

    def count_from_data(self, data):
        freq_dict = {}
        for byte_value in data:
            freq_dict[byte_value] = freq_dict.get(byte_value, 0) + 1
        return freq_dict

    def count_from_string(self, text):
        return self.count_from_data(text.encode("utf-8"))
