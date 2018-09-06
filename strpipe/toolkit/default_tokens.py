class DefaultTokens:

    sos = '<SOS>'
    eos = '<EOS>'
    unk = '<UNK>'
    pad = '<PAD>'
    nul = '\0'  # For Cython classes to use as Python's 'None'.

    @classmethod
    def list_all_tokens(cls):
        tokens = {}
        for vname, val in cls.__dict__.items():
            if (not vname.startswith("__")) and (
                    isinstance(val, str)):
                tokens[vname] = val
        return tokens
