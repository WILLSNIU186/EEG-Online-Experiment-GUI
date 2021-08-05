from package.entity.edata.variables import Variables
from package.entity.base.participant import Participant
import datetime
import os
from PyQt5.QtWidgets import QFileDialog


class SubjectInfo():
    """
    Enter and save subject information.
    """

    def onClicked_button_save_subject_information(self):
        """
        Event listener for 'save' button on subject information tab. The subject information typed in Gself.ui
        will be saved to subject.txt
        """
        self.participant.first_name = self.ui.lineEdit_first_name.text()
        self.participant.last_name = self.ui.lineEdit_last_name.text()
        self.participant.gender = self.ui.lineEdit_gender.text()
        self.participant.age = self.ui.lineEdit_age.text()
        self.participant.email = self.ui.lineEdit_email.text()
        self.participant.telephone = self.ui.lineEdit_telephone.text()
        self.participant.address = self.ui.lineEdit_address.text()
        self.participant.comment = self.ui.plainTextEdit_additional_comments.toPlainText()
        self.ui.tab_subjec_information.setEnabled(False)

        base_path = self.choose_base_folder()
        path = r"{}\{}".format(base_path,
                               self.participant.first_name + "_" + self.participant.last_name + \
                               datetime.datetime.today().strftime('%Y-%m-%d'))
        Variables.set_base_folder_path(path)
        try:
            os.makedirs(Variables.get_base_folder_path())
        except OSError:
            print("Creation of the directory %s failed" % Variables.get_base_folder_path())
        self.subject_file_path = "{}\subject.txt".format(Variables.get_base_folder_path())
        self.participant.save_info(self.subject_file_path)
        # f = open(self.subject_file_path, "w+")
        # f.writelines("first name: {}\n".format(self.first_name))
        # f.writelines("last name: {}\n".format(self.last_name))
        # f.writelines("age: {}\n".format(self.age))
        # f.writelines("gender: {}\n".format(self.gender))
        # f.writelines("email: {}\n".format(self.email))
        # f.writelines("telephone: {}\n".format(self.telephone))
        # f.writelines("address: {}\n".format(self.address))
        # f.writelines("additional comments: {}\n".format(self.additional_comment))
        # f.close()
        self.ui.statusBar.showMessage(
            "Subject information is saved to {}".format("{}\subject.txt".format(Variables.get_base_folder_path())))

    def choose_base_folder(self):
        """
        Choose directory to save recording files.
        :returns: directory path
        """
        dir_name = QFileDialog.getExistingDirectory(self, "",
                                                    r"D:\OneDrive - University of Waterloo\Jiansheng\MRCP_folder\MRCP_online_interface\records",
                                                    QFileDialog.ShowDirsOnly)
        if dir_name:
            print(dir_name)
        return dir_name