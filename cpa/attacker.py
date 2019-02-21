import itertools
from numpy import cov, std
from scipy.stats import pearsonr

class Attacker:

    def __init__(self, plaintexts):
        """Initiates an Attacker object, which will execute a Correlation
        Power Analysis Attack on an AES implementation by having it encrypt
        a given set of plaintexts.
        
        Arguments:
            plaintexts {[string]} -- The plaintext strings that will be
            encrypted to obtain power samples from the algorithm.
        """
        self.plaintexts = plaintexts
        pass


    def obtain_full_private_key(self):
        raise NotImplementedError

        private_key = [] # List of binary values

        # Record n power consumption samples from a certain point in the alg.
        # Preferably, each sample is recorded for a different plaintext.
        power_samples = []

        possible_subkeys = self.get_possible_byte_combs()
        for subkey_guess in possible_subkeys:
            modeled_consumption = 


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
