
from PyQt5 import uic
from PyQt5.Qt import QApplication, QMainWindow
import sys
import pyperclip
from PyQt5.QtCore import Qt, QObject, QEvent
from PyQt5.QtGui import QColor, QFont, QFontDatabase


class Filter(QObject):
    def eventFilter(self, widget, event):
        # FocusOut event
        if event.type() == QEvent.FocusOut:
            # return False so that the widget will also handle the event
            # otherwise it won't focus out
            return True
        else:
            # we don't care about other events
            return False


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.__ignoreUpdate = 0
        self.new_username = []

        self.changeScreen("mainWin.ui", self.mainWin)

    def changeScreen(self, fileUi, nextFunct=""):
        self.__nextFunct = nextFunct
        uic.loadUi(fileUi, self)
        self.show()
        if self.__nextFunct != "":
            self.__nextFunct()

    def updatePreview(self):
        self.usernameUpdate.setText("<p>" +
                                    "".join(list(map(lambda char: f"<span style=' color:\"{char[1]['color'] if char[1]['color']!='' else '#ffffff'}\"; font-weight:{char[1]['bold']}; text-decoration:{char[1]['strike']} {char[1]['under']}; font-style:{char[1]['ita']}; ' >{char[0] if char[1]['obf'] == '' else '§'}</span>", self.new_username))) +
                                    "</p>")
        # print(self.usernameUpdate.text())
        pass

    def textEditPreview(self, id, val):
        # c'è una lettera selezionata?
        if self.username.hasSelectedText():
            # prendi l'inizio della selezione
            start = self.username.selectionStart()
            # e la durata
            lenght = self.username.selectionLength()

            for i in range(start, start+lenght):
                if id != "reset":
                    self.new_username[i][1][id] = val if self.new_username[i][1][id] != val else ""
                else:
                    self.new_username[i][1] = {
                        "color": "", "bold": "", "strike": "", "under": "", "ita": "", "obf": ""}

            self.updatePreview()

    def mapNewString(self, newtext):
        self.copiato.clear()
        if self.__ignoreUpdate == 0:
            self.new_username = list(
                map(lambda x: [x, {"color": "", "bold": "", "strike": "", "under": "", "ita": "", "obf": ""}], list(newtext)))

    def generateMC(self):

        translTab = {
            "": "",
            "#000000": "&0",
            "#0000AA": "&1",
            "#00AA00": "&2",
            "#00AAAA": "&3",
            "#AA0000": "&4",
            "#AA00AA": "&5",
            "#FFAA00": "&6",
            "#AAAAAA": "&7",
            "#555555": "&8",
            "#5555FF": "&9",
            "#55FF55": "&a",
            "#55FFFF": "&b",
            "#FF5555": "&c",
            "#FF55FF": "&d",
            "#FFFF55": "&e",
            "#FFFFFF": "&f",
            "bold": "&l",
            "line-through": "&m",
            "underline": "&n",
            "italic": "&o",
            "1": "&k"
        }

        temp = "".join(
            list(map(lambda char: f"{translTab[char[1]['color']]}{translTab[char[1]['bold']]}{translTab[char[1]['strike']]}{translTab[char[1]['under']]}{translTab[char[1]['ita']]}{translTab[char[1]['obf']]}{char[0]}&r", self.new_username)))

        print(temp)
        pyperclip.copy(temp)
        self.copiato.setText("Copiato...")

    def mcFormatToText(self, newtext):
        self.new_username = []
        self.username.clear()
        mem = []

        translTab = {
            "": "",
            "&0": ["color", "#000000"],
            "&1": ["color", "#0000AA"],
            "&2": ["color", "#00AA00"],
            "&3": ["color", "#00AAAA"],
            "&4": ["color", "#AA0000"],
            "&5": ["color", "#AA00AA"],
            "&6": ["color", "#FFAA00"],
            "&7": ["color", "#AAAAAA"],
            "&8": ["color", "#555555"],
            "&9": ["color", "#5555FF"],
            "&a": ["color", "#55FF55"],
            "&b": ["color", "#55FFFF"],
            "&c": ["color", "#FF5555"],
            "&d": ["color", "#FF55FF"],
            "&e": ["color", "#FFFF55"],
            "&f": ["color", "#FFFFFF"],
            "&l": ["bold", "bold"],
            "&m": ["strike", "line-through"],
            "&n": ["under", "underline"],
            "&o": ["ita", "italic"],
            "&k": ["obf", "1"]
        }

        self.__ignoreUpdate = 1

        for string in newtext.split("&r"):
            char = string[-1:]
            string = string[:-1]
            mem = [char, {"color": "", "bold": "", "strike": "",
                          "under": "", "ita": "", "obf": ""}]
            self.username.setText(self.username.text()+char)
            if string != '':
                try:
                    for i in range(0, len(string), 2):

                        mem[1][translTab[string[i]+string[i+1]][0]
                               ] = translTab[string[i]+string[i+1]][1]

                except:
                    return

            self.new_username.append(mem)

        self.__ignoreUpdate = 0
        self.updatePreview()

    def mainWin(self):

        self.btnBlack.clicked.connect(
            lambda: self.textEditPreview("color", "#000000"))  # &0
        self.btnDBlue.clicked.connect(
            lambda: self.textEditPreview("color", "#0000AA"))  # &1
        self.btnDGreen.clicked.connect(
            lambda: self.textEditPreview("color", "#00AA00"))  # &2
        self.btnDAqua.clicked.connect(
            lambda: self.textEditPreview("color", "#00AAAA"))  # &3
        self.btnDRed.clicked.connect(
            lambda: self.textEditPreview("color", "#AA0000"))  # &4
        self.btnDPurple.clicked.connect(
            lambda: self.textEditPreview("color", "#AA00AA"))  # &5
        self.btnGold.clicked.connect(
            lambda: self.textEditPreview("color", "#FFAA00"))  # &6
        self.btnGray.clicked.connect(
            lambda: self.textEditPreview("color", "#AAAAAA"))  # &7
        self.btnDGray.clicked.connect(
            lambda: self.textEditPreview("color", "#555555"))  # &8
        self.btnBlue.clicked.connect(
            lambda: self.textEditPreview("color", "#5555FF"))  # &9
        self.btnGreen.clicked.connect(
            lambda: self.textEditPreview("color", "#55FF55"))  # &a
        self.btnAqua.clicked.connect(
            lambda: self.textEditPreview("color", "#55FFFF"))  # &b
        self.btnRed.clicked.connect(
            lambda: self.textEditPreview("color", "#FF5555"))  # &c
        self.btnLPurple.clicked.connect(
            lambda: self.textEditPreview("color", "#FF55FF"))  # &d
        self.btnYellow.clicked.connect(
            lambda: self.textEditPreview("color", "#FFFF55"))  # &e
        self.btnWhite.clicked.connect(
            lambda: self.textEditPreview("color", "#FFFFFF"))  # &f

        self.btnBold.clicked.connect(
            lambda: self.textEditPreview("bold", "bold"))  # &l
        self.btnStrike.clicked.connect(
            lambda: self.textEditPreview("strike", "line-through"))  # &m
        self.btnUnder.clicked.connect(
            lambda: self.textEditPreview("under", "underline"))  # &n
        self.btnItalic.clicked.connect(
            lambda: self.textEditPreview("ita", "italic"))  # &o
        self.btnObf.clicked.connect(
            lambda: self.textEditPreview("obf", "1"))  # &k

        self.btnReset.clicked.connect(
            lambda: self.textEditPreview("reset", ""))  # &r

        self.btnGenera.clicked.connect(self.generateMC)

        self._filter = Filter()
        self.username.installEventFilter(self._filter)
        self.username.textChanged.connect(self.mapNewString)
        self.mcFormat.textChanged.connect(self.mcFormatToText)

        self.statusBar.showMessage('Made by alessandrobasi.it')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
