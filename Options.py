from os.path import join


class Options(object):
    """Class that manages files available for selection feature
    It uses a dictionary as its main data structure
    """
    def __init__(self, parent_path, filename_list):
        """Constructor
        Parameters:
            - parent_path: str representing a valid path to the file
            - filename_list: list[str] full filename without parent path
        """
        self._dicc = {}
        self._current_n = 1
        self.add_list(parent_path, filename_list)

    def insert(self, parent_path, filename):
        """Inserts an record into the options
        Parameters:
            - parent_path: str representing a valid path to the file
            - filename: str representing the full filename without parent path
        """
        exec_path = join(parent_path, filename)
        self._dicc[self._current_n] = (exec_path, filename)
        self._current_n += 1
    
    def get(self, option_number):
        """Gets a record of the dictionary
        Parameters:
            - option_number: int, which record number to retrieve
        """
        if 0< option_number < self._current_n:
            return self._dicc[option_number]
        else:
            message = error("Option is not valid")
            raise Exception(message)

    def add_list(self, parent_path, filename_list):
        """Adds a list of files into the dictionary
        Parameters:
            - parent_path: str representing a valid path to the file
            - filename_list: list[str] full filename without parent path
        """
        for filename in filename_list:
            self.insert(parent_path, filename)

    def __str__(self):
        """String representation of objects dictionary
        """
        res = ''
        for key, (exec_path, file_name) in self._dicc.items():
            res += '{:3d}    {}\n'.format(key, file_name)
        return res