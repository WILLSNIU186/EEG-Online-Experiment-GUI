from package.entity.base.mrcp_buffer import MRCPBuffer
from package.entity.base.ssvep_buffer import SSVEPBuffer
from package.entity.base.scope import Scope
from package.entity.base.filter import Filter

class OnlineTest():
    def onClicked_pushButton_test(self):
        self.bp_filter_full = Filter(low_cut=0.05, hi_cut=40, order=2, sf=500, n_chan=31)
        self.bp_filter_low = Filter(low_cut=0.05, hi_cut=5, order=2, sf=500, n_chan=31)
        # self.EEGNET_buffer = MRCPBuffer(self, window_stride=0.1, window_size=2, buffer_size=10,
        #                               l_filter=self.bp_filter_full, filter_type='bpf',
        #                               ica_path=r'model/sub146_ica_005_40.fiff', downsample=100,
        #                               model_path=r'model/EEGNET_test_fold_0', model_type='keras', model_name='EEGNET')
        
        self.EEGNET_buffer = SSVEPBuffer(self, window_stride=0.1, window_size=2, buffer_size=10,
                                      l_filter=self.bp_filter_full, filter_type='bpf',
                                      ica_path=None, downsample=None,
                                      model_path=None, model_type=None, model_name='cca')
        # self.SVM_buffer = MRCPBuffer(self, window_stride=0.1, window_size=2, buffer_size=10,
        #                               l_filter=self.bp_filter_low, filter_type='bpf',
        #                               ica_path=r'model/sub146_ica.fiff', downsample=100,
        #                               model_path=r'model/svm_test_fold_0.pkl', model_type='sklearn', model_name='SVM')
        # self.ETSSVM_buffer = MRCPBuffer(self, window_stride=0.1, window_size=2, buffer_size=10,
        #                               l_filter=self.bp_filter_full, filter_type='bpf',
        #                               ica_path=r'model/sub146_ica_005_40.fiff', downsample=100,
        #                               model_path=r'model/etssvm_test_fold_0.pkl', model_type='sklearn', model_name='ETSSVM')

        self.EEGNET_scope = Scope(self.EEGNET_buffer)
        # self.SVM_scope = Scope(self.SVM_buffer)
        # self.ETSSVM_scope = Scope(self.ETSSVM_buffer)

        self.EEGNET_buffer.start_timer()
        # self.SVM_buffer.start_timer()
        # self.ETSSVM_buffer.start_timer()

        self.EEGNET_scope.start_timer(20)
        # self.SVM_scope.start_timer(20)
        # self.ETSSVM_scope.start_timer(20)

        self.EEGNET_buffer.mrcp_test_win.show()
        # self.SVM_buffer.mrcp_test_win.show()
        # self.ETSSVM_buffer.mrcp_test_win.show()

    def onClicked_pushButton_scope_mrcp(self):
        self.EEGNET_scope.show_win()
        # self.SVM_scope.show_win()
        # self.ETSSVM_scope.show_win()

    def change_window_stride(self):
        self.EEGNET_buffer.update_window_stride(float(self.ui.lineEdit_window_stride_mrcp.text()))
        # self.SVM_buffer.update_window_stride(float(self.ui.lineEdit_window_stride_mrcp.text()))
        # self.ETSSVM_buffer.update_window_stride(float(self.ui.lineEdit_window_stride_mrcp.text()))