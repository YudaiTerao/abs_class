
import time
from mpi4py import MPI
import numpy as np

import itertools
from wannier_utils.hamiltonian import HamR, HamK

class ParallelClass():
    def __init__(self):
        self.comm = MPI.COMM_WORLD
        self.rank = self.comm.Get_rank()
        self.nproc = self.comm.Get_size()

    @classmethod
    def return_node_info(cls):
        return cls().comm, cls().rank, cls().nproc

    @classmethod
    def parallel_info(cls, func):
        def wrapper(self, *args, **kwargs):
            start_time = time.time()
            func(self, *args, **kwargs)
            end_time = time.time()

            # メモリ使用量の取得
            process = psutil.Process(os.getpid())
            mem_info = process.memory_info()

            if self.rank == 0:
                print(f"Program: {os.path.basename(__file__)}")
                print(f"Rank: {parallel.rank}")
                print(f"Number of processes: {parallel.nproc}")
                print(f"Time taken: {end_time - start_time} seconds")
                print(f"Memory used: {mem_info.rss / 1024 ** 2} MB\n")
        return wrapper

    def array_split_scatter(
        self,
        array: np.ndarray,
     ):
        # ランク0のプロセスでarrayを分割する
        if self.rank == 0:
            _array_assigned = np.array_split(array, self.nproc)
        else:
            _array_assigned = None
        print(self.rank)

        # 分割したarrayを、ランク0のプロセスから他のプロセスに分散する
        return self.comm.scatter(_array_assigned, root=0)

    def array_gather_connect(
        self,
        array: np.ndarray,
    ):
        # 各プロセスのarrayをランク0のプロセスに集める
        array_list = self.comm.gather(array, root=0)
        if self.rank == 0:
            return np.concatenate(array_list, axis=0)
        else:
            return None

    def parallel_eigval(
        self,
        ham_r: HamR,
        klist: np.ndarray,
    ) -> np.ndarray:
        """対角化を分散する。

        Args:
            ham_r (HamR or MagRotation): Real space Hamiltonian object.
            klist: List of kpoints in (klen, 3) array.

        Returns:
            eigval: List of eigvals in (num_wann, klen) array.
        """
        _k_assigned = self.array_split_scatter(klist)
        _eigval_assigned = self.diag_ham(ham_r, _k_assigned)
        eigval = self.array_gather_connect(_eigval_assigned)
        if self.rank == 0:
            return eigval
        else:
            return None

    def diag_ham(self, ham_r: HamR, klist: np.ndarray) -> np.ndarray:
        eigval = np.zeros((len(klist), ham_r.num_wann), dtype=np.float_)
        for i, k in enumerate(klist):
            ham_k = HamK(ham_r, k, diagonalize=True)
            eigval[i] = ham_k.ek
        return eigval

    def get_klist(self, nk1, nk2, nk3):
        k123 = [np.arange(nk) / float(nk) for nk in [nk1, nk2, nk3]]
        klist = list(itertools.product(k123[0], k123[1], k123[2]))
        return np.array(klist)


