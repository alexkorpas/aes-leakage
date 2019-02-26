def bit_tuples_to_string(bit_tuples):
    strings = [bit_tuple_to_string(bit_tup) for bit_tup in bit_tuples]
    return "".join(strings)


def bit_tuple_to_string(bits):
    return "".join([str(bit) for bit in bits])