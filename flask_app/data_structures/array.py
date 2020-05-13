"""
C library
"""
import ctypes


class Array:
    """Creates an array with size elements"""
    def __init__(self, size):
        """initialize functions attributes"""
        assert size > 0, "Array size must be > 0"
        self._size = size
        # Create the array structure using the ctypes module.
        py_array_type = ctypes.py_object * size
        self._elements = py_array_type()
        self._new_element_pos = -1
        # Initialize each element.
        self.clear(0)

    # Returns the size of the array.
    def __len__(self):
        """abstract function"""
        return self._size

    # Gets the contents of the index element.
    def __getitem__(self, index):
        """abstract function"""
        assert 0 <= index < len(self), "Array subscript out of range"
        return self._elements[index]

    # Puts the value in the array element at index position.
    def __setitem__(self, index, value):
        """abstract function"""
        assert 0 <= index < len(self), "Array subscript out of range"
        self._elements[index] = value

    # Clears the array by setting each element to the given value.
    def clear(self, value):
        """abstract function"""
        for i in range(len(self)):
            self._elements[i] = value

    # Returns the array's iterator for traversing the elements.
    def __iter__(self):
        """abstract function"""
        return _ArrayIterator(self._elements)

    def __str__(self):
        """
        Converts structure to a string.

        :return: converted structure.
        """
        to_return = "["
        for index in range(self._size - 1):
            to_print = str(self[index])
            to_return = to_return + to_print + ","
        to_print = str(self[self._size - 1])
        return to_return + to_print + "]"

    def append_array(self, item):
        """
        item: an element to append on new self._new_element_pos
        """
        self._new_element_pos += 1
        self._elements[self._new_element_pos] = item
        self._size += 1

    def split(self, char):
        """
        char: str, a character with which split this text
        """
        self2 = Array(50)
        string = self[0]
        position_next_line = 0
        for i in range(75, len(string)):
            ch = string[i]
            if ch == char:
                self2.append_array(string[position_next_line:i - 1])
                position_next_line = i + 1

        return self2

    def join_array(self, char):
        """
        char: str, with which to join array elements
        """
        result_str = ""
        for i in range(self._size):
            if self[i] != 0:
                result_str += self[i] + char
            else:
                break

        return result_str


# An iterator for the Array ADT.
class _ArrayIterator:
    def __init__(self, the_array):
        """abstract function"""
        self._array_ref = the_array
        self._cur_index = 0

    def __iter__(self):
        """abstract function"""
        return self

    def __next__(self):
        """abstract function"""
        if self._cur_index < len(self._array_ref):
            entry = self._array_ref[self._cur_index]
            self._cur_index += 1
            return entry
        else:
            raise StopIteration
