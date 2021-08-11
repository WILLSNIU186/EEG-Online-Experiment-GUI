from __future__ import print_function

import pdb

import CalculateSMR
import matlab
import matplotlib.pyplot as plt
import numpy as np

from analyzer import Analyzer
from data_loader import DataLoader
from preprocessing import Preprocessing
import philistine

if __name__ == "__main__":
    pre_process = True
    mode = "SMR"
    generate_report = False
    Ref = "O1"
    exp_counter = 2002
    if mode == "MRCP":
        low_freq = 40
        hi_freq = 400
    elif mode == "SMR":
        low_freq = 1
        hi_freq = 50

    if pre_process == True:
        ####################################################################################################################
        # import data
        ####################################################################################################################
        data_loader = DataLoader(exp_counter=exp_counter)
        data_loader.init_task_dependent_variables()
        data_loader.load_data()
        data_loader.create_raw_object()
        # pdb.set_trace()
        data_loader.create_event()
        BV_header_file = r"D:\OneDrive - University of Waterloo\Jiansheng\MRCP_folder\MRCP_online_interface\BP_record\sample_data\NE.vhdr"
        # philistine.mne.write_raw_brainvision(data_loader.raw_array, BV_header_file, data_loader.event_array)
        print(
            "-----------------------------------------------------------------------------------------------------------"
            "\n{}\n------------------------------------------------------------------------------------------------------"
                .format(data_loader.exp_name))

        filtered = data_loader.raw_array.notch_filter(60, picks='emg')
        filtered.plot(duration=100)
        plt.show()
        pdb.set_trace()
        # data_loader.raw_array.plot(duration=30)
        # plt.show()
        # pdb.set_trace()
        ####################################################################################################################
        # preprocessing
        ####################################################################################################################
        preprocessing = Preprocessing(data_loader)
        preprocessing.data_loader.raw_array.plot_psd()
        preprocessing.apply_filter(hi=hi_freq, low=low_freq, order=2)
        preprocessing.apply_referencing(reference_channel=[Ref], duration=100, change_raw=True)
        preprocessing.filtered_raw_array.copy().pick_channels(["C3", "Cz", "C4"]).plot(duration=100)
        preprocessing.apply_ICA()
        preprocessing.exclude_ICA()
        # save data
        preprocessing.save_consecutive_data(special_name='referenced_using_{}'.format(Ref))

    ####################################################################################################################
    # analyze
    ####################################################################################################################
    else:
        for mode in ['SMR']:
            if mode == "MRCP":
                low_freq = 0.05
                hi_freq = 5
            elif mode == "SMR":
                low_freq = 1
                hi_freq = 50

            for CAR in [False]:
                analyzer = Analyzer(exp_counter=exp_counter, low_freq=low_freq, hi_freq=hi_freq,
                                    pick_channels=['Cz', 'C3', 'C4'], generate_report=generate_report)
                analyzer.create_event()
                analyzer.load_preprocessed_data(special_name='referenced_using_{}'.format(Ref), duration=100)
                # if CAR:
                #     analyzer.apply_referencing()

                # epoch data
                # left_signal_epochs = analyzer.epoch_data(tmin=-3, tmax=5, baseline=None, cue_type='left',
                #                                          caption='left signal')
                #
                # left_noise_epochs = analyzer.epoch_data(tmin=3, tmax=11, baseline=None, cue_type='left',
                #                                         caption='left noise')
                # right_signal_epochs = analyzer.epoch_data(tmin=-3, tmax=5, baseline=None, cue_type='right',
                #                                           caption='right signal')
                # right_noise_epochs = analyzer.epoch_data(tmin=3, tmax=11, baseline=None, cue_type='right',
                #                                          caption='right noise')
                for task in ['EE_l', 'EE_r', 'R_l', 'R_r', 'WE_l', 'WE_r']:
                # for task in ['AD']:
                    signal_epochs = analyzer.epoch_data(tmin=-3, tmax=5, baseline=None, cue_type=task,
                                                        caption='{} signal'.format(task))
                    # pdb.set_trace()

                    noise_epochs = analyzer.epoch_data(tmin=3, tmax=11, baseline=None, cue_type=task,
                                                       caption='{} noise'.format(task))
                    if mode == "MRCP":
                        signal_evoked = analyzer.create_evoked_data(signal_epochs, tmin=-3, tmax=5,
                                                                    caption='{} signal'.format(task), line_color='r',
                                                                    vline=[0.])
                        noise_evoked = analyzer.create_evoked_data(noise_epochs, tmin=3, tmax=11,
                                                                   caption='{} noise'.format(task), line_color='k',
                                                                   vline=None)

                        analyzer.apply_lap(signal_evoked, caption='{} signal'.format(task))
                        analyzer.apply_lap(noise_evoked, caption='{} noise'.format(task))

                    if mode == "SMR":
                        # eng = matlab.engine.start_matlab()
                        reshaped_signal_epochs = np.transpose(signal_epochs, (1, 2, 0))
                        # scipy.io.savemat('epochs.mat', mdict={'arr': reshaped_left_signal_epochs})
                        reshaped_signal_epochs = matlab.double(reshaped_signal_epochs.tolist())

                        my_calculate_SMR = CalculateSMR.initialize()
                        plot_bootstrap = matlab.double([0])
                        plot_db = matlab.double([0])
                        plot_true_power = matlab.double([0])
                        plot_ERD = matlab.double([1])
                        srate = matlab.double([500])
                        time_start = matlab.double([-3])
                        time_end = matlab.double([5])
                        baseline_start = matlab.double([-2])
                        baseline_end = matlab.double([-1])
                        freq_min = matlab.double([1])
                        freq_max = matlab.double([50])
                        num_frex = matlab.double([50])
                        xlim_min = matlab.double([-2])
                        xlim_max = matlab.double([4])
                        cyc_min = matlab.double([4])
                        cyc_max = matlab.double([10])
                        fix_cyc = matlab.double([0])
                        cyc_num = matlab.double([5])
                        clim_min = matlab.double([-100])
                        clim_max = matlab.double([100])
                        plot_row = matlab.double([6])
                        plot_col = matlab.double([6])

                        my_calculate_SMR.CalculateSMR(reshaped_signal_epochs,
                                                      '{} {}'.format(analyzer.data_loader.exp_name, task),
                                                      plot_bootstrap, plot_db, plot_true_power, plot_ERD,
                                                      srate, time_start, time_end, baseline_start, baseline_end,
                                                      freq_min,
                                                      freq_max, num_frex, xlim_min, xlim_max, cyc_min, cyc_max,
                                                      fix_cyc, cyc_num, clim_min, clim_max, plot_row, plot_col,
                                                      analyzer.data_loader.channel_names,
                                                      analyzer.data_loader.n_channel,
                                                      nargout=0)

                        # my_calculate_SMR.CalculateSMR(reshaped_left_signal_epochs,
                        #                               '{} left'.format(analyzer.data_loader.exp_name),
                        #                               plot_bootstrap, plot_db, plot_true_power, plot_ERD,
                        #                               srate, time_start, time_end, baseline_start, baseline_end, freq_min,
                        #                               freq_max, num_frex, xlim_min, xlim_max, cyc_min, cyc_max,
                        #                               fix_cyc, cyc_num, clim_min, clim_max, plot_row, plot_col,
                        #                               analyzer.data_loader.channel_names, analyzer.data_loader.n_channel,
                        #                               nargout=0)
                        my_calculate_SMR.terminate()

                        analyzer.plot_power_band_temporal_ERD(epoch=signal_epochs, low_freq=1, high_freq=50,
                                                              toi_min=-2, toi_max=-1, num_freq=50,
                                                              caption='left signal',
                                                              task_name=analyzer.exp_name, mode='percent',
                                                              baseline=(-2.5, -1))

                        # analyzer.plot_power_band_temporal_ERD(epoch=right_signal_epochs, low_freq=1, high_freq=50,
                        #                                       toi_min=-2, toi_max=-1, num_freq=50, caption='right signal',
                        #                                       task_name=analyzer.exp_name, mode='percent',
                        #                                       baseline=(-2.5, -1))
                    # analyzer.load_epoches()

                    # elif mode == "MRCP":
                    #     for task in ['EE_l', 'EE_r', 'R_l', 'R_r', 'WE_l', 'WE_r']:
                    #         signal_evoked = analyzer.create_evoked_data(left_signal_epochs, tmin=-3, tmax=5,
                    #                                                     caption='left signal', line_color='r',
                    #                                                     show_vline=True)
                    #
                    #     left_signal_evoked = analyzer.create_evoked_data(left_signal_epochs, tmin=-3, tmax=5,
                    #                                                      caption='left signal', line_color='r',
                    #                                                      show_vline=True)
                    #     left_noise_evoked = analyzer.create_evoked_data(left_noise_epochs, tmin=3, tmax=11,
                    #                                                     caption='left noise', line_color='k',
                    #                                                     show_vline=False)
                    #     right_signal_evoked = analyzer.create_evoked_data(right_signal_epochs, tmin=-3, tmax=5,
                    #                                                       caption='right signal', line_color='r',
                    #                                                       show_vline=True)
                    #     right_noise_evoked = analyzer.create_evoked_data(right_noise_epochs, tmin=3, tmax=11,
                    #                                                      caption='right noise', line_color='k',
                    #                                                      show_vline=False)
                    #     analyzer.apply_lap(left_signal_evoked, caption='left signal')
                    #     analyzer.apply_lap(left_noise_evoked, caption='left noise')
                    #     analyzer.apply_lap(right_signal_evoked, caption='right signal')
                    #     analyzer.apply_lap(right_noise_evoked, caption='right noise')
                    #     # analyzer.save_consecutive_data()
                    # pdb.set_trace()
                if generate_report:
                    analyzer.save_report(mode=mode, Ref=Ref)
