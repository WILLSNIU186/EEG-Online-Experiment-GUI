#!/usr/bin/env python
import sys

import pycnbi.utils.pycnbi_utils as pu
from PyQt5 import QtWidgets

from package.entity.edata import constants, variables
from package.views.main_GUI import main_view
from package.views.record_replay_GUI.record_replay_selector import RecordReplaySelector
from package.views.stream_selector_GUI.stream_selector_view import StreamSelectorView


# def display_views():
#     if len(sys.argv) == 2:
#         amp_name = sys.argv[1]
#         amp_serial = None
#     elif len(sys.argv) == 3:
#         amp_name, amp_serial = sys.argv[1:3]
#     else:
#         amp_name, amp_serial = pu.search_lsl()
#         variables.Variables.set_amp_name(amp_name)
#         variables.Variables.set_amp_serial(amp_serial)
#     if amp_name == 'None':
#         amp_name = None
#     app = QtWidgets.QApplication(sys.argv)
#     ex = main_view.MainView(variables.Variables.get_amp_name(), variables.Variables.get_amp_serial())
#     sys.exit(app.exec_())

if __name__ == "__main__":
    variables.Variables.set_current_environment(constants.CONSTANTS.ENV_DEVELOPMENT)

    app = QtWidgets.QApplication(sys.argv)
    record_replay_view = RecordReplaySelector()
    stream_selector_view = StreamSelectorView()
    # ex = main_view.MainView(variables.Variables.get_amp_name(), variables.Variables.get_amp_serial())
    ex = main_view.MainView(variables.Variables.get_amp_name(), variables.Variables.get_amp_serial())

    sys.exit(app.exec_())