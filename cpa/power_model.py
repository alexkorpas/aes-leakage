class PowerModel:
    
    def __init__(self):
        pass

    
    def hamming_dist(self, reference, data):
        """Computes the Hamming distance for two given bit strings by counting
        the amount of different bits between them.
        
        Arguments:
            reference {string} -- A binary string representing the reference
            power consumption state.
            data {string} -- A binary string representing the power 
            consumption data to be compared against the reference consumption.

        Returns:
            {int} The amount of differing bits between reference and data.
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

    
    def compute_consumed_power(self, ham_dist, a, b):
        """Computes the consumed power W, which is proportional to scalar a
        and base consumption b.
        
        Arguments:
            ham_dist {int} -- The Hamming distance computed between two bit
            strings.
            a {int} -- The scalar value by which the Hamming distance is
            scaled in the power model.
            b {int} -- The base power consumption value in the model, which
            encapsulates noise, independent background consumption, etc.

        Returns:
            {int} The consumed power over a certain time period defined by
            bit strings of which the Hamming distance is given.
        """
        return a*ham_dist + b

