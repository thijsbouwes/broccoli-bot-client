from bbot.ui import Ui
from PySide2.QtWidgets import QApplication
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = Ui()
    ui.resize(1920, 920)
    ui.setWindowTitle('Broccoli - RIC-TOI')
    ui.show()
    sys.exit(app.exec_())
