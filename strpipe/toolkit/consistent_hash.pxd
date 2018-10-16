cdef extern from "MurmurHash3.h":  # noqa: E999
    void MurmurHash3_x86_32(
        void *key,  # noqa: E225
        int len,
        unsigned int seed,
        void *out,  # noqa: E225
    )


cdef unsigned int consistent_hash_in_c(  # noqa: E999
        str input_str,
        unsigned int mod_int,
        unsigned int seed,
    )
