from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWidgets import QMainWindow

import sys
from pitckgui.maingui import MainGUI



if __name__ == '__main__':
    appctxt = ApplicationContext()
    gallery = MainGUI()
    gallery.show()
    sys.exit(appctxt.app.exec_())
