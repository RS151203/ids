import os
import subprocess
import sys
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt, QEvent, Signal, QTimer, QEasingCurve)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence,
                           QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PySide2.QtWidgets import *
from email_validator import validate_email, EmailNotValidError
from gui import Ui_MainWindow
from user_auth import create_connection, check_user, change_user_credentials, add_email, get_email, delete_email

WINDOW_SIZE = 0
TOGGLE_STATUS = 80


def open_log_folder():
    log_folder_path = r"C:\Aegis IDS\Log Files"

    if not os.path.exists(log_folder_path):
        os.makedirs(log_folder_path)

    subprocess.Popen(f'explorer "{log_folder_path}"')


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
        self.logout_button.clicked.connect(self.logging_out)  # lambda needs to add bracket after function name
        self.home_button.clicked.connect(lambda: self.page_indicator.move(0, self.home_button.pos().y()))
        self.settings_button.clicked.connect(lambda: self.page_indicator.move(0, self.settings_button.pos().y()))
        self.exit_button.clicked.connect(self.close)
        self.logs_button.clicked.connect(open_log_folder)

        # Time
        # Create a timer to update the label every second
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateTime)
        self.timer.start(1000)  # Update every 1000 milliseconds (1 second)

        # Call updateTime initially to set the label to current time
        self.updateTime()

        # SETTINGS
        self.update_user_config_button.clicked.connect(lambda: self.update_user_config(user=self.user_name_info.text()))
        self.error_popup_2.hide()
        self.cancel_error_popup_2.clicked.connect(lambda: self.error_popup_2.hide())
        self.add_email_address_button_4.clicked.connect(self.email_add)

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
            self.stackedWidget_2.setCurrentIndex(0)
            self.page_indicator.move(0, self.home_button.pos().y())
            self.user_name_info.setText(username)
            self.current_username.setText(username)
            self.email_address_area_4.setText(get_email(conn, username))
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

    def update_user_config(self, user):
        current_username = self.current_username.text()
        current_password = self.current_password.text()
        new_username = self.new_username.text()
        new_password = self.new_password.text()

        conn = create_connection("user.db")
        if new_username or new_password:
            result = check_user(conn, current_username, current_password)
            if result:
                username = change_user_credentials(conn, current_username, current_password, new_username, new_password)
                self.current_username.setText(username)
                self.user_name_info.setText(username)
                self.email_address_area_4.setText(get_email(conn, username))
                self.current_password.setText("")
                self.new_username.setText("")
                self.new_password.setText("")
            else:
                self.error_text_2.setText("Current Username or Password is incorrect.")
                self.error_popup_2.show()
                self.current_username.setText(user)
                self.current_password.setText("")
        else:
            self.error_text_2.setText("Add new username or new password.")
            self.error_popup_2.show()
            self.current_username.setText(user)
            self.current_password.setText("")

    def email_add(self):
        conn = create_connection("user.db")
        emails = self.email_address_area_4.toPlainText().replace(" ", "")
        if emails:
            email_array = emails.split(",")
            all_valid = True
            for email in email_array:
                try:
                    validate_email(email)
                except EmailNotValidError:
                    all_valid = False
                    break
            if all_valid:
                add_email(conn, username=self.current_username.text(), email=emails)
                self.email_address_area_4.setText(get_email(conn, username=self.current_username.text()))
            else:
                self.error_text_2.setText("Email or Emails not valid.")
                self.error_popup_2.show()
                self.email_address_area_4.setText(get_email(conn, username=self.current_username.text()))
        else:
            delete_email(conn, username=self.current_username.text())
            self.email_address_area_4.setText("")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Create and show the main window
    window = MainWindow()
    window.show()

    # Run the application event loop
    sys.exit(app.exec_())
