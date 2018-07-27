# ------------------- Task 1 ----------------------
import collections


def my_lru(max_storage_size):

    def pre_wrapper(func):
        cache = collections.OrderedDict()

        def wrapper(*args):
            key = "{}".format(args)
            if key not in cache:
                if len(cache) == max_storage_size:
                    cache.popitem(last=False)
                res = func(*args)
                cache[key] = res
                return cache.get(key)
            else:
                return cache.get(key)
        return wrapper
    return pre_wrapper


@my_lru(5)
def mul(x, y):
    return x * y


res1 = mul(2, 2)
res2 = mul(3, 3)
res3 = mul(2, 2)
res4 = mul(2, 3)
res5 = mul(2, 7)
res6 = mul(2, 9)
res7 = mul(2, 11)
res8 = mul(1, 1)

print(res1, res2, res3, res4, res5, res6, res7, res8)

# ------------------- Task 2 ----------------------


def modulo_check(func):
    def wrapper(*args):
        func_res = func(*args)
        to_check = func_res % 100
        if to_check == 0:
            print("We are ok")
        else:
            print("Bad news guys, we got {}".format(to_check))
    return wrapper


@modulo_check
def my_func(x):
    return x * 7


my_func(101)
my_func(100)


# ------------------- Task 3 ----------------------
# import time
# import signal
#
#
# def time_meter(seconds_to_implement):
#
#     def pre_wrapper(func):
#
#         def wrapper(*args):
#             start_time = time.time()
#             while True:
#                 present_time = time.time()
#                 res = func(*args)
#                 if (present_time - start_time) > seconds_to_implement:
#                     break
#                 return res
#         return wrapper
#     return pre_wrapper
#
#
# @time_meter(4)
# def my_func():
#     return sum(range(1000000))
#
# ------------------- Task 4 ----------------------


def my_memoize(func):
    cache = {}
    implementation_counter = 0
    cache_counter = 0

    def wrapper(*args):
        nonlocal implementation_counter, cache_counter
        key = "{}".format(args)
        if key not in cache:
            implementation_counter += 1
            res = func(*args)
            cache[key] = res
            print("Function executed with counter = {}, function result = {}".format(implementation_counter, res))
        else:
            cache_counter += 1
            print("Used cache with counter = {}, result = {}".format(cache_counter, cache[key]))
    return wrapper


@my_memoize
def my_func(a):
    return 10 * a


my_func(1)
my_func(5)
my_func(10)
my_func(1)
my_func(2)
my_func(1)
my_func(20)
my_func(5)
