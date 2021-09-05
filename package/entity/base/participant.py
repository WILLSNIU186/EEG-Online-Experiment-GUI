import os
import datetime
from package.entity.edata.variables import Variables

class Participant():
    '''
    Participant class defines basic information of a subject

    Attribute
    ---------
    first_name
    last_name
    gender
    age
    email
    telephone
    address
    comment
    '''
    def __init__(self, first_name='', last_name='', gender='', age='', email='',\
                 telephone='', address='', comment=''):
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.age = age
        self.email = email
        self.telephone = telephone
        self.address = address
        self.comment = comment

    def save_info(self, file):
        f = open(file, "w+")
        f.writelines("first name: {}\n".format(self.first_name))
        f.writelines("last name: {}\n".format(self.last_name))
        f.writelines("age: {}\n".format(self.age))
        f.writelines("gender: {}\n".format(self.gender))
        f.writelines("email: {}\n".format(self.email))
        f.writelines("telephone: {}\n".format(self.telephone))
        f.writelines("address: {}\n".format(self.address))
        f.writelines("additional comments: {}\n".format(self.comment))
        f.close()