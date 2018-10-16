# distutils: sources = strpipe/toolkit/MurmurHash3.cpp


cdef extern from "MurmurHash3.h":  # noqa: E999
    void MurmurHash3_x86_32(
        void *key,  # noqa: E225
        int len,
        unsigned int seed,
        void *out,  # noqa: E225
    )


def consistent_hash(input_str: str, mod_int: int):
    return consistent_hash_in_c(
        input_str=input_str,
        mod_int=mod_int,
        seed=0,
    )


cdef unsigned int consistent_hash_in_c(  # noqa: E999
        str input_str,
        unsigned int mod_int,
        unsigned int seed,
    ):
    cdef unsigned int out
    cdef bytes byte_str = input_str.encode('utf-8')
    MurmurHash3_x86_32(
        <char*> byte_str,  # noqa: E225, E226
        len(byte_str),
        seed,
        &out,  # noqa: E225
    )
    return out % mod_int
