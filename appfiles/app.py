import appfiles.ui.loadingUi as loadingUi

from PyQt5.QtWidgets import QApplication


class App:
    def __init__(self, logger):
        self.logger = logger

        self.qApp = QApplication([])

    def run(self):
        self.runLoggin()
        self.runLoading()
        self.runClient()

    def runLoggin(self):
        self.logger.debug("Login")

        self.logger.debug("Login end")

    def runLoading(self):
        self.logger.debug("Loading")

        self.loadingUi = loadingUi.loadingWindow(self.logger)
        self.loadingUi.show()

        self.qApp.exec()

        self.logger.debug("Loading end")

    def runClient(self):
        self.logger.debug("Client")

        self.logger.debug("Client end")
