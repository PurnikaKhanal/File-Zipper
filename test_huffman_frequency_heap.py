import random
import unittest

from huffman_frequency_heap import FrequencyCounter, MinHeap, Node


class TestNode(unittest.TestCase):
    def test_node_creation(self):
        node = Node("a", 5)
        self.assertEqual(node.char, "a")
        self.assertEqual(node.frequency, 5)
        self.assertIsNone(node.left)
        self.assertIsNone(node.right)

    def test_node_comparison(self):
        node1 = Node("a", 5)
        node2 = Node("b", 3)
        self.assertTrue(node2 < node1)
        self.assertFalse(node1 < node2)


class TestMinHeap(unittest.TestCase):
    def test_heap_push_and_peek(self):
        heap = MinHeap()
        node1 = Node("a", 5)
        node2 = Node("b", 3)
        node3 = Node("c", 7)

        heap.push(node1)
        heap.push(node2)
        heap.push(node3)

        min_node = heap.peek()
        self.assertEqual(min_node.char, "b")
        self.assertEqual(min_node.frequency, 3)

    def test_heap_pop(self):
        heap = MinHeap()
        nodes = [Node("a", 5), Node("b", 3), Node("c", 7), Node("d", 1)]
        for node in nodes:
            heap.push(node)

        self.assertEqual(heap.pop().frequency, 1)
        self.assertEqual(heap.pop().frequency, 3)
        self.assertEqual(heap.pop().frequency, 5)
        self.assertEqual(heap.pop().frequency, 7)
        self.assertTrue(heap.is_empty())

    def test_heap_size(self):
        heap = MinHeap()
        self.assertEqual(heap.size(), 0)

        heap.push(Node("a", 1))
        self.assertEqual(heap.size(), 1)

        heap.push(Node("b", 2))
        self.assertEqual(heap.size(), 2)

        heap.pop()
        self.assertEqual(heap.size(), 1)

    def test_heap_maintains_order(self):
        heap = MinHeap()
        random.seed(42)
        values = [random.randint(1, 100) for _ in range(20)]

        for val in values:
            heap.push(Node(None, val))

        sorted_values = []
        while not heap.is_empty():
            sorted_values.append(heap.pop().frequency)

        self.assertEqual(sorted_values, sorted(sorted_values))

    def test_heap_with_duplicates(self):
        heap = MinHeap()
        heap.push(Node("a", 5))
        heap.push(Node("b", 5))
        heap.push(Node("c", 5))

        self.assertEqual(heap.size(), 3)
        heap.pop()
        heap.pop()
        heap.pop()
        self.assertTrue(heap.is_empty())

    def test_heapify_builds_heap(self):
        heap = MinHeap()
        nodes = [Node("a", 8), Node("b", 4), Node("c", 6), Node("d", 2)]
        heap.heapify(nodes)

        self.assertEqual(heap.peek().frequency, 2)
        self.assertEqual(heap.size(), 4)


class TestFrequencyCounter(unittest.TestCase):
    def test_frequency_count_simple(self):
        counter = FrequencyCounter()
        freqs = counter.count_from_string("hello")

        self.assertEqual(len(freqs), 4)
        total = sum(freqs.values())
        self.assertEqual(total, 5)

    def test_frequency_count_from_bytes(self):
        counter = FrequencyCounter()
        data = bytes([1, 2, 1, 3, 1, 2])
        freqs = counter.count_from_data(data)

        self.assertEqual(freqs[1], 3)
        self.assertEqual(freqs[2], 2)
        self.assertEqual(freqs[3], 1)

    def test_frequency_single_character(self):
        counter = FrequencyCounter()
        freqs = counter.count_from_string("aaaa")

        self.assertEqual(len(freqs), 1)
        total = sum(freqs.values())
        self.assertEqual(total, 4)

    def test_frequency_empty_input(self):
        counter = FrequencyCounter()
        freqs = counter.count_from_data(b"")

        self.assertEqual(freqs, {})
        self.assertEqual(len(freqs), 0)


if __name__ == "__main__":
    unittest.main()
