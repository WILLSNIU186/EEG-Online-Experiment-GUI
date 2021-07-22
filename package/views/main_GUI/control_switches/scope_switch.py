


class ScopeSwitch():
    def onClicked_button_scope_switch(self, pressed):

        if pressed:
            self.ui.statusBar.showMessage("show oscilloscope")
            self.win.show()
        else:
            self.ui.statusBar.showMessage("oscilloscope closed")
            self.win.hide()
