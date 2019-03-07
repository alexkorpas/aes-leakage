import itertools

import numpy as np

from helpers import *


POSSIBLE_SUBKEYS = get_possible_byte_combs()

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

    def obtain_full_private_key(self):
        """Computes the full private key used in AES128 by computing each of
        its 16 subkeys. This is done by constructing a template for each
        possible key and comparing the

        Returns:
            string -- The full 128-bit key.
        """

        private_key = []  # Our best full key gues as a list of binary values.

        # Record n power consumption samples of the full run of the alg.
        # Preferably, each sample is recorded for a different plaintext.
        # All samples should use the same key for encryption.
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
        """Finds the actual used subkey for AES128 encryption at a given point
        in the plaintext. A subkey is found by...
        
        Arguments:
            power_samples {[[int]]} -- The actual power consumption traces at
            the desired point for each plaintext encryption. Given as as a
            list of bit tuples.
            plaintext_block_nr {int} -- Integer to indicate where in the
            plaintext the inspected block starts.
            subkey_byte_index {int} -- Integer to indicate which byte we're
            inspecting in the given block.
        
        Returns:
            [int] -- The best subkey guess as a tuple of 8 integers.
        """
        # Compute Pearson's Correlation Coefficient (PCC) for each possible
        # subkey and use the PCCs to find the best subkey.
        best_subkey = (0, 0, 0, 0, 0, 0, 0, 0)
        best_subkey_pcc = 0

        for subkey_guess in POSSIBLE_SUBKEYS:
            pass

        return best_subkey

    def construct_subkey_templates(self, power_samples):
        # power_samples is a dict with:
        #   k = subkey, v = list of all samples for that subkey
        #   Each of these samples contains a voltage value for each POI.

        # For each possible subkey, store the template as a
        # (means, covariance_matrix) tuple computed with voltage values of
        # that subkey's traces.
        templates = {}

        poi_amnt = len(power_samples[0x00])

        for subkey in POSSIBLE_SUBKEYS:
            traces = power_samples[subkey]

            # Calculate the mean voltage and variance values for each POI
            means = {}
            variances = {}
            for poi_index in range(poi_amnt):
                traces = list(power_samples.values())
                voltages_at_poi = [trace[poi_index] for trace in traces]

                mean_volt = np.mean(voltages_at_poi)
                variance = [(volt - mean_volt)**2 for volt in voltages_at_poi]

                means[poi_index] = mean_volt
                variances[poi_index] = variance
            
            # TODO: Compute cov matrix using either the variances or numpy.cov
            covariance_matrix = None

            # Template = (means, cov_matrix) for this subkey.
            templates[subkey] = (means, covariance_matrix)

    
    def find_points_of_interest(self, power_samples):
        # Find points that have high variance for different encryption runs
        points_of_interest = [] # List of indexes in a power trace

        means = {} # For each possible subkey, store the mean of all its traces
        for subkey in POSSIBLE_SUBKEYS:
            traces = power_samples[subkey]
            
            # TODO: get means and sums of differences to find all POI


    def get_subplaintext(self, plaintext_index, block_nr, subbyte_nr):
        # AES uses blocks of 128 bits. Set the index at the start of the block.
        bit_index = block_nr*128
        bit_index += subbyte_nr*8  # Set the index at the byte under test

        plaintext_bits = self.plaintexts[plaintext_index]
        # Return the byte at this location
        return plaintext_bits[bit_index:bit_index + 8]
