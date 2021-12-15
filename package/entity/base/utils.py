'''
utilities for real time processing
'''
import numpy as np
from sklearn.cross_decomposition import CCA

class SSVEPCCAAnalysis:
    """Vanilla Canonical Correlation Analysis for SSVEP/SSMVEP detection"""
    def __init__(self, fs, data_len, target_freqs, num_harmonics=1):
        """
        Args:
            s_rate (int): Sampling rate of EEG signal.
            data_len (float): Detection window length in seconds.
            target_freqs (list): List of target frequencies in Hz.
            num_harmonics (int): Number of harmonics to be considered, eg. 1, 2, 3.
        """
        self.fs = fs
        self.data_len = data_len
        self.target_freqs = target_freqs
        self.num_harmonics = num_harmonics
        self.sinusoidal_templates = self._init_sinusoidal_templates()
        self.cca = CCA(n_components=1)

    def _init_sinusoidal_templates(self):
        time_axis = np.linspace(0, self.data_len, int(self.fs * self.data_len))
        templates_dictionary = dict()
        for freq in self.target_freqs:
            sinusoidal_reference_template = list()
            for harmonic_num in range(self.num_harmonics):
                sinusoidal_reference_template.append(np.sin(2 * np.pi * harmonic_num * freq * time_axis))
                sinusoidal_reference_template.append(np.cos(2 * np.pi * harmonic_num * freq * time_axis))
            templates_dictionary[freq] = np.array(sinusoidal_reference_template).T
        
        return templates_dictionary

    def apply_cca(self, test_data):
        """Apply CCA analysis to EEG data and return scores for each target frequency
        Args:
            test_data (np.array): EEG sample window of shape (num_samples, num_channels).
        Returns:
            list of correlation coefficients.
        """
        corr_coeffcients = list()
        for target_freq in self.sinusoidal_templates.keys():
            transformed_signal, transformed_template = self.cca.fit_transform(test_data, self.sinusoidal_templates[target_freq])
            corr_coeffcients.append(np.corrcoef(transformed_signal.T, transformed_template.T)[0, 1])
        
        return corr_coeffcients