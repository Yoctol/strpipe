

def invert_dictionary(input_dict: dict):
    return invert_dictionary_in_c(input_dict=input_dict)


cdef dict invert_dictionary_in_c(
        dict input_dict,
    ):
    cdef dict output_dict = {}

    for key, value in input_dict.items():
        if value in output_dict:
            raise KeyError(
                'duplicate value [{}]'.format(value),
            )
        output_dict[value] = key
    return output_dict
