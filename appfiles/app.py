import appfiles.ui.loadingUi as loadingUi


class App:
    def __init__(self, logger):
        self.logger = logger

        self.loadingUi = loadingUi.loadingWindow()

    def run(self):
        self.logger.debug("Start of the run function")
        self.loadingUi.show()
