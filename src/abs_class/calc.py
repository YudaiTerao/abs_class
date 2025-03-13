
from pathlib import Path
import numpy as np
from abs_class import FileOperationClass, ArrayClass

class CalcClass(ArrayClass, FileOperationClass):
    def write_meshgrid_dat(
        self,
        values: np.ndarray,
        prefix: str,
        extention: str,
     ):
        self._check_array_shape(values, 'meshgrid_values', ndim=3)
        fo = self._open_new_file(prefix, extention)

        shape = values.shape[1:]
        lines = np.stack([ np.ravel(v) for v in values ]).T

        print("{0[0]:>8} {0[1]:>8}".format(shape), file=fo)
        for line in lines:
            string = ""
            for param in line: string += " {0:>10.10f}".format(param)
            print(string, file=fo)
        fo.close()

