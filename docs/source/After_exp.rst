After experiment
----------------

Directory structure

| root folder
| ├── event_annotation.csv
| ├── subject.txt
| ├── Run1
| │   ├── bad_epochs.csv
| │   └── channels.csv
| │   └── event.csv
| │   └── raw_eeg.csv


* event_annotation.csv
    Task name and event number entered in GUI will list up here.

* subject.txt
    Subject information will be saved in this file.

* bad_epochs.csv
    Specified bad epochs using bad epoch button in GUI will show up here.

* channels.csv
    channel names will be saved here.

* event.csv
    event number and timestamp for each event will listed up here.

* raw_eeg.csv
    timestamps will show in first column, second column is a placeholder for
    marker (not supported now), the rest columns represents channels data.