import logging
import functools
import json
import os.path
import yaml

def create_logger(name=__name__, format="File: %(filename)s, Func:%(funcName)s, %(levelname)s:%(message)s", **kwargs):
    """ Logger initial"""
    logging.basicConfig(format=format, **kwargs)
    return logging.getLogger(name)

# ------------------- Task 1 ----------------------


def singleton(cls):
    instance = {}

    @functools.wraps(cls)
    def wrapper(*args, **kwargs):
        if cls not in instance:
            instance[cls] = cls(*args, **kwargs)
        return instance[cls]
    return wrapper


@singleton
class IPManipulator:

    ipm_logger = create_logger(filename="logs.txt", filemode="w", level=10)

    def __init__(self, ip_list):
        self._ip_list = ip_list

    # 1.1)
    @property
    def ip_list(self):
        self.ipm_logger.debug("result: {}".format(self._ip_list))
        return self._ip_list

    @ip_list.setter
    def ip_list(self, new_list):
        self._ip_list = new_list

    def _split_ips(self):
        return [x.split(".") for x in self._ip_list]

    # 1.2)
    def get_reversed_ips(self):
        res = [".".join(x[::-1]) for x in self._split_ips()]
        self.ipm_logger.debug("result: {}".format(res))
        return res

    # 1.3)
    def get_ips_without_1st_octet(self):
        res = [".".join(x[1:]) for x in self._split_ips()]
        self.ipm_logger.debug("result: {}".format(res))
        return res

    # 1.4)
    def get_ips_last_octet(self):
        res = [x[-1] for x in self._split_ips()]
        self.ipm_logger.debug("result: {}".format(res))
        return res


# ------------------- Task 2 ----------------------


class JSONHandler:
    """ Contain operations with json files """

    jsonh_logger = create_logger(filename="logs.txt", filemode="w", level=30)

    @classmethod
    def _check_file_format(cls, path):
        """
        Check given file format.

        Raises 'TypeError' if it`s not json file
        """
        if os.path.isdir(path) or not path.endswith(".json"):
            cls.jsonh_logger.error("TypeError: Not a json file was given")
            raise TypeError("Error! Path should lead to json file")

    @classmethod
    def _check_data_to_write(cls, data):
        """
        Check given data on correctness before write

        Raises 'TypeError' if data does not match json standards
        """
        if not isinstance(data, dict):
            cls.jsonh_logger.error("Not a dict object was given")
            raise TypeError("Data is not a dict object! Unsupported by json")
        try:
            json.dumps(data)
        except TypeError as why:
            cls.jsonh_logger.error("TypeError: Invalid data to write: {}".format(why))
            raise TypeError("Invalid data to write: {}".format(why))

    @classmethod
    def _check_path_for_read(cls, path):
        """
        Check path before read

        Raises 'TypeError' if given path lead to a not json file
        Raises 'FileNotFoundError' for obvious reasons
        """
        cls._check_file_format(path)
        try:
            handle = open(path)
        except FileNotFoundError as why:
            cls.jsonh_logger.error("FileNotFoundError: {}".format(why))
            raise FileNotFoundError("{}".format(why))
        handle.close()

    @classmethod
    def _check_data_in_file(cls, data):
        """
        Check validity of data

        Raises 'ValueError' if data in file is not valid
        """
        try:
            json.loads(data)
        except json.decoder.JSONDecodeError as why:
            cls.jsonh_logger.error("json.decoder.JSONDecodeError: {}".format(why))
            raise ValueError("Not valid data in file. {}".format(why))

    # 2.1)
    @classmethod
    def write(cls, path, data, mode="w"):
        """
        Create the new json file on given path with json data in it

        :param path: To file
        :param data: For write
        :param mode: support only: 'w', 'a', 'x' file operations with the same functional
        """
        cls._check_file_format(path)
        if mode not in ["w", "a", "x"]:
            raise AttributeError("Wrong kword value: {}, only: 'w', 'a', 'x' supported".format(mode))
        cls._check_data_to_write(data)
        try:
            with open(path, mode) as handle:
                json_data = json.dumps(data)
                handle.write(json_data)
        except PermissionError as why:
            cls.jsonh_logger.error("Exception: {}".format(why))
            raise PermissionError("Wrong path: {}".format(why))

    # 2.2)
    @classmethod
    def read(cls, path):
        """
        Read data from json file

        If data in file was dumped many times program retrieves data until:
         - it become a dict type obj.
         - exception occur
        :return: 'dict'.
        """
        cls._check_path_for_read(path)
        with open(path) as handle:
            data = handle.read()
            while not isinstance(data, dict):
                cls._check_data_in_file(data)
                data = json.loads(data)
            return data

    # 2.3)
    @classmethod
    def unite_data(cls, new_file, *file_pathways):
        """
        Read given 'file_pathways' and write all data in 'new_file'

        Written data will have view: {'file_path': 'data from file', 'file_path_2': 'data from file 2', ...}
        Program skip pathways under such conditions:
         - 'file_pathways' contains not valid pathways
         - Valid pathways contains broken/not valid data

        :param new_file: json file to write all read data
        :param file_pathways: json files to read
        :return: 'list of tuples'. View: [('Not valid path', 'Exception')]
        Example: [('resu2.json', FileNotFoundError("[Errno 2] No such file or directory: 'resu2.json'",))]
        """
        all_data = {}
        wrong_pathways = []

        for path in file_pathways:
            try:
                path = os.path.abspath(path)
                data = cls.read(path)
                all_data[path] = data
            except Exception as ex:
                wrong_pathways.append((path, ex))

        cls.write(new_file, all_data)
        return wrong_pathways

    # 2.4)
    @classmethod
    def get_relative_path(cls, path, start=None):
        """ Only for json files"""
        cls._check_file_format(path)
        return os.path.relpath(path, start=start)

    # 2.5)
    @classmethod
    def get_abs_path(cls, filename):
        """ Only for json files"""
        cls._check_file_format(filename)
        return os.path.abspath(filename)


