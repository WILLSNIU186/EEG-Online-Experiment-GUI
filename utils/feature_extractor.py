import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin
# from matlab_functions import run_LPP, run_cICA
# import matlab
import mne


class TemplateMatching(BaseEstimator, ClassifierMixin):
    def __init__(self):
        pass

    def _check_Xy(self, X, y=None):
        """Check input data."""
        if not isinstance(X, np.ndarray):
            raise ValueError("X should be of type ndarray (got %s)."
                             % type(X))
        if y is not None:
            if len(X) != len(y) or len(y) < 1:
                raise ValueError('X and y must have the same length.')
        if X.ndim < 3:
            raise ValueError('X must have at least 3 dimensions.')

    def fit(self, X, y):
        self._check_Xy(X, y)

        self._n_channel = X.shape[1]
        self._classes = np.unique(y)
        self._n_classes = len(self._classes)
        if self._n_classes < 2:
            raise ValueError("n_classes must be >= 2.")
        self._template = dict.fromkeys(self._classes)
        for this_class in self._classes:
            self._template[this_class] = np.mean(X[y == this_class])
        return self

    def transform(self, X):
        self._n_trial = len(X)
        self._n_feature = self._n_channel * self._n_classes
        self._features = np.zeros((self._n_trial, self._n_feature), dtype=float)
        for trial_counter in range(self._n_trial):
            trial = X[trial_counter]
            feature = []
            for this_class in self._classes:
                feature.append(np.diagonal(np.dot(trial, self._template[this_class].T)))
            self._features[trial_counter, :] = np.asarray(feature).flatten()
        return self._features

class Convert2d(BaseEstimator, ClassifierMixin):
    def __init__(self):
        pass
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        new_X = X.reshape(X.shape[0], -1)
        return new_X
        
        
class LPP(BaseEstimator, ClassifierMixin):
    def __init__(self, reduced_dim, gnd, neighbor_mode = 'KNN', k = 5, PCARatio = 1, WeightMode = 'HeatKernel', bLDA=1):
        self._reduced_dim = reduced_dim
        self._neighbor_mode = neighbor_mode
        self._k = k
        self._PCARatio = PCARatio
        self._WeightMode = WeightMode
        self._gnd = gnd
        self._bLDA = bLDA

    def fit(self, X, y = None):
#         print("LPP fit")
        self._my_run_LPP = run_LPP.initialize()
        n_trial = len(X)
#         print('X shape: {}, n_trial: {}'.format(X.shape, n_trial))
        X_reshape = X.reshape(n_trial, -1)
#         print('X reshape: {}'.format(X_reshape.shape))
#         self._reduced_dim = np.linalg.matrix_rank(X_reshape).item()
#         savemat("X_y.mat", {'X': X_reshape.tolist(), 'y' : self._gnd.tolist() })


        self._eig_vector = self._my_run_LPP.run_LPP(matlab.double(X_reshape.tolist()), self._reduced_dim, matlab.double(self._gnd.tolist()), self._neighbor_mode, self._k, self._PCARatio, self._WeightMode, self._bLDA)
        self._eig_vector  = np.asarray(self._eig_vector)
#         print('eig_vector shape: {}'.format(self._eig_vector.shape))
#         print('eig_vector: ', self._eig_vector)
        self._my_run_LPP.terminate()
        return self

    def transform(self, X):
#         print('LPP tranform')
        n_trial = X.shape[0]
        X_reshape = X.reshape(n_trial, -1)
#         print('X reshape: {}'.format(X_reshape.shape))
        new_X = np.dot(X_reshape, self._eig_vector)
        print('new_X : {}'.format(new_X.shape))
        return new_X
#     def predict(self, X):
#         print('LPP prdict')


