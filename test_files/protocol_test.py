import numpy as np
import pdb
from package.entity.edata.utils import Utils
from package.entity.edata.variables import Variables
import pandas as pd

# task_table = [['left', 'left',
#                'C:/uw_ebionics_mrcp_online_interface_python/package/views/icon/left_hand.jpg',
#                'C:/uw_ebionics_mrcp_online_interface_python/package/views/icon/right.mp3'],
#               ['right' ,'right',
#                'C:/uw_ebionics_mrcp_online_interface_python/package/views/icon/right_hand.jpg',
#                'C:/uw_ebionics_mrcp_online_interface_python/package/views/icon/right.mp3']]
# task_list = []
# task_name_list = ['left', 'right', 'right']
# task_list.append(task_name_list)
# task_description_list = ['LEFT', 'RIGHT', 'RIGHT']
# task_list.append(task_description_list)
# task_table_list = np.transpose(np.asarray(task_list))
# pdb.set_trace()
# Utils.save_protocol_to_csv(task_table, 'exp protocol.csv',"C:\\uw_ebionics_mrcp_online_interface_python")


df = pd.read_csv("records/Subject_protocol_test_12_20200321/exp. protocol")
task_table = df.values


pdb.set_trace()
raw_data = df.values
raw_data = raw_data[:, 2:]


