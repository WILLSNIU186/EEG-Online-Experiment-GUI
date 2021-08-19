# -*- coding: utf-8 -*-
from __future__ import print_function, division, unicode_literals

"""
Jiansheng Niu
2021

"""

DEBUG_TRIGGER = False  # TODO: parameterize
NUM_X_CHANNELS = 16  # TODO: parameterize
import sys
import numpy as np
import pyqtgraph as pg
import multiprocessing as mp
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QDialog
from PyQt5 import QtCore
from configparser import RawConfigParser
from pycnbi import logger
from twisted.internet import task
from pycnbi.stream_receiver.stream_receiver import StreamReceiver

from package.views.main_GUI.control_switches.eye_tracker import EyeTracker
from package.views.layouts import main_layout, subject_layout, eye_tracker_layout
from package.router.router import Router
from package.entity.edata.variables import Variables
from package.entity.edata.utils import Utils
from package.entity.base.participant import Participant
from package.entity.base.event import Event
from package.entity.base.protocol import Protocol
from package.entity.base.bad_epoch import BadEpoch
from package.entity.base.buffer import Buffer
from package.entity.base.mrcp_buffer import MRCPBuffer
from package.entity.base.scope import Scope

from package.entity.base.filter import Filter

from package.views.main_GUI.control_switches.main_switch import MainSwitch
from package.views.main_GUI.control_switches.record_switch import RecordSwitch
from package.views.main_GUI.control_switches.scope_switch import ScopeSwitch
from package.views.main_GUI.control_switches.task_switch import TaskSwitch

from package.views.main_GUI.exp_protocol_design.exp_protocol import ExpProtocol
from package.views.main_GUI.exp_protocol_design.sequence_manager import SequenceManager
from package.views.main_GUI.exp_protocol_design.ssvep_exp_protocol import SSVEPExpProtocol
from package.views.main_GUI.exp_protocol_design.task_manager import TaskManager
from package.views.main_GUI.exp_protocol_design.cue_manager import CueManager

from package.views.main_GUI.online_monitor.bad_epoch_monitor import BadEpochMonitor
from package.views.main_GUI.online_monitor.MRCP_extractor import MRCPExtractor

from package.views.main_GUI.oscilloscope.channel_filter import ChannelFilter
from package.views.main_GUI.oscilloscope.channel_scale_manager import ChannelScaleManager
from package.views.main_GUI.oscilloscope.channel_selector import ChannelSelector
from package.views.main_GUI.oscilloscope.event_plot import EventPlot

from package.views.main_GUI.subject_info.subject_info import SubjectInfo

from package.views.main_GUI.timer.run_timer import RunTimer
from package.views.main_GUI.timer.GUI_timer import GUITimer

from package.views.main_GUI.online_testing.online_test import OnlineTest
import pdb


