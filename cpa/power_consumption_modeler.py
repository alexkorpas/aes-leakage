class PowerConsumptionModeler:
    SUBKEY_HAMM_WEIGHTS = [bin(i).count("1") for i in range(0, 256)]

    def __init__(self):
        pass

    def hamming_dist(self, reference, data):
        """Computes the Hamming distance for two given bit strings by counting
        the amount of different bits between them. The Hamming distance will
        be proportional to the actual power consumption of going from the
        "reference" state to the "data" state.

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

    def hamming_weight(self, data):
        """Computes the Hamming weight of a given integer. The HW is the
        amount of bits set to 1.

        Arguments:
            data {int} -- The integer of which the Hamming weight will be
            computed.

        Returns:
            int -- The Hamming weight of the given binary string.
        """
        return bin(data).count("1")

    def subkey_hamm_weight(self, subkey):
        """Returns the Hamming weight of a given integer in the range [0..255]
        by performing a lookup in a preprocessed Hamming weight table.

        Arguments:
            subkey {int}} -- The subkey of which we would like to get
            the Hamming weight.

        Returns:
            int -- The Hamming weight of the given subkey.
        """
        return self.SUBKEY_HAMM_WEIGHTS[subkey]

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
