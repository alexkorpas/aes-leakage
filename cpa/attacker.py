import itertools
import numpy as np
from scipy.stats import pearsonr
from power_consumption_modeler import PowerConsumptionModeler
from helpers import *

import time


class Attacker:
    POSSIBLE_SUBKEYS = range(256)  # Integers [0..255]

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
        self.plaintexts = plaintexts

        self.power_modeler = PowerConsumptionModeler()

        # For each of the 16 subkeys, store a "subkey guess correlation" dict.
        # Such a dict stores the correlation coefficient for each subkey guess.
        self.subkey_corr_coeffs = {}
        for i in range(16):
            self.subkey_corr_coeffs[i] = {}

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
            [int] -- The full 128-bit key as a list of 16 integers.
        """
        private_key = []  # List of binary values

        block_nr = 0  # It doesn't matter which plaintext block we look at

        final_subkeys = []  # 16 subkeys of 8 bits each, as integers
        for subkey_nr in range(0, 16):
            print(f"Starting to obtain subkey {subkey_nr}!")
            subkey = self.find_used_subkey(power_samples, block_nr, subkey_nr)
            print(f"Found subkey nr {subkey_nr}: {subkey}")
            final_subkeys.append(subkey)

        return final_subkeys

    def find_used_subkey(self, power_samples, plaintext_block_nr,
                         subkey_byte_index):
        """Finds the actual used subkey for AES128 encryption at a given point
        in the plaintext. A subkey is found by modeling the power consumptions
        for each of 2^8 subkey guesses and checking which of the guesses
        correlates the most with the actual power consumptions.

        Arguments:
            power_samples { [[float]] } -- The actual power consumption traces
            at the desired point for each plaintext encryption. Given as a list
            of samples where each sample is a list of floats.
            plaintext_block_nr {int} -- Integer to indicate where in the
            plaintext the inspected block starts.
            subkey_byte_index {int} -- Integer to indicate which byte we're
            inspecting in the given block.

        Returns:
            int -- The best subkey guess as an integer.
        """
        # Compute Pearson's Correlation Coefficient (PCC) for each possible
        # subkey and use the PCCs to find the best subkey.
        best_subkey = 0
        best_subkey_pcc = 0

        for subkey_guess in self.POSSIBLE_SUBKEYS:
            # print(f"Trying subkey {subkey_guess} for PT byte {subkey_byte_index}...")

            # For each plaintext, compute the modeled consumption for
            # encrypting it with one of the guessed subkeys.
            subkey_guess_consumptions = []

            # Compute the simulated subkey consumptions for each plaintext
            for i in range(len(self.plaintexts)):
                # Define the location we're attacking in the full plaintext
                subplaintext = self.plaintexts[i][subkey_byte_index]

                # Compute the Hamm dist after subBytes in round 1
                sbox_simulation = apply_sbox(subplaintext ^ subkey_guess)
                modeled_consumption = \
                    self.power_modeler.subkey_hamm_weight(sbox_simulation)

                subkey_guess_consumptions.append(modeled_consumption)

            # Find out the correlation between the modeled consumptions and the
            # actual consumptions by computing correlation values for each
            # subkey guess. 
            numpoint = len(power_samples[0])
            # For each point, keep track of the sum and both denominators in
            # the correlation function computed as
            # r_i,j = sumnum / np.sqrt(sumden1 * sumden2).
            sumnum = np.zeros(numpoint)
            sumden1 = np.zeros(numpoint)
            sumden2 = np.zeros(numpoint)

            numtraces = len(power_samples)

            modeled_cons_mean = np.mean(subkey_guess_consumptions,
                                        dtype=np.float64)
            traces_mean = np.mean(power_samples, axis=0, dtype=np.float64)

            # Compute the correlation for all trace points at the same time.
            # Build up the correlation value over time by iterating over all
            # power traces.
            for trace_num in range(0, numtraces):
                modeled_cons_diff = \
                    subkey_guess_consumptions[trace_num] - modeled_cons_mean
                actual_cons_diff = power_samples[trace_num] - traces_mean

                sumnum = sumnum + modeled_cons_diff*actual_cons_diff
                sumden1 = sumden1 + modeled_cons_diff*modeled_cons_diff
                sumden2 = sumden2 + actual_cons_diff*actual_cons_diff

            pcc = max(abs(sumnum / np.sqrt(sumden1 * sumden2)))

            # For this subkey attempt, store the correlation of this subkey
            # guess with the actual consumptions to compute guessing entropy.
            self.subkey_corr_coeffs[subkey_byte_index][subkey_guess] = pcc

            # Compare this subkey's correlation coeff with that of the others.
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
        # PCC = np.cov(AC, MC)/stddev(AC)*stddev(MC)
        # (pcc, _) = pearsonr(actual_consumptions, modeled_consumptions)

        # Initialize arrays &amp; variables to zero
        numpoint = 5000
        sumnum = np.zeros(numpoint)
        sumden1 = np.zeros(numpoint)
        sumden2 = np.zeros(numpoint)

        # Mean of hypothesis
        modeled_cons_mean = np.mean(modeled_consumptions, dtype=np.float64)

        # Mean of all points in trace
        meant = np.mean(actual_consumptions, axis=0, dtype=np.float64)

        hdiff = (modeled_consumptions[tnum] - modeled_cons_mean)
        tdiff = actual_consumptions[tnum, :] - meant

        sumnum = sumnum + (hdiff*tdiff)
        sumden1 = sumden1 + hdiff*hdiff
        sumden2 = sumden2 + tdiff*tdiff

        pcc = sumnum / np.sqrt(sumden1 * sumden2)

        return pcc

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
