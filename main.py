__Author__ = "Bowarc\nDiscord: Bowarc#4159"

import appfiles.app as app
import appfiles.utils.logger as logger

if __name__ == "__main__":
    l = logger.logger(level=0, logFile="LoLUis.log",
                      custom_exception_hook=False)
    myApp = app.App(l)
    myApp.run()
