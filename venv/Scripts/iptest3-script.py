#!C:\uw_ebionics_mrcp_online_interface_python\venv\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'ipython','console_scripts','iptest3'
__requires__ = 'ipython'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('ipython', 'console_scripts', 'iptest3')()
    )
