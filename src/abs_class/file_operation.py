
import os
from pathlib import Path
import numpy as np

class FileOperationClass():
    def _check_file_exist(
        self,
        file_path: Path | None = None,
    ):
        assert os.path.exists(file_path), str(file_path) + " is not found"

    def _open_new_file(
        self,
        prefix: str,
        extention: str,
    ):
        filename = "{}{}".format(prefix, extention)
        for i in range(1,1001):
            try:
                fo = open(filename, 'x')
                break
            except FileExistsError:
                filename = "{}_{}{}".format(prefix, i, extention)
            assert i != 1000, "Failed to make file"
        return fo

class ArrayClass():
    def _check_array_shape(
        self,
        array: np.ndarray,
        array_name: str,
        shape: tuple | None = None,
        ndim: int | None = None,
    ):
        assert shape is not None or ndim is not None, \
            "shape and ndim not defined"
        if shape is not None:
            assert array.shape == shape, array_name + " shape is wrong"
        if ndim is not None:
            assert array.ndim == ndim, array_name + " ndim is wrong"

    def _check_array(
        self,
        array: np.ndarray,
        array_name: str,
    ):
        print("Array \'{}\' information".format(array_name))
        print("    ndim   :  {}".format(array.ndim))
        print("    shape  :  {}".format(array.shape))
        print("    values  :")
        if   array.ndim == 1:  print(array[:5])
        elif array.ndim == 2:  print(array[:5, :5])
        elif array.ndim == 3:  print(array[:5, :5, :5])



