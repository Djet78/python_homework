import logging
import os.path
import json
import shutil
# ------------------- Task 1 ----------------------


def create_logger(name=__name__, format="File: %(filename)s, Func:%(funcName)s, %(levelname)s:%(message)s", **kwargs):
    """ Logger initial"""
    logging.basicConfig(format=format, **kwargs)
    return logging.getLogger(name)


# ------------------- Task 2 ----------------------


def read_files(*pathways):
    """
    Read files and concatenate them.

    :param pathways: If pathways is not valid, function ignore them
    :return: 'str'. Concat of all readed files
    """
    logger = create_logger(level=20, filename="logs.txt")
    logger.info("Start with args: {}".format(pathways))
    lst = []
    for path in pathways:
        if os.path.isfile(path):
            with open(path) as handle:
                lst.append(handle.read())
    logger.info("Result: {}".format("".join(lst)))
    return "".join(lst)


def write_txt2bytes(file_name, txt):
    """
    Write to 'file_name' given 'txt' in binary format

    :return: None
    """
    logger = create_logger(level=20, filename="logs.txt")
    logger.info("Start write info to: {}".format(file_name))
    with open(file_name, "wb") as handle:
        handle.write(txt.encode())
    logger.info("Exit from func")


# ------------------- Task 3 ----------------------


def identify_file(path):
    """
    Return dict with file name, directory and abspath

    If given path is not exist or lead to a not file object raise TypeError
    :param path: Path to a file
    :return: 'dict'. File name, directory , abspath
    """
    logger = create_logger(level=20, filename="logs.txt")
    logger.info("Start")
    if not os.path.exists(path):
        logger.error("Not existing path")
        raise TypeError("Path is not exist")
    elif not os.path.isfile(path):
        logger.error("Not a file path was given")
        raise TypeError("Given path should lead to a file")
    abs_path = os.path.abspath(path).split("\\")
    result = {"Name": abs_path[-1], "Dir": abs_path[-2], "Path": "\\".join(abs_path)}
    logger.info("End")
    return result


# ------------------- Task 4 ----------------------


def string2dict(string):
    string = [elem.split(": ") for elem in string.split(",")]
    return {k: v for k, v in string}


def write_dict2json_file(dictionary, file_path):
    dictionary = json.dumps(dictionary)
    with open(file_path, "w") as handle:
        handle.write(dictionary)


# ------------------- Task 5 ----------------------


def my_copy(src, dst):
    """
    Copy file or directory

    :param src: Path to File or Dir for copy
    :param dst: Destination path
    :return: None
    """
    logger = create_logger(level=20, filename="logs.txt")
    if not os.path.exists(src):
        logger.info("Wrong path given")
        raise TypeError("One of pathways is not exist")
    if os.path.isfile(src):
        try:
            shutil.copy2(src, dst)
        except shutil.SameFileError as why:
            logger.info("Create file with same name attempt")
            raise shutil.SameFileError(why)
    elif os.path.isdir(src):
        try:
            shutil.copytree(src, dst)
        except FileExistsError as why:
            logger.info("Create directory with same name attempt")
            raise FileExistsError(why)


if __name__ == "__main__":
    write_txt2bytes("Result.bin", read_files("txt1.txt", "txt2.txt"))

    print(identify_file("Result.bin"))

    string = "Name: Peter, Age: 20, Country: USA"
    write_dict2json_file(string2dict(string), "result.json")

    my_copy(r"Result.bin", r"D:\Programming\Python3x\github_repositories\python_homework\Result.bin")
    my_copy("D:\Programming\Python3x\github_repositories\python_homework", r"D:\new_dir")
