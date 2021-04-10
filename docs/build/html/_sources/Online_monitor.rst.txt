Online Monitor
-------------------

Online monitor is used for experimenter monitoring bad epochs and
interested signal extraction.

* MRCP monitor. In my experiment, movement-related cotical potential
  (MRCP) is the interested signal, I applied laplacian filter to
  extract MRCP component from each trial for monitoring. Several other
  tabs are reserved for other experiments like EMG, ECG, SSVEP. You
  could design your own monitor.

    .. image:: ../tutorial_images/online_exp_tab.png
      :width: 800
      :alt: online_exp_tab

* Bad epoch monitor. During the experiment, you could record the number
  of bad epoch by clicking bad epoch button, they will be saved into
  bad_epochs.csv.

    .. image:: ../tutorial_images/bad_epoch.png
      :width: 200
      :alt: bad_epoch