class MainView(QMainWindow, SubjectInfo, TaskManager, SequenceManager, ExpProtocol, \
               ChannelScaleManager, ChannelSelector, ChannelFilter, BadEpochMonitor, MRCPExtractor, MainSwitch, \
               ScopeSwitch, RecordSwitch, TaskSwitch, EventPlot, SSVEPExpProtocol, EyeTracker, RunTimer, GUITimer, \
               CueManager, OnlineTest):
    """
    MainView class controls the GUI frontend interaction
    """

    def __init__(self, amp_name, amp_serial, state=mp.Value('i', 1), queue=None):
        """
        Initialize experimenter window GUI and subject view window GUI

        :amp_name: amplifier name passed from LSL
        :amp_serial: amplifier serial passed from LSL
        """
        super(MainView, self).__init__()
        self.router = Router()
        self.ui = main_layout.Ui_MainWindow()
        self.ui.setupUi(self)

        self.window = QMainWindow()
        self.SV_window = subject_layout.Ui_SV()
        self.SV_window.setupUi(self.window)

        self.eye_tracker_dialog = QDialog()
        self.eye_tracker_window = eye_tracker_layout.Ui_Dialog()
        self.eye_tracker_window.setupUi(self.eye_tracker_dialog)

        # redirect_stdout_to_queue(logger, queue, 'INFO')
        logger.info('Viewer launched')

        self.amp_name = amp_name
        self.amp_serial = amp_serial
        self.state = state
        self.init_all()

        self.ui.widget_mrcp_extractor.show()
        self.participant = Participant()
        self.cue_list = []
        self.cue_image = None
        self.cue_sound = None

        self.trial_image = None
        self.trial_sound = None
        self.protocol = Protocol()
        self.trial_counter = 0
        self.cue_counter = 0
        self.event_obj = Event()
        self.cue_change_flag = True
        self.bad_epoch = BadEpoch()


        self.raw = Variables.get_stream_player_raw()
        # pdb.set_trace()
        self.event_counter = 0
        self.prev_event_counter = -1
        # self.ui.widget_mrcp_extractor.setYRange(-100, 100)
        #
        # self.scope = Scope(window_stride=0.1, window_size=2, buffer_size=10,
        #                                 filter=self.bp_filter, filter_type='bpf', ica=True)
        # self.scope_buffer.start_timer()
        # self.scope = Scope(self, self.scope_buffer)

        # self.b1 = Buffer(window_stride=0.1, window_size=2, buffer_size=10, filter=self.bp_filter, filter_type='bpf')
        # self.b2 = Buffer(window_stride=0.1, window_size=2, buffer_size=10, filter=self.bp_filter, filter_type='bpf')
        # self.b1.start_timer()
        # self.b2.start_timer()

    def init_all(self):
        """
        Initialize specialized functions inside GUI
        """
        self.init_config_file()
        self.init_loop()
        self.init_panel_GUI()
        self.init_event_functions()
        self.init_SV_GUI()
        self.init_scope_GUI()
        self.init_timer()  # timer for scope refreshing
        self.init_Runtimer()  # timer for record, train and test
        self.init_eye_tracker()

    def init_config_file(self):
        """
        Initialize config file
        """
        self.scope_settings = RawConfigParser(allow_no_value=True, inline_comment_prefixes=('#', ';'))
        if (len(sys.argv) == 1):
            self.show_channel_names = 0
            self.device_name = ""
        else:
            if (sys.argv[1].find("gtec") > -1):
                self.device_name = "gtec"
                self.show_channel_names = 1
            elif (sys.argv[1].find("biosemi") > -1):
                self.device_name = "biosemi"
                self.show_channel_names = 1
            elif (sys.argv[1].find("hiamp") > -1):
                self.device_name = "hiamp"
                self.show_channel_names = 1
            else:
                self.device_name = ""
                self.show_channel_names = 0
        # self.scope_settings.read(os.getenv("HOME") + "/.scope_settings.ini")
        self.scope_settings.read('.scope_settings.ini')

    def init_loop(self):
        """
        Initialize loop related variables like StreamReceiver and self.eeg
        """
        self.updating = False
        logger.info("init_loop runs")
        self.sr = StreamReceiver(window_size=5, buffer_size=10,
                                 amp_serial=Variables.get_amp_serial(), amp_name=Variables.get_amp_name())
        srate = int(self.sr.sample_rate)
        # n_channels= self.sr.channels

        # 12 unsigned ints (4 bytes)
        ########## TODO: assumkng 32 samples chunk => make it read from LSL header
        data = ['EEG', srate, ['L', 'R'], 32, len(self.sr.get_channels()),
                0, self.sr.get_trigger_channel(), None, None, None, None, None]

        logger.info('Trigger channel is %d' % self.sr.get_trigger_channel())

        self.config = {'id': data[0], 'sf': data[1], 'labels': data[2],
                       'samples': data[3], 'eeg_channels': data[4], 'exg_channels': data[5],
                       'tri_channels': data[6], 'eeg_type': data[8], 'exg_type': data[9],
                       'tri_type': data[10], 'lbl_type': data[11], 'tim_size': 1,
                       'idx_size': 1}

        self.tri = np.zeros(self.config['samples'])
        self.last_tri = 0
        self.eeg = np.zeros(
            (self.config['samples'], self.config['eeg_channels']),
            dtype=np.float)
        self.exg = np.zeros(
            (self.config['samples'], self.config['exg_channels']),
            dtype=np.float)
        self.ts_list = []
        self.ts_list_tri = []

    def init_event_functions(self):
        """
        Initialize event listeners for widgets in GUI
        """
        # Control buttons
        self.ui.pushButton_Main_switch.clicked.connect(self.onClicked_button_Main_switch)
        self.ui.pushButton_start_SV.clicked.connect(self.onClicked_button_start_SV)
        self.ui.pushButton_scope_switch.clicked.connect(self.onClicked_button_scope_switch)
        self.ui.pushButton_rec.clicked.connect(self.onClicked_button_rec)
        # self.ui.pushButton_start_train.clicked.connect(self.onClicked_button_train)
        # self.ui.pushButton_start_test.clicked.connect(self.onClicked_button_test)

        # Subject information
        self.ui.pushButton_save.clicked.connect(self.onClicked_button_save_subject_information)

        # Experimental protocol
        self.ui.pushButton_define_task_done.clicked.connect(self.onClicked_button_define_task_done)
        self.ui.pushButton_define_task_add.clicked.connect(self.onClicked_button_define_task_add)
        self.ui.pushButton_create_sequence.clicked.connect(self.onClicked_button_create_sequence)
        self.ui.pushButton_randomize.clicked.connect(self.onClicked_button_randomize)
        self.ui.toolButton_choose_image_task.clicked.connect(self.onClicked_toolButton_choose_image_task)
        self.ui.toolButton_choose_sound_task.clicked.connect(self.onClicked_toolButton_choose_sound_task)
        self.ui.pushButton_experimental_protocol_finish.clicked.connect(self.onClicked_experimental_protocol_finish)
        self.ui.pushButton_save_protocol.clicked.connect(self.onClicked_button_save_protocol)
        self.ui.toolButton_load_protocol.clicked.connect(self.onClicked_toolButton_load_protocol)
        self.ui.toolButton_choose_image_cue.clicked.connect(self.onClicked_toolButton_choose_image_cue)
        self.ui.toolButton_choose_sound_cue.clicked.connect(self.onClicked_toolButton_choose_sound_cue)
        self.ui.pushButton_define_cue_add.clicked.connect(self.onClicked_button_define_cue_add)
        self.ui.pushButton_define_cue_done.clicked.connect(self.onClicked_button_define_cue_done)

        # Oscilloscope
        self.ui.comboBox_scale.activated.connect(self.onActivated_combobox_scale)
        self.ui.spinBox_time.valueChanged.connect(self.onValueChanged_spinbox_time)
        self.ui.spinBox_downsample_ratio.valueChanged.connect(self.onValueChanged_downsample_ratio)

        self.ui.checkBox_car.stateChanged.connect(self.onActivated_checkbox_car)
        self.ui.checkBox_bandpass.stateChanged.connect(self.onActivated_checkbox_bandpass)
        self.ui.checkBox_notch.stateChanged.connect(self.onActivated_checkbox_notch)

        self.ui.pushButton_bp.clicked.connect(self.onClicked_button_bp)
        self.ui.pushButton_apply_notch.clicked.connect(self.onClicked_button_notch)

        self.ui.table_channels.itemSelectionChanged.connect(self.onSelectionChanged_table)
        self.ui.table_channels.doubleClicked.connect(self.onDoubleClicked_channel_table)
        self.ui.pushButton_update_channel_name.clicked.connect(self.onClicked_button_update_channel_name)
        self.ui.table_channels.viewport().installEventFilter(self)

        # SSVEP
        self.ui.pushButton_ssvep_task.clicked.connect(self.onClicked_pushButton_ssvep_task)

        # eye tracker
        self.ui.pushButton_open_eye_tracker_ui.clicked.connect(self.onClicked_pushButton_open_eye_tracker_ui)

        # MRCP tab
        self.ui.pushButton_temp_clear.clicked.connect(self.onClicked_button_temp_clear)
        self.ui.pushButton_temp_mean.clicked.connect(self.onClicked_button_temp_mean)
        self.ui.pushButton_temp_view.clicked.connect(self.onClicked_button_temp_view)
        self.ui.pushButton_temp_remove.clicked.connect(self.onClicked_button_temp_remove)

        self.ui.pushButton_test.clicked.connect(self.onClicked_pushButton_test)
        self.ui.pushButton_scope_switch_mrcp.clicked.connect(self.onClicked_pushButton_scope_mrcp)
        self.ui.lineEdit_window_stride_mrcp.textChanged.connect(self.change_window_stride)

    def init_panel_GUI(self):
        """
        Initialize experimenter GUI
        """
        # Tabs
        self.ui.tab_experimental_protocol.setEnabled(False)
        self.ui.tab_subjec_information.setEnabled(False)
        # self.ui.tab_Oscilloscope.setEnabled(False)
        self.ui.tab_experiment_type.setEnabled(False)

        # Button
        self.init_task_name_table()
        self.init_cue_name_table()
        self.ui.groupBox_sequence_manager.setEnabled(False)
        self.ui.pushButton_save_protocol.setEnabled(False)

        # Event management tab
        self.event_timestamp_list = []
        # self.init_task_event_number_table()
        # self.event_list = []
        # Button
        self.event_file_path = ""
        self.mrcp_template_file_path = ""
        self.raw_eeg_file_path = ""
        self.raw_mrcp_file_path = ""
        self.subject_file_path = ""

        # Oscilloscope
        self.ui.comboBox_scale.setCurrentIndex(4)
        self.ui.checkBox_notch.setChecked(True)
        # self.ui.checkBox_car.setChecked(
        #     int(self.scope_settings.get("filtering", "apply_car_filter")))
        # self.ui.checkBox_bandpass.setChecked(
        #     int(self.scope_settings.get("filtering", "apply_bandpass_filter")))
        self.ui.pushButton_apply_notch.setEnabled(True)
        self.ui.doubleSpinBox_lc_notch.setEnabled(True)
        self.ui.doubleSpinBox_hc_notch.setEnabled(True)

        # initialize channel selection panel in main view GUI
        self.channels_to_show_idx = []
        idx = 0
        for y in range(0, 4):
            for x in range(0, NUM_X_CHANNELS):
                if idx < self.config['eeg_channels']:
                    # self.table_channels.item(x,y).setTextAlignment(QtCore.Qt.AlignCenter)
                    self.ui.table_channels.item(x, y).setSelected(True)  # Qt5
                    # self.table_channels.setItemSelected(self.table_channels.item(x, y), True) # Qt4 only
                    self.channels_to_show_idx.append(idx)
                else:
                    self.ui.table_channels.setItem(x, y,
                                                   QTableWidgetItem("N/A"))
                    self.ui.table_channels.item(x, y).setFlags(
                        QtCore.Qt.NoItemFlags)
                    self.ui.table_channels.item(x, y).setTextAlignment(
                        QtCore.Qt.AlignCenter)
                idx += 1
        self.ui.table_channels.verticalHeader().setStretchLastSection(True)
        self.ui.table_channels.horizontalHeader().setStretchLastSection(True)
        self.channel_to_scale_row_index = -1
        self.channel_to_scale_column_index = -1

        self.selected_channel_row_index = 0
        self.selected_channel_column_index = 0
        self.single_channel_scale = 1

        # # BP initialization
        # self.apply_bandpass = 1
        # if (self.apply_bandpass):
        #     self.ui.doubleSpinBox_lp.setValue(40.0)
        #     self.ui.doubleSpinBox_hp.setValue(1.0)
        #     self.ui.doubleSpinBox_lp.setMinimum(0)
        #     self.ui.doubleSpinBox_lp.setMaximum(self.sr.sample_rate / 2 - 0.1)
        #     self.ui.doubleSpinBox_lp.setSingleStep(1)
        #     self.ui.doubleSpinBox_hp.setMinimum(0)
        #     self.ui.doubleSpinBox_hp.setMaximum(self.sr.sample_rate / 2 - 0.1)
        #     self.ui.doubleSpinBox_hp.setSingleStep(1)
        #     self.ui.pushButton_bp.click()
        #
        # # notch initialization
        # self.apply_notch = 1
        # if (self.apply_notch):
        #     self.ui.doubleSpinBox_lc_notch.setValue(58.0)
        #     self.ui.doubleSpinBox_hc_notch.setValue(62.0)
        #     self.ui.doubleSpinBox_lc_notch.setMinimum(0.1)
        #     self.ui.doubleSpinBox_lc_notch.setMaximum(self.sr.sample_rate / 2 - 0.1)
        #     self.ui.doubleSpinBox_lc_notch.setSingleStep(1)
        #     self.ui.doubleSpinBox_hc_notch.setMinimum(0.1)
        #     self.ui.doubleSpinBox_hc_notch.setMaximum(self.sr.sample_rate / 2 - 0.1)
        #     self.ui.doubleSpinBox_hc_notch.setSingleStep(1)
        #     self.ui.pushButton_apply_notch.click()
        #
        # self.ui.checkBox_bandpass.setChecked(self.apply_bandpass)
        #
        # self.b_bandpass_scope_refilter = self.b_bandpass_scope
        # self.a_bandpass_scope_refilter = self.a_bandpass_scope
        # self.zi_bandpass_scope_refilter = self.zi_bandpass_scope
        # self.b_notch_scope_refilter = self.b_notch_scope
        # self.a_notch_scope_refilter = self.a_notch_scope
        # self.zi_notch_scope_refilter = self.zi_notch_scope

        # MRCP tab
        self.init_class_epoch_counter_table()
        self.init_class_bad_epoch_table()
        self.show_TID_events = False
        self.show_LPT_events = False
        self.show_Key_events = True

        self.raw_trial_MRCP = np.ndarray([])
        self.processed_trial_MRCP = np.ndarray([])
        self.total_trials_MRCP = []
        self.total_trials_raw_MRCP = []
        self.total_MRCP_inds = []
        self.temp_counter = 0
        self.temp_counter_list = []
        self.input_temp_list = []
        self.display_temp_list = []
        self.selected_temp = ""
        self.list_selected_temp = []
        self.template_buffer = np.zeros((6 * int(self.sr.sample_rate), self.config['eeg_channels']), dtype=float)

        self.b_lp, self.a_lp = Utils.butter_lowpass(3, int(self.sr.sample_rate), 2)
        self.b_hp, self.a_hp = Utils.butter_highpass(0.05, int(self.sr.sample_rate), 2)
        self.initial_condition_list_lp = Utils.construct_initial_condition_list(self.b_lp, self.a_lp,
                                                                                self.config['eeg_channels'])
        self.initial_condition_list_hp = Utils.construct_initial_condition_list(self.b_hp, self.a_hp,
                                                                                self.config['eeg_channels'])
        self.ui.pushButton_bad_epoch.clicked.connect(self.onClicked_button_bad_epoch)
        self.screen_width = 522
        self.screen_height = 160
        # self.setGeometry(100,100, self.screen_width, self.screen_height)
        # self.setFixedSize(self.screen_width, self.screen_height)
        self.setWindowTitle('EEG Scope Panel')
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.setFocus()
        logger.info('GUI show')
        self.show()

    def init_panel_GUI_stop_recording(self):
        """
        Initialize experimenter GUI when stop recording button pressed. This is used to
        prepare for next run.

        """
        # Tabs
        self.ui.tab_experimental_protocol.setEnabled(False)
        self.ui.tab_subjec_information.setEnabled(False)
        # self.ui.tab_Oscilloscope.setEnabled(False)
        self.ui.tab_experiment_type.setEnabled(False)

        # Experimental protocol
        # self.task_list = []
        # self.new_task_list = []
        # self.task_descriptor_list = []
        # self.task_image_path = ""
        # self.task_image_path_list = []
        # self.task_sound_path = ""
        # self.task_sound_path_list = []
        # self.task_table = np.ndarray([])
        # self.new_task_table = np.ndarray([])
        # self.task_counter = 0
        # self.protocol_path = ""
        # Button
        self.init_task_name_table()
        self.ui.groupBox_sequence_manager.setEnabled(False)

        # Event management tab
        self.event_timestamp_list = []
        # self.init_task_event_number_table()
        # self.event_list = []
        # Button
        self.event_file_path = ""
        self.mrcp_template_file_path = ""
        self.raw_eeg_file_path = ""
        self.raw_mrcp_file_path = ""
        self.subject_file_path = ""

        # Oscilloscope
        self.ui.comboBox_scale.setCurrentIndex(4)
        self.ui.checkBox_notch.setChecked(True)
        # self.ui.checkBox_car.setChecked(
        #     int(self.scope_settings.get("filtering", "apply_car_filter")))
        # self.ui.checkBox_bandpass.setChecked(
        #     int(self.scope_settings.get("filtering", "apply_bandpass_filter")))
        # self.ui.pushButton_apply_notch.setEnabled(False)
        self.ui.doubleSpinBox_lc_notch.setEnabled(False)
        self.ui.doubleSpinBox_hc_notch.setEnabled(False)

        # # initialize channel selection panel in main view GUI
        # self.channels_to_show_idx = []
        # idx = 0
        # for y in range(0, 4):
        #     for x in range(0, NUM_X_CHANNELS):
        #         if idx < self.config['eeg_channels']:
        #             # self.table_channels.item(x,y).setTextAlignment(QtCore.Qt.AlignCenter)
        #             self.ui.table_channels.item(x, y).setSelected(True)  # Qt5
        #             # self.table_channels.setItemSelected(self.table_channels.item(x, y), True) # Qt4 only
        #             self.channels_to_show_idx.append(idx)
        #         else:
        #             self.ui.table_channels.setItem(x, y,
        #                                            QTableWidgetItem("N/A"))
        #             self.ui.table_channels.item(x, y).setFlags(
        #                 QtCore.Qt.NoItemFlags)
        #             self.ui.table_channels.item(x, y).setTextAlignment(
        #                 QtCore.Qt.AlignCenter)
        #         idx += 1

        self.ui.table_channels.verticalHeader().setStretchLastSection(True)
        self.ui.table_channels.horizontalHeader().setStretchLastSection(True)
        self.channel_to_scale_row_index = -1
        self.channel_to_scale_column_index = -1

        self.selected_channel_row_index = 0
        self.selected_channel_column_index = 0
        self.single_channel_scale = 1

        # MRCP tab
        self.init_class_epoch_counter_table()
        self.init_class_bad_epoch_table()
        self.show_TID_events = False
        self.show_LPT_events = False
        self.show_Key_events = True
        self.raw_trial_MRCP = np.ndarray([])
        self.processed_trial_MRCP = np.ndarray([])
        self.total_trials_MRCP = []
        self.total_trials_raw_MRCP = []
        self.total_MRCP_inds = []
        self.temp_counter = 0
        self.temp_counter_list = []
        self.input_temp_list = []
        self.display_temp_list = []
        self.selected_temp = ""
        self.list_selected_temp = []
        self.template_buffer = np.zeros((6 * int(self.sr.sample_rate), self.config['eeg_channels']), dtype=float)

        self.b_lp, self.a_lp = Utils.butter_lowpass(3, int(self.sr.sample_rate), 2)
        self.b_hp, self.a_hp = Utils.butter_highpass(0.05, int(self.sr.sample_rate), 2)
        self.initial_condition_list_lp = Utils.construct_initial_condition_list(self.b_lp, self.a_lp,
                                                                                self.config['eeg_channels'])
        self.initial_condition_list_hp = Utils.construct_initial_condition_list(self.b_hp, self.a_hp,
                                                                                self.config['eeg_channels'])
        self.ui.pushButton_bad_epoch.clicked.connect(self.onClicked_button_bad_epoch)
        self.screen_width = 522
        self.screen_height = 160
        # self.setGeometry(100,100, self.screen_width, self.screen_height)
        # self.setFixedSize(self.screen_width, self.screen_height)
        self.setWindowTitle('EEG Scope Panel')
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.setFocus()
        self.show()

    def init_SV_GUI(self):
        """
        Initialize subject view GUI
        """
        self.SVStatus = 0
        self.starttime = 0
        self.SV_time = 0
        self.is_experiment_on = False

    def init_scope_GUI(self):
        """
        Initialize oscilloscope GUI
        """
        self.bool_parser = {True: '1', False: '0'}

        # PyQTGraph plot initialization
        self.win = pg.GraphicsWindow()
        self.win.setWindowTitle('EEG Scope')
        self.win.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)
        self.win.keyPressEvent = self.keyPressEvent
        # self.win.show()
        self.main_plot_handler = self.win.addPlot()
        self.win.resize(1280, 800)

        # Scales available in the GUI. If you change the options in the GUI
        # you should change them here as well
        self.scales_range = [1, 10, 25, 50, 100, 250, 500, 1000, 2500, 100000]
        self.single_scales_range = [0.2, 0.4, 0.6, 0.8, 1, 1.2, 1.5, 1.7, 1.8, 2]

        # Scale in uV
        self.scale = 100
        # Time window to show in seconds
        self.seconds_to_show = self.ui.spinBox_time.value()

        # Y Tick labels. Use values from the config file.
        self.channel_labels = []
        values = []

        ''' For non-LSL systems having no channel names
        for x in range(0, self.config['eeg_channels']):
            if (self.show_channel_names):
                self.channel_labels.append("(" + str(x + 1) + ") " +
                    self.scope_settings.get("internal",
                    "channel_names_" + self.device_name + str(
                    self.config['eeg_channels'])).split(', ')[x])
            else:
                self.channel_labels.append('CH ' + str(x + 1))
        '''
        ch_names = np.array(self.sr.get_channel_names())
        self.channel_labels = ch_names[self.sr.get_channels()]
        for x in range(0, len(self.channels_to_show_idx)):
            values.append((-x * self.scale,
                           self.channel_labels[self.channels_to_show_idx[x]]))

        values_axis = []
        values_axis.append(values)
        values_axis.append([])
        # Update table labels with current names
        idx = 0
        for y in range(0, 4):
            for x in range(0, NUM_X_CHANNELS):
                if (idx < self.config['eeg_channels']):
                    self.ui.table_channels.item(x, y).setText(
                        self.channel_labels[idx])
                idx += 1

        # Plot initialization
        # Plotting colors. If channels > 16, colors will roll back to the beginning
        self.colors = np.array(
            [[255, 0, 0], [0, 255, 0], [0, 0, 255], [255, 255, 0],
             [0, 255, 255], [255, 0, 255], [128, 100, 100], [0, 128, 0],
             [0, 128, 128], [128, 128, 0], [255, 128, 128], [128, 0, 128],
             [128, 255, 0], [255, 128, 0], [0, 255, 128], [128, 0, 255]])

        # pen = pg.mkColor(self.colors)
        # self.main_plot_handler.getAxis('left').setTextPen('b')

        self.main_plot_handler.getAxis('left').setTicks(values_axis)

        self.main_plot_handler.setRange(xRange=[0, self.seconds_to_show],
                                        yRange=[+1.5 * self.scale,
                                                -0.5 * self.scale - self.scale * self.config['eeg_channels']])
        self.main_plot_handler.disableAutoRange()
        self.main_plot_handler.showGrid(y=True)
        self.main_plot_handler.setLabel(axis='left',
                                        text='Scale (uV): ' + str(self.scale))
        self.main_plot_handler.setLabel(axis='bottom', text='Time (s)')

        # X axis
        self.x_ticks = np.zeros(self.config['sf'] * self.seconds_to_show);
        for x in range(0, self.config['sf'] * self.seconds_to_show):
            self.x_ticks[x] = (x * 1) / float(self.config['sf'])

        # We want a lightweight scope, so we downsample the plotting to 64 Hz

        self.subsampling_ratio = self.ui.spinBox_downsample_ratio.value()
        self.subsampling_freq = int(self.config['sf'] / self.subsampling_ratio)
        self.x_ticks_sub = np.zeros(self.subsampling_freq * self.seconds_to_show)
        # pdb.set_trace()

        for i, x in enumerate(np.arange(0, self.config['sf'] * self.seconds_to_show, self.subsampling_ratio)):
            self.x_ticks_sub[i] = (x * 1) / float(self.config['sf'])

        # EEG data for plotting
        self.data_plot = np.zeros((self.config['sf'] * self.seconds_to_show,
                                   self.config['eeg_channels']))

        self.data_plot_sub = np.zeros((self.subsampling_freq * self.seconds_to_show, self.config['eeg_channels']))

        print('self.data plot shape: ', self.data_plot.shape)

        self.curve_eeg = []
        for x in range(0, len(self.channels_to_show_idx)):
            self.curve_eeg.append(self.main_plot_handler.plot(x=self.x_ticks_sub,
                                                              y=self.data_plot_sub[:, self.channels_to_show_idx[x]],
                                                              pen=pg.mkColor(
                                                                  self.colors[self.channels_to_show_idx[x] % 16, :])))
            # self.curve_eeg[-1].setDownsampling(ds=self.subsampling_value, auto=False, method="mean")

        # Events data
        self.events_detected = []
        self.events_curves = []
        self.events_text = []

        # CAR initialization
        self.apply_car = False
        self.matrix_car = np.zeros(
            (self.config['eeg_channels'], self.config['eeg_channels']),
            dtype=float)
        self.matrix_car[:, :] = -1 / float(self.config['eeg_channels'])
        np.fill_diagonal(self.matrix_car,
                         1 - (1 / float(self.config['eeg_channels'])))

        # Laplacian initalization. TO BE DONE
        self.matrix_lap = np.zeros(
            (self.config['eeg_channels'], self.config['eeg_channels']),
            dtype=float)
        np.fill_diagonal(self.matrix_lap, 1)
        self.matrix_lap[2, 0] = -1
        self.matrix_lap[0, 2] = -0.25
        self.matrix_lap[0, 2] = -0.25

        # BP initialization
        self.apply_bandpass = 1
        if (self.apply_bandpass):
            self.ui.doubleSpinBox_lp.setValue(40.0)
            self.ui.doubleSpinBox_hp.setValue(1.0)
            self.ui.doubleSpinBox_lp.setMinimum(0)
            self.ui.doubleSpinBox_lp.setMaximum(self.sr.sample_rate / 2 - 0.1)
            self.ui.doubleSpinBox_lp.setSingleStep(1)
            self.ui.doubleSpinBox_hp.setMinimum(0)
            self.ui.doubleSpinBox_hp.setMaximum(self.sr.sample_rate / 2 - 0.1)
            self.ui.doubleSpinBox_hp.setSingleStep(1)
            self.ui.pushButton_bp.click()

        # notch initialization
        self.apply_notch = 1
        if (self.apply_notch):
            if self.sr.sample_rate / 2 - 0.1 > 58:
                self.ui.doubleSpinBox_lc_notch.setValue(58.0)
                self.ui.doubleSpinBox_hc_notch.setValue(62.0)
            else:
                self.ui.doubleSpinBox_lc_notch.setValue(1.0)
                self.ui.doubleSpinBox_hc_notch.setValue(2.0)
            self.ui.doubleSpinBox_lc_notch.setMinimum(0.1)
            self.ui.doubleSpinBox_lc_notch.setMaximum(self.sr.sample_rate / 2 - 0.1)
            self.ui.doubleSpinBox_lc_notch.setSingleStep(1)
            self.ui.doubleSpinBox_hc_notch.setMinimum(0.1)
            self.ui.doubleSpinBox_hc_notch.setMaximum(self.sr.sample_rate / 2 - 0.1)
            self.ui.doubleSpinBox_hc_notch.setSingleStep(1)
            self.ui.pushButton_apply_notch.click()

        self.ui.checkBox_bandpass.setChecked(self.apply_bandpass)

        self.b_bandpass_scope_refilter = self.b_bandpass_scope
        self.a_bandpass_scope_refilter = self.a_bandpass_scope
        self.zi_bandpass_scope_refilter = self.zi_bandpass_scope
        self.b_notch_scope_refilter = self.b_notch_scope
        self.a_notch_scope_refilter = self.a_notch_scope
        self.zi_notch_scope_refilter = self.zi_notch_scope

        self.update_title_scope()

        # Help variables
        self.show_help = 0
        self.help = pg.TextItem(
            "CNBI EEG Scope v0.3 \n" + "----------------------------------------------------------------------------------\n" + "C: De/activate CAR Filter\n" + "B: De/activate Bandpass Filter (with current settings)\n" + "T: Show/hide TiD events\n" + "L: Show/hide LPT events\n" + "K: Show/hide Key events. If not shown, they are NOT recorded!\n" + "0-9: Add a user-specific Key event. Do not forget to write down why you marked it.\n" + "Up, down arrow keys: Increase/decrease the scale, steps of 10 uV\n" + "Left, right arrow keys: Increase/decrease the time to show, steps of 1 s\n" + "Spacebar: Stop the scope plotting, whereas data acquisition keeps running (EXPERIMENTAL)\n" + "Esc: Exits the scope",
            anchor=(0, 0), border=(70, 70, 70),
            fill=pg.mkColor(20, 20, 20, 200), color=(255, 255, 255))

        # Stop plot functionality
        self.stop_plot = 0

        # Force repaint even when we shouldn't repaint.
        self.force_repaint = 1

    def init_timer(self):
        """
        Initialize main timer used for refreshing oscilloscope window. This refreshes every 20ms.
        """
        self.os_time_list1 = []
        QtCore.QCoreApplication.processEvents()
        QtCore.QCoreApplication.flush()
        self.timer = QtCore.QTimer(self)
        self.timer.setTimerType(QtCore.Qt.PreciseTimer)
        self.timer.timeout.connect(self.update_loop)
        self.timer.start(20)

    def init_Runtimer(self):
        """
        Initialize task related timer which controls the timing for visual cues
        """
        self.time_show = 0
        self.os_time_list = []

        self.Runtimer = task.LoopingCall(self.Time)

    def init_eye_tracker(self):
        self.eye_tracker_window.tableWidget.setRowCount(9)

        self.eye_tracker_window.pushButton_1.clicked.connect(self.update_cal1)
        self.eye_tracker_window.pushButton_2.clicked.connect(self.update_cal2)
        self.eye_tracker_window.pushButton_3.clicked.connect(self.update_cal3)
        self.eye_tracker_window.pushButton_4.clicked.connect(self.update_cal4)
        self.eye_tracker_window.pushButton_5.clicked.connect(self.update_cal5)
        self.eye_tracker_window.pushButton_6.clicked.connect(self.update_cal6)
        self.eye_tracker_window.pushButton_7.clicked.connect(self.update_cal7)
        self.eye_tracker_window.pushButton_8.clicked.connect(self.update_cal8)
        self.eye_tracker_window.pushButton_9.clicked.connect(self.update_cal9)

        self.eye_tracker_window.pushButton_12.clicked.connect(self.update_current_gaze_loc)
        self.eye_tracker_window.pushButton_13.clicked.connect(self.recording_data)
        self.eye_tracker_window.pushButton_14.clicked.connect(self.recording_stop)

        self.rec_time = int(self.eye_tracker_window.LineEdit_rec.text())
        # self.LineEdit_rec.clicked.conntect(self.update_rec_time(int(self.LineEdit_rec.text())))

        self.gaze_x = 0
        self.gaze_y = 0
        self.table_row = 0
        self.table_col = 0
        # print(self.gaze_x, self.gaze_y)

        self.UTC_time = 0

        # List of values in 9 points
        self.points = np.zeros((9, 2))

        self.gaze_loc = 0

    def trigger_help(self):
        """Shows / hide help in the scope window"""
        if self.show_help:
            self.help.setPos(0, self.scale)
            self.main_plot_handler.addItem(self.help)
            self.help.setZValue(1)
        else:
            self.main_plot_handler.removeItem(self.help)

    def eventFilter(self, source, event):
        """
        Select single channel to scale by right clicking
        :param source: channel table content
        :param event: right mouse button press
        :return: ID of the selected channel
        """
        if (event.type() == QtCore.QEvent.MouseButtonPress and
                event.buttons() == QtCore.Qt.RightButton and
                source is self.ui.table_channels.viewport()):
            item = self.ui.table_channels.itemAt(event.pos())
            # print('Global Pos:', event.globalPos())
            if item is not None:
                self.channel_to_scale_row_index = item.row()
                self.channel_to_scale_column_index = item.column()
                print("RRRRRRRRR", self.channel_to_scale_row_index, self.channel_to_scale_column_index)

                # print('Table Item:', item.row(), item.column())
                # self.menu = QMenu(self)
                # self.menu.addAction(item.text())         #(QAction('test'))
                # menu.exec_(event.globalPos())
        return super(MainView, self).eventFilter(source, event)
