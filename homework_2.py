import re

# ------------------- Task 1 ----------------------

def not_occur_number_in(iterable):
    """
    Seeking lowest number witch not occur in 'iterable' and bigger than 0

    :param iterable: object, excepting dict`s
    :return: 'int'. Founded number
    """
    iterable = sorted(list(set(iterable)))
    if not iterable or iterable[-1] <= 0:
        return 1
    if len(iterable) == 1:
        return iterable[0] + 1
    for idx, elem in enumerate(iterable[:-1]):
        if elem + 1 != iterable[idx + 1]:
            return elem + 1
    return iterable[-1] + 1

# ------------------- Task 2 ----------------------


def longest_binary_gap(integer):
    """
    Seeking longest binary gap in given digit

    :param integer: any 'int' value
    :return: 'int'. Length of longest binary gap. '0' if haven`t gaps
    """
    if not isinstance(integer, int):
        raise TypeError("Only 'int' value allowed!")
    binary_repr = bin(integer)
    binary_gaps = re.findall(r"(?<=1)0+(?=1)", binary_repr)
    if not binary_gaps:
        return 0
    binary_gaps.sort(reverse=True)
    return len(binary_gaps[0])

# ------------------- Task 3 ----------------------


def shift_array(array, shift):
    """
    Rotate array on given shift

    :param array: list or tuple of values
    :param shift: 'int' value
    :return: 'list'. Shifted list

    >>> shift_array([1, 2, 3, 4], 4)
    [1, 2, 3, 4]
    >>> shift_array([1, 2, 3], -1)
    [2, 3, 1]
    >>> shift_array([3, 8, 9, 7, 6], 3)
    [9, 7, 6, 3, 8]
    >>> shift_array([3, 8, 9, 7, 6], 0)
    [3, 8, 9, 7, 6]
    >>> shift_array(["a", "b", "c"], 1)
    ['c', 'a', 'b']
    >>> shift_array(22, 1)
    Traceback (most recent call last):
        ...
    TypeError: Object is not iterable, can`t make rotations
    >>> shift_array([1, 2, 3], "")
    Traceback (most recent call last):
        ...
    TypeError: Only int allow
    """
    if not hasattr(array, "__iter__"):
        raise TypeError("Object is not iterable, can`t make rotations")
    if not isinstance(shift, int):
        raise TypeError("Only int allow")
    shifted = [0]*len(array)
    for idx, elem in enumerate(array):
        new_idx = (idx + shift) % len(array)
        shifted[new_idx] = elem
    return shifted

# ------------------- Task 4 ----------------------


def count_natural_divisors_1(integer):
    """
    Counts natural divisors of an 'integer'

    :param integer: positive 'int' value
    :return:'int'. Quantity of natural divisors of 'integer'
    """
    if not isinstance(integer, int):
        raise TypeError("Only 'int' value allowed!")
    if integer < 1:
        raise ValueError("Only positive numbers allowed!")
    divisors = 1
    for number in range(1, (integer // 2) + 1):
        if integer % number == 0:
            divisors += 1
    return divisors


# ------------------- Task 5 ----------------------


def longest_correct_pass(string):
    """
    Seeking suitable password in given string

    there are three restrictions on the format of the password:
        it has to contain only alphanumerical characters (a−z, A−Z, 0−9);
        there should be an even number of letters;
        there should be an odd number of digits.
    :return: 'int'. Length of longest suitable password, or -1 if any does not suit
    """
    if not isinstance(string, str):
        raise TypeError("Only strings allowed!")
    passes = string.split()
    for pas in sorted(passes, key=len, reverse=True):
        letters = 0
        digits = 0
        for char in sorted(pas):
            if not char.isalpha() and not char.isdigit():
                letters = 0
                digits = 0
                break
            if char.isalpha():
                letters += 1
            elif char.isdigit():
                digits += 1
        if letters % 2 == 0 and digits % 2 != 0:
            return len(pas)
    return -1

# ------------------- Task 6 ----------------------


def is_nested(string):
    if not isinstance(string, str):
        raise TypeError
    string = string.lstrip(")")
    string = string.rstrip("(")
    if 0 <= len(string) <= 3:
        return 0
    previous_bracket_idx = 1
    for bracket in string[2:-1]:
        if bracket == ")" and string[previous_bracket_idx] == "(":
            return 1
        previous_bracket_idx += 1
    return 0


if __name__ == "__main__":
    import doctest
    doctest.testmod()
