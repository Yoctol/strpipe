

def invert_dictionary(
        input_dict: dict,
        serializable: bool=False,
    ):
    return invert_dictionary_in_c(
        input_dict=input_dict,
        serializable=serializable,
    )


cdef dict invert_dictionary_in_c(
        dict input_dict,
        bint serializable,
    ):
    cdef dict output_dict = {}

    for key, value in input_dict.items():
        if value in output_dict:
            raise KeyError(
                'duplicate value [{}]'.format(value),
            )

        # for serialization
        if serializable:
            output_key = str(value)
        else:
            output_key = value
        output_dict[output_key] = key
    return output_dict
