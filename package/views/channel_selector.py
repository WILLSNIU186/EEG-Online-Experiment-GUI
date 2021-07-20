import numpy as np
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem

class ChannelSelector():
    NUM_X_CHANNELS = 16

    def onDoubleClicked_channel_table(self):
        for idx in self.ui.table_channels.selectionModel().selectedIndexes():
            self.selected_channel_row_index = idx.row()
            self.selected_channel_column_index = idx.column()
            print("ch index: {}, {}".format(self.selected_channel_row_index, self.selected_channel_column_index))

    def onClicked_button_update_channel_name(self):
        """
        Update channel name by double clicking channel name in channel manager and click update channel name
        to update them in Oscilloscope
        """

        # self.channel_labels[self.selected_channel_column_index * 16 + self.selected_channel_row_index] = \
        #     self.ui.table_channels.item(self.selected_channel_row_index, self.selected_channel_column_index).text()
        idx = 0
        new_channel_labels = []
        for y in range(0, 4):
            for x in range(0, ChannelSelector.NUM_X_CHANNELS):
                if (idx < self.config['eeg_channels']):
                    new_channel_labels.append(self.ui.table_channels.item(x, y).text())
                    idx += 1
        self.channel_labels = np.asarray(new_channel_labels)
        print("channel labels: {}".format(self.channel_labels))


    def onSelectionChanged_table(self):
        """
        Update highlighted channels in Channel Manager when different channels are selected
        """
        # Remove current plot
        for x in range(0, len(self.channels_to_show_idx)):
            self.main_plot_handler.removeItem(self.curve_eeg[x])

        # Which channels should I plot?
        self.channels_to_show_idx = []
        self.channels_to_hide_idx = []
        idx = 0
        for y in range(0, 4):
            for x in range(0, ChannelSelector.NUM_X_CHANNELS):
                if (idx < self.config['eeg_channels']):
                    if (QTableWidgetItem.isSelected(  # Qt5
                            self.ui.table_channels.item(x, y))):
                        self.channels_to_show_idx.append(idx)
                    else:
                        self.channels_to_hide_idx.append(idx)
                    idx += 1

        # Add new plots
        self.curve_eeg = []
        for x in range(0, len(self.channels_to_show_idx)):
            self.curve_eeg.append(self.main_plot_handler.plot(x=self.x_ticks,
                                                              y=self.data_plot[:, self.channels_to_show_idx[x]],
                                                              pen=self.colors[
                                                                  self.channels_to_show_idx[x] % ChannelSelector.NUM_X_CHANNELS, :]))
            self.curve_eeg[-1].setDownsampling(ds=self.subsampling_value,
                                               auto=False, method="mean")

        # Update CAR so it's computed based only on the shown channels
        if (len(self.channels_to_show_idx) > 1):
            self.matrix_car = np.zeros(
                (self.config['eeg_channels'], self.config['eeg_channels']),
                dtype=float)
            self.matrix_car[:, :] = -1 / float(len(self.channels_to_show_idx))
            np.fill_diagonal(self.matrix_car,
                             1 - (1 / float(len(self.channels_to_show_idx))))
            for x in range(0, len(self.channels_to_hide_idx)):
                self.matrix_car[self.channels_to_hide_idx[x], :] = 0
                self.matrix_car[:, self.channels_to_hide_idx[x]] = 0

        # Refresh the plot
        self.update_plot_scale(self.scale)