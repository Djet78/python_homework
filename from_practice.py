# ----------------------- Task 6 -----------------------


def number2roman(number):
    """
    Convert positive number to roman representation

    :param number: Any positive 'int'
    :return: 'str'. Roman repr of a number
    """
    number = str(number)
    ROMAN_NUMBERS = [{1: "I", 4: "IV", 5: "V", 9: "IX"},
                     {1: "X", 4: "XL", 5: "L", 9: "XC"},
                     {1: "C", 4: "CD", 5: "D", 9: "CM"}]
    roman_num = []
    num_idx = 0
    for list_idx in range(len(number)):
        if list_idx == 3:
            current = int(number[:-3])
            roman_num.append("M" * current)
            break
        num_idx -= 1
        current = int(number[num_idx])
        if current == 0:
            continue
        if current in ROMAN_NUMBERS[list_idx]:
            roman_num.append(ROMAN_NUMBERS[list_idx][current])
        else:
            roman_num.append(ROMAN_NUMBERS[list_idx][1] * (current % 5))
            if current > 5:
                roman_num.append(ROMAN_NUMBERS[list_idx][5])
    return "".join(roman_num[::-1])

# ----------------------- Task 7 -----------------------


def even_sum_mul_last(lst):
    return sum(lst[::2]) * lst[-1]

# ----------------------- Task 9 -----------------------


def encrypt(text, shift):
    return "".join([chr(ord(x) + shift) for x in text])

# ----------------------- Task 10 -----------------------


def sort_tuple(lst_of_tuples):
    return sorted(lst_of_tuples, key=lambda x: x[1])

# ----------------------- Task 11 -----------------------


def remove_falsy_elems(lst):
    return [x for x in lst if x]