class cICA(BaseEstimator, ClassifierMixin):
    def __init__(self, ref_ind):
        self._ref_ind = ref_ind
        
    def fit(self, X, y):
        self._my_run_cICA = run_cICA.initialize()
        X_reshape = np.transpose(X, (1, 2, 0))
        time_locked = X_reshape[:, :, y==1]
        data_noise = X_reshape[:, :, y==0]
        self._w = self._my_run_cICA.run_cICA(matlab.double(time_locked.tolist()), 
                                            matlab.double(data_noise.tolist()), 
                                            self._ref_ind)
        self._w = np.asarray(self._w)
        self._my_run_cICA.terminate()
        return self
    
    def transform(self, X):
        X_reshape = np.transpose(X, (1, 2, 0))
        n_trial = X_reshape.shape[2]
        n_sample = X_reshape.shape[1]
        new_X = np.zeros((1, n_sample, n_trial))
#         pdb.set_trace()
        for i in range(n_trial):
            new_X[:, :, i] = np.dot(self._w.T, X_reshape[:, :, i])
        new_X = np.transpose(new_X, (2, 0, 1))
        
        return new_X


class PSD(BaseEstimator, ClassifierMixin):
    def __init__(self, fmin, fmax, n_per_seg=64, n_fft=256, average_method='mean', sfreq=500):
        self._sfreq = sfreq
        self._fmin = fmin
        self._fmax = fmax
        self._n_per_seg = n_per_seg
        self._n_fft = n_fft
        self._average_method = average_method

    def fit(self, X, y = None):
        return self

    def transform(self, X):
        self._n_trial = X.shape[0]
        self._psd_welch, self._freqs = mne.time_frequency.psd_array_welch(X, sfreq=self._sfreq, fmin=self._fmin,
                                                                          fmax=self._fmax, n_fft=self._n_fft,
                                                                          n_per_seg=self._n_per_seg,
                                                                          average=self._average_method)
        temp_X = np.reshape(self._psd_welch, (self._n_trial, -1))
        temp_X -= np.mean(temp_X)
        new_X = (temp_X - np.min(temp_X)) / (np.max(temp_X) - np.min(temp_X))
        return new_X

class SWT(BaseEstimator, ClassifierMixin):
    def __init__(self, wavelet, level):
        self._wavelet = wavelet
        self._level = level
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        n_trial = X.shape[0]
        n_ch = X.shape[1]
        swt_features = []
        for trial in range(n_trial):
            coeffs_list = []
            for ch in range (n_ch):
                coeffs = pywt.swt(data=X[trial,ch,:], wavelet=self._wavelet, level= self._level,  trim_approx=True)
                coeffs_list.append(coeffs)
            swt_features.append(coeffs_list)
        swt_features = np.asarray(swt_features)
        return swt_features
    

