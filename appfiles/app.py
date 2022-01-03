import appfiles.ui.loadingUi as loadingUi


class App:
    def __init__(self, logger):
        self.logger = logger

        self.loadingUi = loadingUi.loadingWindow(self.logger)

    def run(self):
        self.logger.debug("Start of the run function")
        self.loadingUi.show()
