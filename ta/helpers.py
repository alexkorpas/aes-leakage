import itertools


def get_possible_byte_combs():
        """Computes a list of all possible combinations of a bit sequence of
        length 8 by using the itertools module's built-in method for this.

        Returns:
            [[int]] -- A list of all byte combinations, where each combination
            is a tuple that consists of 8 integers.
        """
        return list(itertools.product([0, 1], repeat=8))


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
