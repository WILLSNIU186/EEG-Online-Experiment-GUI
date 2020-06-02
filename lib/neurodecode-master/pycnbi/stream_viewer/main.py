# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 19:44:19 2020

@author: j33niu
"""
import sys
import pycnbi.utils.pycnbi_utils as pu
from PyQt5.QtWidgets import QMainWindow,QApplication, QTableWidgetItem
from Scope import Scope

if __name__ == '__main__':
    if len(sys.argv) == 2:
        amp_name = sys.argv[1]
        amp_serial = None
    elif len(sys.argv) == 3:
        amp_name, amp_serial = sys.argv[1:3]
    else:
        amp_name, amp_serial = pu.search_lsl()
    if amp_name == 'None':
        amp_name = None
    #logger.info('Connecting to a server %s (Serial %s).' % (amp_name, amp_serial))

    app = QApplication(sys.argv)
    ex = Scope(amp_name, amp_serial)
    sys.exit(app.exec_())