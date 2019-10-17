from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWidgets import QMainWindow

import sys
from pitckgui.maingui import MainGUI
from pitck.imbandpass import ImageOperations


if __name__ == '__main__':

    imageops = ImageOperations()
    appctxt = ApplicationContext()
    mainapp = MainGUI(imageoperator=imageops)
    mainapp.show()
    sys.exit(appctxt.app.exec_())
