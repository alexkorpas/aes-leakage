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
            plaintexts {[[int]]} -- The plaintext binary sequences that will
            be encrypted to obtain power samples from the algorithm. Each
            sequence is a tuple (or list) of bits.
        """
        self.plaintexts = plaintexts
        self.power_modeler = PowerConsumptionModeler()

    def obtain_full_private_key(self):
        # TODO: Write method docstring

        private_key = []  # List of binary values

        # Record n power consumption samples from a certain point in the alg.
        # Preferably, each sample is recorded for a different plaintext.
        power_samples = []

        block_nr = 0  # It doesn't matter which plaintext block we look at

        final_subkeys = []  # 16 subkeys of 8 bits each
        for subkey_nr in range(0, 16):
            subkey = self.find_used_subkey(power_samples, block_nr, subkey_nr)
            final_subkeys.append(subkey)

        private_key = list(itertools.chain.from_iterable(final_subkeys))

        return bit_tuple_to_string(private_key)

    def find_used_subkey(self, power_samples, plaintext_block_nr,
                         subkey_byte_index):
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

                # Compute the following Hamm dist after subBytes in round 1
                modeled_consumption = \
                    self.power_modeler.hamming_dist(subkey_guess, subplaintext)

                subkey_guess.append(subkey_guess_consumptions)

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

    def get_subplaintext(self, plaintext_index, block_nr, subbyte_nr):
        # AES uses blocks of 128 bits. Set the index at the start of the block.
        bit_index = block_nr*128
        bit_index += subbyte_nr*8  # Set the index at the byte under test

        plaintext_bits = self.plaintexts[plaintext_index]
        # Return the byte at this location
        return plaintext_bits[bit_index:bit_index + 8]