# ------------------- Task 3 ----------------------

class PersonalData:

    def __init__(self, unit_name, mac_address, ip_address, login, password):
        self.__unit_name = unit_name
        self.__mac_address = mac_address
        self.__ip_address = ip_address
        self.__login = login
        self.__password = password

    @property
    def unit_name(self):
        return self.__unit_name

    @unit_name.setter
    def unit_name(self, value):
        self.__unit_name = value

    @property
    def mac_address(self):
        return self.__mac_address

    @mac_address.setter
    def mac_address(self, value):
        self.__mac_address = value

    @property
    def ip_address(self):
        return self.__ip_address

    @ip_address.setter
    def ip_address(self, value):
        self.__ip_address = value

    @property
    def login(self):
        return self.__login

    @login.setter
    def login(self, value):
        self.__login = value

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, value):
        self.__password = value


# ------------------- Task 4 ----------------------

class YAMLHandler:

    yamlh_logger = create_logger(level=30, filename="log.txt", filemode="w")

    def _check_file_format(self, path):
        """
        Check given file format.

        Raises 'TypeError' if it`s not yaml file
        """
        if os.path.isdir(path) or not path.endswith((".yaml", ".yml")):
            self.yamlh_logger.error("TypeError: Not a yaml file was given")
            raise TypeError("Error! Path should lead to yaml file")

    def _check_data_in_file(self, data):
        """
        Check validity of data

        Raises 'yaml.parser.ParserError' if data in file is not valid
        """
        try:
            yaml.load(data)
        except yaml.parser.ParserError as why:
            self.yamlh_logger.error("yaml.parser.ParserError: broken data in file.")
            raise yaml.parser.ParserError("{}".format(why))

    def _check_path_for_read(self, path):
        """
        Check path before read

        Raises 'TypeError' if given path lead to a not json file
        Raises 'FileNotFoundError' for obvious reasons
        """
        self._check_file_format(path)
        try:
            handle = open(path)
        except FileNotFoundError as why:
            self.yamlh_logger.error("FileNotFoundError: {}".format(why))
            raise FileNotFoundError("{}".format(why))
        handle.close()

    def read(self, path):
        """
        Read data in yaml file

        :return: result of yaml.load() func
        """
        self._check_path_for_read(path)
        with open(path) as handle:
            data = handle.read()
            self._check_data_in_file(data)
            return yaml.load(data)

    def write(self, path, data):

        """ Write 'data' in yaml file """

        self._check_file_format(path)
        try:
            with open(path, "w") as handle:
                data = yaml.dump(data)
                handle.write(data)
        except PermissionError as why:
            self.yamlh_logger.error("Exception: {}".format(why))
            raise PermissionError("Wrong path: {}".format(why))