class Laplacian(BaseEstimator, ClassifierMixin):
    def __init__(self, channel_names, lap_type = 'large'):
        self._channel_names = channel_names
        self._lap_type = lap_type
        if self._lap_type == 'large':
            self._n_channel = 5
            self._lap_C3_chs = [self._channel_names.index('C3'), self._channel_names.index('T7'),
                                self._channel_names.index('Cz'), self._channel_names.index('F3'),
                                self._channel_names.index('P3')]
            self._lap_Cz_chs = [self._channel_names.index('Cz'), self._channel_names.index('C3'),
                                self._channel_names.index('C4'), self._channel_names.index('Fz'),
                                self._channel_names.index('Pz')]
            self._lap_C4_chs = [self._channel_names.index('C4'), self._channel_names.index('Cz'),
                                self._channel_names.index('T8'), self._channel_names.index('F4'),
                                self._channel_names.index('P4')]
            self._lap_FC1_chs = [self._channel_names.index('FC1'), self._channel_names.index('F3'),
                                 self._channel_names.index('Fz'), self._channel_names.index('C3'),
                                 self._channel_names.index('Cz')]
            self._lap_FC2_chs = [self._channel_names.index('FC2'), self._channel_names.index('Cz'),
                                 self._channel_names.index('Fz'), self._channel_names.index('F4'),
                                 self._channel_names.index('C4')]
            
        elif self._lap_type == 'small':
            self._n_channel = 4
            self._lap_C3_chs = [self._channel_names.index('C3'), self._channel_names.index('C1'),
                                self._channel_names.index('FC3'), self._channel_names.index('C5'),
                                self._channel_names.index('CP3')]
            self._lap_Cz_chs = [self._channel_names.index('Cz'), self._channel_names.index('C1'),
                                self._channel_names.index('C2'), self._channel_names.index('FCz'),
                                self._channel_names.index('CPz')]
            self._lap_C4_chs = [self._channel_names.index('C4'), self._channel_names.index('C2'),
                                self._channel_names.index('C6'), self._channel_names.index('FC4'),
                                self._channel_names.index('CP4')]
            self._lap_FCz_chs = [self._channel_names.index('FCz'), self._channel_names.index('Cz'),
                                 self._channel_names.index('Fz'), self._channel_names.index('FC2'), 
                                 self._channel_names.index('FC1')]
        elif self._lap_type == 'mixed':
            self._n_channel = 7
            self._lap_C3_chs = [self._channel_names.index('C3'), self._channel_names.index('T7'),
                                self._channel_names.index('Cz'), self._channel_names.index('F3'),
                                self._channel_names.index('P3')]
            self._lap_C1_chs = [self._channel_names.index('C1'), self._channel_names.index('C3'),
                                self._channel_names.index('Cz'), self._channel_names.index('FC1'),
                                self._channel_names.index('CP1')]
            self._lap_Cz_chs = [self._channel_names.index('Cz'), self._channel_names.index('C3'),
                                self._channel_names.index('C4'), self._channel_names.index('Fz'),
                                self._channel_names.index('Pz')]
            self._lap_C2_chs = [self._channel_names.index('C2'), self._channel_names.index('C4'),
                                self._channel_names.index('Cz'), self._channel_names.index('FC2'),
                                self._channel_names.index('CP2')]
            self._lap_C4_chs = [self._channel_names.index('C4'), self._channel_names.index('Cz'),
                                self._channel_names.index('T8'), self._channel_names.index('F4'),
                                self._channel_names.index('P4')]
            self._lap_FC1_chs = [self._channel_names.index('FC1'), self._channel_names.index('F3'),
                                 self._channel_names.index('Fz'), self._channel_names.index('C3'),
                                 self._channel_names.index('Cz')]
            self._lap_FC2_chs = [self._channel_names.index('FC2'), self._channel_names.index('Cz'),
                                 self._channel_names.index('Fz'), self._channel_names.index('F4'),
                                 self._channel_names.index('C4')]

    def fit(self, X, y=None):
#         print('LAP fit')
        return self
            
    def transform(self, X):
#         print('LAP transform')
        self._n_trial = X.shape[0]
        self._n_sample = X.shape[2]
        new_X = np.zeros((self._n_trial, self._n_channel, self._n_sample))
        for trial_counter in range(self._n_trial):
            if self._lap_type == 'large':
                self._lap_C3 = self.lap(X[trial_counter, self._lap_C3_chs, :])
                self._lap_Cz = self.lap(X[trial_counter, self._lap_Cz_chs, :])
                self._lap_C4 = self.lap(X[trial_counter, self._lap_C4_chs, :])
                self._lap_FC1 = self.lap(X[trial_counter, self._lap_FC1_chs, :])
                self._lap_FC2 = self.lap(X[trial_counter, self._lap_FC2_chs, :])
                new_trial = np.r_[self._lap_C3, self._lap_Cz, self._lap_C4, self._lap_FC1, self._lap_FC2]

            elif self._lap_type == 'small':
                self._lap_C3 = self.lap(X[trial_counter, self._lap_C3_chs, :])
                self._lap_Cz = self.lap(X[trial_counter, self._lap_Cz_chs, :])
                self._lap_C4 = self.lap(X[trial_counter, self._lap_C4_chs, :])
                self._lap_FCz = self.lap(X[trial_counter, self._lap_FCz_chs, :])
                new_trial = np.r_[self._lap_C3, self._lap_Cz, self._lap_C4, self._lap_FCz]
            elif self._lap_type == 'mixed':
                self._lap_C3 = self.lap(X[trial_counter, self._lap_C3_chs, :])
                self._lap_Cz = self.lap(X[trial_counter, self._lap_Cz_chs, :])
                self._lap_C4 = self.lap(X[trial_counter, self._lap_C4_chs, :])
                self._lap_FC1 = self.lap(X[trial_counter, self._lap_FC1_chs, :])
                self._lap_FC2 = self.lap(X[trial_counter, self._lap_FC2_chs, :])
                self._lap_C1 = self.lap(X[trial_counter, self._lap_C1_chs, :])
                self._lap_C2 = self.lap(X[trial_counter, self._lap_C2_chs, :])
                new_trial = np.r_[self._lap_C3, self._lap_Cz, self._lap_C4, self._lap_FC1, self._lap_FC2, self._lap_C1,
                                  self._lap_C2]
            new_X[trial_counter, :, :] = new_trial
        return new_X

    def lap(self, data_pre_lap):
        lap_filter = [-1 / 4] * 4
        lap_filter.insert(0, 1)  # center channel is channel 0
        lap_filter = np.asarray(lap_filter)
        temp = np.reshape(lap_filter, (1, 5))
        data_lap_filtered = np.dot(temp, data_pre_lap)
        return data_lap_filtered



