def bit_tuples_to_string(bit_tuples):
    """Converts a given list of bit tuples to a single string of those bits.

    Arguments:
        bit_tuples {[[int]]} -- The list of bit tuples, of which all the bits
        should be concatenated in the returned string.

    Returns:
        string -- The string representation of all the given bits.
    """
    strings = [bit_tuple_to_string(bit_tup) for bit_tup in bit_tuples]
    return "".join(strings)


def bit_tuple_to_string(bits):
    """Converts a given list or tuple of bits to its string representation.

    Arguments:
        bits {[int]} -- List of bits to concatenate in the string.

    Returns:
        string -- The string representation of the given bits.
    """
    return "".join([str(bit) for bit in bits])


def bytes_to_bits(byte_decimals):
    bits = []
    for dec in byte_decimals:
        bit_str = bin(dec)[2:].zfill(8)
        for bit in bit_str:
            bits.append(bit)
