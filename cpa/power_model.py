class PowerModel:
    
    def __init__(self):
        pass

    
    def hamming_dist(self, reference, data):
        """Computes the Hamming distance for two given bitstrings by counting
        the amount of different bits between them.
        
        Arguments:
            reference {string} -- A binary string representing the reference
            power consumption state.
            data {string} -- A binary string representing the power 
            consumption data to be compared against the reference consumption.
        """
        if len(reference) != len(data):
            raise Exception("Unequal lengths between compared bitstrings.")

        dist = 0
        for i in len(data):
            ref_bit = reference[i]
            data_bit = data[i]
            if ref_bit != data_bit:
                dist += 1
        return dist
