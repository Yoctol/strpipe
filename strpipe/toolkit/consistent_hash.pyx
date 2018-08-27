# distutils: language = c++
from libcpp.string cimport string  # noqa: E999

import hashlib
import pickle


def consistent_hash(
        input_str: str,
        mod_int: int,
    ) -> int:
    return consistent_hash_in_cpp(
        input_str=input_str,
        mod_int=mod_int,
    )


cdef long int consistent_hash_in_cpp(  # noqa: E999
        str input_str,
        long int mod_int,
    ):
    cdef long int output_int
    cdef string byte_str = pickle.dumps(input_str)

    hash_obj = hashlib.sha256()
    hash_obj.update(byte_str)
    output_int = int(hash_obj.hexdigest(), 16) % mod_int
    del hash_obj
    return output_int
