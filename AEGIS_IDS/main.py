import sys
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt, QEvent, Signal, QTimer, QEasingCurve)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence,
                           QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PySide2.QtWidgets import *
from gui import Ui_MainWindow
from user_auth import create_connection, check_user

WINDOW_SIZE = 0
TOGGLE_STATUS = 80


class MainWindow(QMainWindow, Ui_MainWindow):
    stackSignal = Signal()

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setupUi(self)
        self.show()
        self.center()
        self.ui = Ui_MainWindow()
        global window_obj
        window_obj = self.ui

        # LOGIN
        self.login_button.clicked.connect(self.verification_login)
        self.error_popup_area.hide()
        self.cancel_error_popup.clicked.connect(lambda: self.error_popup_area.hide())
        self.show_password_check_box.stateChanged.connect(self.show_password)

        # self.stackedWidget.setCurrentIndex(1)

        # MAIN
        # Window_Control_Buttons
        self.exit.clicked.connect(lambda: self.close())
        self.minimize.clicked.connect(lambda: self.showMinimized())
        self.maxmize.clicked.connect(lambda: self.restore_or_maximize_window())

        # Menu
        self.menu_button.clicked.connect(self.toggleMenu)
        self.home_button.clicked.connect(lambda: self.stackedWidget_2.setCurrentIndex(0))
        self.settings_button.clicked.connect(lambda: self.stackedWidget_2.setCurrentIndex(1))
        self.logout_button.clicked.connect(self.logging_out) #lambda needs to add bracket after function name
        self.home_button.clicked.connect(lambda: self.page_indicator.move(0, self.home_button.pos().y()))
        self.settings_button.clicked.connect(lambda: self.page_indicator.move(0, self.settings_button.pos().y()))
        self.exit_button.clicked.connect(self.close)
        #Time
        # Create a timer to update the label every second
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateTime)
        self.timer.start(1000)  # Update every 1000 milliseconds (1 second)

        # Call updateTime initially to set the label to current time
        self.updateTime()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def verification_login(self):

        conn = create_connection("user.db")

        username = self.user_name.text()
        password = self.password.text()

        result = check_user(conn, username, password)

        if result:
            self.stackedWidget.setCurrentIndex(1)
            self.user_name_info.setText(username)
        else:
            self.show_error("Username or Password incorrect")
    def show_error(self, message):
        self.error_text.setText(message)
        self.error_popup_area.show()

    def show_password(self, state):
        if state == Qt.Checked:
            self.password.setEchoMode(QLineEdit.Normal)
        else:
            self.password.setEchoMode(QLineEdit.Password)

    def restore_or_maximize_window(self):
        # global variable for window size
        global WINDOW_SIZE
        win_status = WINDOW_SIZE
        if win_status == 0:
            WINDOW_SIZE = 1
            self.showFullScreen()
        else:
            WINDOW_SIZE = 0
            self.showNormal()

    def updateTime(self):
        # Get current time
        current_time = QTime.currentTime()

        # Convert time to string format
        time_str = current_time.toString('hh:mm:ss')

        # Update label text
        self.label_42.setText(time_str)

    def logging_out(self):
        self.stackedWidget.setCurrentIndex(0)
        self.user_name_info.clear()
        self.user_name.clear()
        self.password.clear()

    def toggleMenu(self):
        global TOGGLE_STATUS
        STATUS = TOGGLE_STATUS
        duration = 500
        if STATUS == 80:

            # TODO EXPANDING ANIMATION
            self.animation = QPropertyAnimation(self.menu, b"minimumWidth")
            self.animation.setDuration(duration)
            self.animation.setStartValue(80)
            self.animation.setEndValue(250)
            self.animation.setEasingCurve(QEasingCurve.OutExpo)
            self.animation.start()

            TOGGLE_STATUS = 150

        else:  # TODO COLLAPSING ANIMATION minimumHeight
            self.animation = QPropertyAnimation(self.menu, b"minimumWidth")
            self.animation.setDuration(duration)
            self.animation.setStartValue(250)
            self.animation.setEndValue(80)
            self.animation.setEasingCurve(QEasingCurve.OutExpo)
            self.animation.start()
            TOGGLE_STATUS = 80


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Create and show the main window
    window = MainWindow()
    window.show()

    # Run the application event loop
    sys.exit(app.exec_())
