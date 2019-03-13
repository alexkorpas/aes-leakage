import itertools
from numpy import cov, std
from scipy.stats import pearsonr
from power_consumption_modeler import PowerConsumptionModeler
from helpers import *


class Attacker:

    def __init__(self, plaintexts):
        """Initiates an Attacker object, which will execute a Correlation
        Power Analysis Attack on an AES implementation by having it encrypt
        a given set of plaintexts.

        Arguments:
            plaintexts { [[int]] } -- The plaintext binary sequences that will
            be encrypted to obtain power samples from the algorithm. Each
            sequence is a tuple (or list) of decimal numbers that represent
            bytes.
        """
        self.plaintexts = []
        # Convert each plaintext to a list of bits
        for plaintext in plaintexts:
            self.plaintexts.append(bytes_to_bits(plaintext))

        self.power_modeler = PowerConsumptionModeler()

    def obtain_full_private_key(self, power_samples):
        """Computes the full private key used in AES128 by computing each of
        its 16 subkeys. This is done with power samples produced by encryption
        of known plaintexts.

        Arguments:
            power_samples { [[float]] } - A list of power traces where each
            trace is a list of floats that represents the obtained output
            for one plaintext encryption. Each sample is assumed to use the
            same encryption key.

        Returns:
            string -- The full 128-bit key.
        """

        private_key = []  # List of binary values

        block_nr = 0  # It doesn't matter which plaintext block we look at

        final_subkeys = []  # 16 subkeys of 8 bits each
        for subkey_nr in range(0, 16):
            subkey = self.find_used_subkey(power_samples, block_nr, subkey_nr)
            final_subkeys.append(subkey)

        private_key = list(itertools.chain.from_iterable(final_subkeys))

        return bit_tuple_to_string(private_key)

    def find_used_subkey(self, power_samples, plaintext_block_nr,
                         subkey_byte_index):
        """Finds the actual used subkey for AES128 encryption at a given point
        in the plaintext. This point should coincide with the point at which
        each power sample was taken. A subkey is found by modeling the power
        consumptions for each of 2^8 subkey guesses and checking which of
        the guesses correlates the most with the actual power consumptions.
        
        Arguments:
            power_samples { [[float]] } -- The actual power consumption traces
            at the desired point for each plaintext encryption. Given as a list
            of samples where each sample is a list of floats.
            plaintext_block_nr {int} -- Integer to indicate where in the
            plaintext the inspected block starts.
            subkey_byte_index {int} -- Integer to indicate which byte we're
            inspecting in the given block.
        
        Returns:
            [int] -- The best subkey guess as a tuple of 8 bits.
        """
        # Compute Pearson's Correlation Coefficient (PCC) for each possible
        # subkey and use the PCCs to find the best subkey.
        possible_subkeys = self.get_possible_byte_combs()
        best_subkey = (0, 0, 0, 0, 0, 0, 0, 0)
        best_subkey_pcc = 0

        for subkey_guess in possible_subkeys:
            # For each plaintext, compute the modeled consumption for
            # encrypting it with one of the guessed subkeys.
            subkey_guess_consumptions = []

            for i in range(len(power_samples)):
                # Define the location we're attacking in the full plaintext
                block_nr = plaintext_block_nr
                byte_nr = subkey_byte_index
                subplaintext = self.get_subplaintext(i, block_nr, byte_nr)

                # Compute the Hamm dist after subBytes in round 1
                sbox_simulation = \
                    apply_sbox(xor_bit_tuples(subplaintext, subkey_guess))
                modeled_consumption = \
                    self.power_modeler.hamming_weight(sbox_simulation)

                subkey_guess_consumptions.append(modeled_consumption)

            pcc = self.pearson_correlation_coeff(power_samples,
                                                 subkey_guess_consumptions)

            # Set this guess ass the best subkey if it correlates better on
            # average over all power traces.
            if (abs(pcc) > abs(best_subkey_pcc)):
                best_subkey = subkey_guess
                best_subkey_pcc = pcc

        return best_subkey

    def pearson_correlation_coeff(self, actual_consumptions,
                                  modeled_consumptions):
        """Computes the Pearson Correlation Coefficient (PCC) between a set of
        obtained power consumptions and the modeled power consumptions for a
        certain subkey guess.

        Arguments:
            actual_consumptions {[int]} -- A list of integers, each of which
            represents the power consumption of a run of the encryption alg
            with a certain plaintext.
            modeled_consumptions {[int]} -- A list of modeled power
            consumptions (as Hamming distances), each of which represents
            the predicted consumption of using a guessed subkey for a run of
            the encryption alg with a certain plaintext.

        Returns:
            float -- The PCC between the given sets of power consumptions. The
            value is in the range [-1, 1], where 1 means the actual
            consumption always increases when the modeled consumption
            increases, and -1 means they always decrease at the same time.
        """
        # PCC = cov(AC, MC)/stddev(AC)*stddev(MC)
        (pcc, _) = pearsonr(actual_consumptions, modeled_consumptions)
        return pcc

    def get_possible_byte_combs(self):
        """Computes a list of all possible combinations of a bit sequence of
        length 8 by using the itertools module's built-in method for this.

        Returns:
            [[int]] -- A list of all byte combinations, where each combination
            is a tuple that consists of 8 integers.
        """
        return list(itertools.product([0, 1], repeat=8))

    def extract_subbytes_trace_points(self, power_trace):
        """Given a list of points from an AES128 power trace, this method
        locates and extracts the points that correspond to the subBytes step
        in the first round of the algorithm.

        Returns:
            [float] -- A subset of the given points' values that correspond to
            the consumption values during the subBytes step in the first round.
        """
        return []

    def get_subplaintext(self, plaintext_index, block_nr, subbyte_nr):
        # AES uses blocks of 128 bits. Set the index at the start of the block.
        bit_index = block_nr*128
        bit_index += subbyte_nr*8  # Set the index at the byte under test

        plaintext_bits =  \
            [int(char) for char in self.plaintexts[plaintext_index]]
        # Return the byte at this location
        return plaintext_bits[bit_index:bit_index + 8]
