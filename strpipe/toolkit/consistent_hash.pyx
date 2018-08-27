from sklearn.utils import murmurhash3_32


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
    return murmurhash3_32(input_str, seed=0) % mod_int
