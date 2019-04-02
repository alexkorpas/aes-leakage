import numpy as np

from helpers import *
from scipy.stats import multivariate_normal


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

        # For each subkey, store the means of each point over all traces
        self.point_means = {}
        for i in range(256):
            self.point_means[i] = {}

        # Save the points of interest once they're computed
        self.pois = []

        # Store the subkey guess templates for easy access
        self.templates = {}

        # For each of the 16 subkeys, store a "subkey guess correlation" dict.
        # Such a dict stores the correlation coefficient for each subkey guess.
        self.subkey_corr_coeffs = {}
        for i in range(16):
            self.subkey_corr_coeffs[i] = {}

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

        return private_key

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

    def find_points_of_interest(self, power_samples):
        # Find points that have high variance for different encryption runs

        point_amnt = len(power_samples[0][0])
        means = {} # For each possible subkey, store the mean of all its traces

        # For each subkey, compute the mean for each point over its traces
        for subkey in POSSIBLE_SUBKEYS:
            traces = power_samples[subkey]

            for point_i in range(point_amnt):
                point_i_volts = [trace[point_i] for trace in traces]
                mean_i = np.mean(point_i_volts)

                self.point_means[subkey][point_i] = mean_i
        
        # Compute sum of differences for every i with every j
        sums_of_diffs = {}
        for point_i in range(point_amnt):
            sum_of_diffs = 0

            for subkey1 in POSSIBLE_SUBKEYS:
                mean1 = self.point_means[subkey1][point_i]

                for subkey2 in POSSIBLE_SUBKEYS:
                    mean2 = self.point_means[subkey2][point_i]

                    sum_of_diffs += abs(mean1 - mean2)
            sums_of_diffs[point_i] = sum_of_diffs
        
        pois = self.extract_pois_from_sums_of_diffs(sums_of_diffs)
        return pois
        
    def extract_pois_from_sums_of_diffs(self, sums_of_diffs):
        amnt_of_pois = 10
        radius = 50

        # Select points of interest, which are the points with the highest
        # sum of differences over all traces.
        pois = []
        for i in range(amnt_of_pois):
            # Get the point index with the maximum sum of difference.
            # Do this by finding the max of a pair (= an item) with the
            # operator.itemgetter(1) method, which selects the maximum by
            # looking at item 1 of the pair instead of at item 0.
            max_sod_poi = max(stats.items(), key=operator.itemgetter(1))[0]
            pois.append(max_sod_poi)

            # Remove neighbouring points from the points to look at
            for j in range (max_sod_poi - radius, max_sod_poi + radius):
                if j not in sums_of_diffs:
                    continue

                del(sums_of_diffs[j])

        self.pois = pois
        return pois

    def construct_subkey_templates(self, power_samples):
        # power_samples is a dict with:
        #   k = subkey, v = list of all samples for that subkey
        #   Each of these samples contains a voltage value for each POI.

        # For each possible subkey, store the template as a
        # (means, covariance_matrix) tuple computed with voltage values of
        # that subkey's traces.
        templates = {}

        # Only create templates for the points of interest
        pois = self.find_points_of_interest(power_samples)
        power_samples = [power_samples[i] for i in pois]

        poi_amnt = len(power_samples[0][0])

        for subkey in POSSIBLE_SUBKEYS:
            # Only look at the traces where this subkey was used
            traces = power_samples[subkey]
            trace_amnt = len(traces)
            
            # Compute covariance matrix manually for each i,j point combination
            cov_mat = np.zeros(shape=(poi_amnt, poi_amnt), dtype=float)

            # Calculate the mean voltage and variance values for each POI
            means = {}
            variances = {}
            for poi_i in range(poi_amnt):
                poi_i_volts = [trace[poi_i] for trace in traces]

                mean_i = np.mean(poi_i_volts)
                variance = compute_variance(traces, trace_amnt, poi_i_volts,
                                            mean_i)

                means[poi_i] = mean_i
                variances[poi_i] = variance

                for poi_j in range(poi_amnt):
                    if poi_i == poi_j:
                        cov_mat[poi_i, poi_j] = variances[poi_i]
                        continue
                    
                    # Early stop for symmetric values in the array
                    if cov_mat[poi_j, poi_i] != 0.0:
                        cov_mat[poi_i, poi_j] = cov_mat[poi_j, poi_i]
                    
                    poi_j_volts = [trace[poi_j] for trace in traces]
                    mean_j = np.mean(poi_j_volts)

                    # Compute covariance between points i and j
                    cov_mat[poi_i, poi_j] = compute_covariance(
                        traces, trace_amnt, poi_i_volts, poi_j_volts,
                        mean_i, mean_j
                    )

            # Template = (means, cov_matrix) for this subkey.
            templates[subkey] = (means, cov_mat)
        
        self.templates = templates
        return templates

    def execute_template_attack(self, traces, subkey_byte_index):
        # For each subkey guess, store the combined probability density
        # function's result over all traces.
        subkey_guess_pdfs = np.zeros(256)

        # For each trace, store the probability density function 

        # Only look at te points of interest.
        poi_traces = []
        for trace in traces:
            trace_at_pois = [trace[i] for i in self.pois]
            poi_traces.append(trace_at_pois)

            for subkey_guess in POSSIBLE_SUBKEYS:
                # Compute the normal dist for the given subkey guess's template
                normal_dist = multivariate_normal(self.templates[subkey_guess])

                # Use the normal dist to compute the PDF values for this trace.
                # This value represents the likelihood of this trace occurring
                # for the given subkey. Compute the log of it to negate float
                # precision errors when computing the product of PDF values.
                trace_logpdf = normal_dist.logpdf(trace_at_pois)
                subkey_guess_pdfs[subkey_guess] += trace_logpdf
        
        # Store the sk guess PDF values for the subkey we're currently finding 
        subkey_corr_coeffs[subkey_byte_index] = subkey_guess_pdfs

        # Our best guess is the one with the highest PDF product for each POI
        best_subkey = subkey_guess_pdfs.argmax()
        return best_subkey
