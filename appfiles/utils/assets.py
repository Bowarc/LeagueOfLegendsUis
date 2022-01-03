import os


class assetsLoader:
    def __init__(self):
        self.ressourcePath = "appfiles\\src\\"
        pass

    def getImage(self, imageName):
        basePath = os.path.abspath(".")
        relativePath = self.ressourcePath + "img\\" + imageName

        return os.path.join(basePath, relativePath)

    def getQss(self, fileName):
        basePath = os.path.abspath(".")
        relativePath = self.ressourcePath + "qss\\" + fileName

        return os.path.join(basePath, relativePath)

    def getFont(self, fileName):
        basePath = os.path.abspath(".")
        relativePath = self.ressourcePath + "font\\" + fileName

        return os.path.join(basePath, relativePath)
