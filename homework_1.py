# ------------------- Task 1 ----------------------


def generate_dict(list_of_numbers):
    return {i: i * i for i in list_of_numbers}


keys = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(generate_dict(keys))

# ------------------- Task 2 ----------------------


def generate_even_list():
    return [i for i in range(100 + 1) if i % 2 == 0]


print(generate_even_list())

# ------------------- Task 3 ----------------------
from random import randint


def consonant2vowel(text):
    """
    Transforms consonant letters to random vowel letters

    :param text: takes given string
    :return: 'str'. Formatted text
    """
    VOVEL_LETTERS = ["B", "C", "D", "F", "G", "H", "J", "K", "L", "M", "N",
                     "P", "Q", "R", "S", "T", "V", "W", "X", "Y", "Z"]
    CONSONANT_LETTERS = ["A", "E", "I", "O", "U", "Y"]
    char_list = []
    for i, char in enumerate(text):
        if char.upper() in CONSONANT_LETTERS:
            char = VOVEL_LETTERS[randint(0, len(VOVEL_LETTERS) - 1)]
            char_list.append(char)
        else:
            char_list.append(char)
    return "".join(char_list)


test_text = "Anyone who reads Old and Middle English literary texts will be familiar with the mid-brown " \
            "volumes of the EETS, with the symbol of Alfred's jewel embossed on the front cover."

print(consonant2vowel(test_text))

# ------------------- Task 4 ----------------------

lst = [10, 11, 2, 3, 5, 8, 23, 11, 2, 5, 76, 43, 2, 32, 76, 3, 10, 0, 1]


# 1)
def remove_duplications(lst):
    return list(set(lst))

print(remove_duplications(lst))


# 2)
def get_max_3_numbers(lst):
    return sorted(lst, reverse=True)[:3]

print(get_max_3_numbers(lst))


# 3)
def lowest_elem_index(lst):
    return lst.index(min(lst))

print(lowest_elem_index(lst))


# 4)
def reverse_list(lst):
    return lst[::-1]

print(reverse_list(lst))

# ------------------- Task 5 ----------------------


def dict_keys_intersection(dict_1, dict_2):
    return dict_1.keys() & dict_2.keys()


dict_one = {"a": 1, "b": 2, "c": 3, "d": 4}
dict_two = {"a": 6, "b": 7, "z": 20, "x": 40}

print(dict_keys_intersection(dict_one, dict_two))

# ------------------- Task 6 ----------------------

data = [{"name": "Viktor", "city": "Kiev", "age": 30},
        {"name": "Maksim", "city": "Dnepr", "age": 20},
        {"name": "Vladimir", "city": "Lviv", "age": 32},
        {"name": "Andrey", "city": "Kiev", "age": 34},
        {"name": "Artem", "city": "Dnepr", "age": 50},
        {"name": "Dmitriy", "city": "Lviv", "age": 21}]


# 1)
def sort_by_age(list_of_dicts):
    return sorted(list_of_dicts, key=lambda i: i["age"])

print(sort_by_age(data))

# 2)
def group_by_city(list_of_dicts):
    CITY_VALUE = "city"
    new_dict = {}
    for i in list_of_dicts:
        pattern = {"name": i["name"], "age": i["age"]}
        if i[CITY_VALUE] not in new_dict.keys():
            new_dict[i[CITY_VALUE]] = [pattern]
        else:
            new_dict[i[CITY_VALUE]].append(pattern)
    return new_dict


print(group_by_city(data))
