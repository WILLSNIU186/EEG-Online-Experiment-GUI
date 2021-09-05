from data_loader import DataLoader

if __name__ == '__main__':
    record_folder = r"D:\OneDrive - University of Waterloo\Jiansheng\MRCP_folder\MRCP_online_interface\offline_processing\records\Narsimha_WEIE_LR_formal_2020-10-17"
    data_loader = DataLoader(record_folder=record_folder, fs=500, experiment_type='MRCP')
    data_loader.get_channels()
    data_loader.get_event_mapping()
    data_loader.get_channel_types()
    data_loader.create_raw_object()
    data_loader.create_event()