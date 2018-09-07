# distutils: language = c++


cdef class BaseOp:
    """Base class for Ops

    Sub-classes should implement `fit`, `transform`, and `inverse_transform`.

    Attributes:
        input_type: input type of data to transform
        output_type: output type of transformed data
    """

    @staticmethod
    cdef fit(input):
        """Generate the **state** of the Op

        A state is some data dependent information
        generating by input data.

        Returns:
            state

        """
        pass

    @staticmethod
    cdef transform(state, input):
        """Transform input data

        Transform input data to certain form which meets the output_type
        defined in `__init__`.

        Returns:
            transformed data
            tx_info: information required by `inverse_transform`

        """
        pass

    @staticmethod
    cdef inverse_transfrom(state, input, meta):
        """Restore input data to its original form

        Returns:
            restored data

        """
        pass