class DSP(BaseEstimator, ClassifierMixin):
    '''
    X: (n_epochs, n_channels, n_times)
    y: class label
    '''
    def __init__(self, theta):
        self.theta = theta


    def fit(self,X,y):
        self._check_Xy(X, y)
        self.class_labels = np.unique(y)
        self.n_classes = self.class_labels.shape[0]
        self.n_ch = X.shape[1]
        self.n_sample = X.shape[2]

        self.S_w = self.scatter_within(X,y)
        self.S_b = self.scatter_between(X, y)
        self.S_w = self.regularization()
        eig_vals, eig_vecs = np.linalg.eig(np.linalg.inv(self.S_w).dot(self.S_b))
        self.eig_vals = eig_vals.real
        eig_vecs = eig_vecs.real
        sorted_order = np.argsort(np.abs(self.eig_vals))[::-1]
        self.eig_vecs = eig_vecs[:, sorted_order]

    def transform(self, X):
        w0 = - np.dot(self.eig_vecs.T, self.overall_mean)
        n_trial = X.shape[0]
        X_new = np.zeros((n_trial, self.n_ch, self.n_sample))
        for idx in range(n_trial):
            X_new[idx, :, :] = np.dot(self.eig_vecs.T, X[idx, :, :]) + w0
        return X_new

    def _check_Xy(self, X, y=None):
        """Check input data."""
        if not isinstance(X, np.ndarray):
            raise ValueError("X should be of type ndarray (got %s)."
                             % type(X))
        if y is not None:
            if len(X) != len(y) or len(y) < 1:
                raise ValueError('X and y must have the same length.')
        if X.ndim < 3:
            raise ValueError('X must have at least 3 dimensions.')

    def regularization(self):
        I = np.identity(self.n_ch)
        S_within = (1-self.theta) * self.S_w + self.theta * I
        return S_within


    def comp_mean_vectors(self, X, y):
        mean_vectors = []
        for cl in self.class_labels:
            mean_vectors.append(np.mean(X[y == cl], axis=0))
        return mean_vectors

    def scatter_within(self, X, y):
        mean_vectors = self.comp_mean_vectors(X, y)

        S_W = np.zeros((self.n_ch, self.n_ch))

        for cl, mv in zip(self.class_labels, mean_vectors):
            class_sc_mat = np.zeros((self.n_ch, self.n_ch))
            for trial in X[y == cl]:
                diff = trial - mv
                class_sc_mat += np.dot(diff, diff.T)
            S_W += class_sc_mat
        return S_W

    def scatter_between(self, X, y):
        self.overall_mean = np.mean(X, axis=0)
        mean_vectors = self.comp_mean_vectors(X, y)
        S_B = np.zeros((self.n_ch, self.n_ch))
        for i, mean_vec in enumerate(mean_vectors):
            n = X[y == i, :].shape[0]
            diff = mean_vec - self.overall_mean
            S_B += n * np.dot(diff, diff.T)
        return S_B























