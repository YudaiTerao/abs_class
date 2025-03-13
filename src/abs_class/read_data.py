
import re
import numpy as np
from pathlib import Path
from abs_class.file_operation import FileOperationClass


class ReadDataClass(FileOperationClass):
    def _get_lines(
        self,
        file_path: Path,
        comment_marker: str = '!',
        lower: bool = False,
        delete_end_comment: bool = False,
        delete_in_space: bool = False,
    ):
        self._check_file_exist(file_path)
        with open(file_path, 'r') as fn: lines = fn.readlines()

        #コメント行の消去
        if comment_marker != '':
            lines = [ re.sub(fr'^{comment_marker}.*$', '', l) for l in lines ]
        #行末コメントの消去
            if delete_end_comment == True:
                lines = [ l.split('!')[0] for l in lines ]

        #行頭行末のスペース, カンマ, コロン, 改行を消去
        lines = [ self._delete_head_end_space(l) for l in lines ]

        #行内スペースの消去
        if delete_in_space == True:
            lines = [ re.sub(r'\s', '', l) for l in lines ]

        #linesの小文字化
        if lower == True:
            lines = [ l.lower() for l in lines ]
        return lines

    def _get_param(
        self,
        keyword: str,
        lines: list,
        judge_lines: list,
        delimiter: str = '=',
        default_value = None,
        dtype: type = float
    ):
        param = None
        for line, j_line in zip(lines, judge_lines):
            if re.match(fr'^\s*{keyword}\s*{delimiter}.+$', j_line):
                assert param == None, keyword + " is defined more than once"
                assert len(line.split(delimiter)) == 2, keyword +' value is not correct'
                param = dtype(line.split(delimiter)[1])

        if param is None:
            if default_value is not None:
                param = default_value
            else: 
                return None
        return param

    def _get_table_param(
        self,
        keyword: str,
        lines: list,
        judge_lines: list,
        end_keyword: str | None = None,
        column_num: int | None = None,
        param_row: list | None = None,
        skip_column: int = 0,
        get_unit: bool = False,
        dtype: type = float,
    ):
        param_lines = None
        for i, j_line in enumerate(judge_lines):
            if re.match(fr'^\s*{keyword}\s*$', j_line):
                assert param_lines == None, keyword + " is defined more than once"

                if column_num is None and end_keyword is None: 
                    assert re.match(r'^[0-9]+\s*$', lines[i+1]), \
                           "column_num of " + keyword + " not found"
                    column_num = int(lines[i+1])
                    if skip_column == 0: skip_column = 1

                elif end_keyword is not None:
                    for j, j_ln in enumerate(judge_lines[i + 1 + skip_column:]):
                        if re.match(fr'^\s*{end_keyword}\s*$', j_ln):
                            if column_num is None: 
                                column_num = j
                            elif column_num is not None:
                                assert column_num == j, \
                                       "The column_num of " + keyword + " is wrong"
                        assert i + j + 2 <= len(lines), \
                               "The end of \'" + keyword + "\' is not found"

                assert i + 1 + skip_column + column_num < len(lines), \
                       keyword + " column is too short"
                param_lines = lines[ i+1+skip_column : i+1+skip_column+column_num ]
                if get_unit == True: 
                    unit = self._delete_head_end_space(lines[i+1]).lower()

        if param_lines is None: return None

        if param_row is not None:
            params = []
            for pl in param_lines:
                param = []
                for prow in param_row:
                    if prow[1] == -1:
                        pm = [ dtype(p) for p in pl.split()[prow[0]:] ]
                    else:
                        pm = [ dtype(p) for p in pl.split()[prow[0]:prow[1]] ] 
                    param.append(pm)
                params.append(param)

        else:
            params = [ [ dtype(p) for p in l.split() ] for l in param_lines ]

        if get_unit == True: return params, unit
        else:                return params

    def _delete_head_end_space(
        self,
        string: str,
    ):
        return re.sub('^\s*[\,\.]?', '', re.sub('[\,\.]?\s*$', '', string))

    def convert_cell_to_kcell(
        self,
        cell: np.ndarray,
    ):
        assert  type(cell) is np.ndarray, "convert_cell_to_kcell: type error"
        assert  cell.shape == (3, 3), \
                "convert_cell_to_kcell: cell shape is wrong"
        #----- kcellの計算 -----#
        #kcell : K空間の基底ベクトル
        #kcellは実空間の基底ベクトルの逆行列の転置*2pi
        kcell = 2 * np.pi * (np.linalg.inv(cell).T)
        return kcell

    def convert_kpath_to_coord(
        self,
        kpath: np.ndarray,
        kcell: np.ndarray,
    ):
        assert  type(kpath) is np.ndarray and type(kcell) is np.ndarray, \
                "convert_kpoints_to_length: type error"
        assert  kpath.ndim == 3 \
                and kpath.shape[1] == 2 \
                and kcell.ndim == 2 \
                and kcell.shape[1] == kpath.shape[2], \
                "convert_kpoints_to_length: kpoints or kcell shape is wrong"

        coord = np.zeros(len(kpath) + 1, dtype = np.float32)
        for i, kp in enumerate(kpath):
            k_diff = kp[1] - kp[0]
            coord[i+1] = coord[i] + np.linalg.norm(k_diff)
        return coord

    def write_labelinfo(
        self,
        prefix = 'none',
        extention = '_band.labelinfo.dat'
    ):
        fo = self._open_new_file(prefix, extention)
        try:
            if self.nmesh is not None: nmesh = self.nmesh
            else: nmesh = 100
        except:
            nmesh = 100
        for i, kn in enumerate(self.kpath_label):
            print("{0:<8}  {1:>6d}  {2:>4.10f}    {3[0]:>4.10f}  {3[1]:>4.10f}  {3[2]:>4.10f}".format(kn, 1 + i * nmesh, self.kpath_label_coord[i], self.kpath[i]), file=fo)
        fo.close()


