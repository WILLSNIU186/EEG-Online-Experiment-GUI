Design your own GUI
----------------------
This GUI is designed using Pyqt5, please refer to Pyqt and
`qt designer tutorials <https://realpython.com/qt-designer-python/>`_
for creating basic window. GUI files are saved in package\views\layouts, you could open one of
them to modify.

Following example is assuming you want to modify experimenter GUI based on the current
design.

* Open package\views\layouts\mainwindow3.ui in Qt Designer.

* Once you designed your own window and saved as .ui file inside layouts foler,
  run the following code in terminal to convert .ui into .py file.

.. code-block::

    pyuic5 –x your_GUI.ui –o your_GUI.py


* Open your_GUI.py, do following modifications:
    * replace class name with 'Ui_MainWindow'
    * Add this line before class definition

        .. code-block:: python

            import pyqtgraph as pg


    * replace
        .. code-block:: python

            self.graphicsView = QtWidgets.QGraphicsView(self.tab_MRCP)

       with
        .. code-block:: python

            self.graphicsView = pg.PlotWidget(self.tab_MRCP)



* Modify GUI module names accordingly in main_view.py
    Replace 'main_layout16' with 'your_GUI' in the whole file