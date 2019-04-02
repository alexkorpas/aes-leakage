import numpy as np

from collections import defaultdict
from helpers import *
from power_consumption_modeler import PowerConsumptionModeler
from scipy.stats import multivariate_normal


POSSIBLE_SUBKEYS = range(256)  # Integers [0..255]
POSS_BYTE_HAMMWEIGHTS = range(9)


class Attacker:

    def __init__(self, plaintexts, keys):
        """Initiates an Attacker object, which will execute a Template Attack
        on an AES implementation by having it encrypt known plaintexts with
        known keys.

        Arguments:
            plaintexts { [[int]] } -- The plaintext byte sequences that will
            be encrypted to obtain power samples from the algorithm. Each
            sequence is a tuple (or list) of decimal numbers that represent
            bytes.
            keys { [[int]] } -- The keys with which each respective
            plaintext was encrypted.
        """
        self.plaintexts = plaintexts
        self.keys = keys

        self.power_modeler = PowerConsumptionModeler()

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

    def obtain_full_private_key(self, power_samples):
        """Computes the full private key used in AES128 by computing each of
        its 16 subkeys. This is done with power samples produced by encryption
        of known plaintexts.

        Arguments:
            power_samples { {[int]: [float]} } - A dictionary of power traces
            where the key is the 16 byte plaintext that was used in the trace.
            A trace is a list of floats that represents the obtained output
            for one plaintext encryption. Each trace may use a different
            encryption key.

        Returns:
            [int] -- The full 128-bit key as a list of 16 integers.
        """
        private_key = []  # Our best full key gues as a list of binary values.

        block_nr = 0  # It doesn't matter which plaintext block we look at

        # Assume the templates have already been created
        final_subkeys = []  # 16 subkeys of 8 bits each
        for subkey_nr in range(0, 16):
            traces = None  # TODO: Sort traces by subkey location
            subkey = self.find_used_subkey_with_templates(traces, subkey_nr)
            final_subkeys.append(subkey)

        return private_key

    def find_points_of_interest(self, power_samples):
        # Find points that have high variance for different encryption runs

        point_amnt = len(power_samples[0][0])
        means = {}  # For each possible subkey, store the mean of its traces

        # For each HW, compute the mean for each point over its traces
        for hw in POSS_BYTE_HAMMWEIGHTS:
            traces = power_samples[hw]

            for point_i in range(point_amnt):
                point_i_volts = [trace[point_i] for trace in traces]
                mean_i = np.mean(point_i_volts)

                self.point_means[hw][point_i] = mean_i

        # Compute sum of differences for every i with every j
        sums_of_diffs = {}
        for point_i in range(point_amnt):
            sum_of_diffs = 0

            for hw1 in POSS_BYTE_HAMMWEIGHTS:
                mean1 = self.point_means[hw1][point_i]

                for hw2 in POSS_BYTE_HAMMWEIGHTS:
                    mean2 = self.point_means[hw2][point_i]

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
            for j in range(max_sod_poi - radius, max_sod_poi + radius):
                if j not in sums_of_diffs:
                    continue

                del(sums_of_diffs[j])

        self.pois = pois
        return pois

    def group_traces_by_hammweight(self, power_samples):
        """Groups a given list of traces by simulating SBOX functionality for
        each trace and computing the Hamming weight for the simulated SBOX
        value. The traces are grouped by this value.

        Arguments:
            power_samples { [[float]] } -- A list of traces, where each trace
            is a list of floats.

        Returns:
            [[float]] -- The grouped traces, presented as 9 lists (1 for each
            possible byte Hamming weight) of traces. Each trace is still a list
            of floats.
        """
        # Assume keys[i] and plaintexts[i] correspond to power_samples[i]
        traces_amnt = len(power_samples)

        # Group traces by Hamming weight of each possible subkey
        grouped_traces = [[] for _ in range(9)]

        # TODO: Extend simulation and grouping to all bytes
        # Compute SBOX simulation for the 9th byte of each plaintext/key combo.
        sbox_sim = lambda subkey, pt_byte: apply_sbox(subkey ^ pt_byte)
        sbox_sims = [sbox_sim(self.plaintexts[i][9], self.keys[i][9]) 
                     for i in range(traces_amnt)]
        sim_hamm_weights = \
            [self.power_modeler.subkey_hamm_weight[sim] for sim in sbox_sims]

        # For each trace, categorise it by the Hamming weight value of its SBOX
        # simulation value.
        for i in range(traces_amnt):
            hw = sim_hamm_weights[i]
            grouped_traces[hw].append(power_samples[i])

        return grouped_traces

    def construct_hammweight_templates(self, power_samples):
        """Constructs and stores power consumption templates, represented as
        (means, covmat) tuples, based on a given set of power traces. The
        traces may use different key and plaintext combinations.

        Arguments:
            power_samples { [[float]] } -- A list of traces, where each trace
            is a list of floats.

        Returns:
            [ ([float], [[float]]) ] -- A dictionary where the key is a Hamming
            weight and the value is a template. A template is a tuple that
            consists of a list of mean values (1 for each POI) over all traces
            corresponding to that HW, and a 2D covariance matrix that
            describes the variance in values between each POI.
        """
        # Categorise the traces by Hamming weight, so we can construct
        # an accurate template for each HW.
        power_samples = self.group_traces_by_hammweight(power_samples)

        # For each possible subkey, store the template as a
        # (means, covariance_matrix) tuple computed with voltage values of
        # that subkey's traces.
        templates = {}

        # Only create templates for the points of interest
        pois = self.find_points_of_interest(power_samples)
        power_samples = [power_samples[i] for i in pois]

        poi_amnt = len(power_samples[0][0])

        for hammweight in range(9):
            # Only look at the traces of which the SBOX sim has this HW
            traces = power_samples[hammweight]
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

            # Template = (means, cov_matrix) for this HW.
            templates[hammweight] = (means, cov_mat)

        self.templates = templates
        return templates

    def find_used_subkey_with_templates(self, traces, plaintexts,
                                        subkey_byte_i):
        """Finds the actual used subkey for AES128 encryption at a given point
        in the plaintext, using a given set of attack traces. A subkey is found
        by comparing the given traces to templates of each possible subkey.

        Arguments:
            traces { [float] } -- The actual power consumption traces
            corresponding to the given subkey byte location. Given as a list of
            floats.
            subkey_byte_i {int} -- Integer to indicate which byte we're
            inspecting in a given block. Assume we're always looking at the
            first block.

        Returns:
            int -- The best subkey guess as an integer.
        """
        plaintexts_amnt = len(self.plaintexts)

        # For each subkey guess, store the combined probability density
        # function's result over all traces.
        subkey_guess_pdfs = np.zeros(256)

        for i in range(len(traces)):
            trace = traces[i]
            pt = plaintexts[i]
            trace_at_pois = [trace[i] for i in self.pois]

            for subkey_guess in POSSIBLE_SUBKEYS:
                # Simulate the power consumption for usage of this key by
                # simulating the SBOX operation and computing the Hamm weight.
                sbox_sim = pt[subkey_byte_i] ^ subkey_guess[subkey_byte_i]
                sim_hw = \
                    self.power_modeler.subkey_hamm_weight(apply_sbox(sbox_sim))

                # Compute the normal dist for the computed HW's template
                (means, covmat) = self.templates[sim_hw]
                normal_dist = multivariate_normal(means, covmat)

                # Use the normal dist to compute the PDF values for this trace.
                # This value represents the likelihood of this trace occurring
                # for the given subkey. Compute the log of it to negate float
                # precision errors when computing the product of PDF values.
                trace_logpdf = normal_dist.logpdf(trace_at_pois)
                subkey_guess_pdfs[subkey_guess] += trace_logpdf

        # Store the sk guess PDF values for the subkey we're currently finding
        subkey_corr_coeffs[subkey_byte_i] = subkey_guess_pdfs

        # Our best guess is the one with the highest PDF product over all POI
        best_subkey = subkey_guess_pdfs.argmax()
        return best_subkey
