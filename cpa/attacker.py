import itertools
from numpy import cov, std
from scipy.stats import pearsonr
from power_consumption_modeler import PowerConsumptionModeler


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
        pass


    def obtain_full_private_key(self):
        # TODO: Write method docstring
        # TODO: Remove when method is fully implemented
        raise NotImplementedError

        private_key = [] # List of binary values

        # Record n power consumption samples from a certain point in the alg.
        # Preferably, each sample is recorded for a different plaintext.
        power_samples = []

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
                # TODO: obtain location of plaintext to model with
                block_nr = 1 # The 128-bit plaintext block we're attacking
                byte_nr = -1 # Attacked byte depends on the subkey's location

                subplaintext = self.get_subplaintext(i, block_nr, byte_nr)
                # TODO: Compute the following Hamm dist after subBytes in rnd 1
                modeled_consumption = \
                    self.power_modeler.hamming_dist(subkey_guess, subplaintext)
                
                subkey_guess.append(subkey_guess_consumptions)
            
            pcc = self.pearson_correlation_coeff(power_samples,
                                                 subkey_guess_consumptions)
            if (abs(pcc) > abs(best_subkey_pcc)):
                best_subkey = subkey_guess
                best_subkey_pcc = pcc


    # Call to get PCC that defines correlation between a subkey guess's
    # predicted power consumption and the actual alg's power consumption.
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
        bit_index += subbyte_nr*8 # Set the index at the byte under test

        plaintext_bits = self.plaintexts[plaintext_index]
        # Return the byte at this location
        return plaintext_bits[bit_index:bit_index + 8]
