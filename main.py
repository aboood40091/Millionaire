#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Who wants to be a millionaire
# By AboodXD

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


################################################################
################################################################

# Imports
import os.path
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from random import shuffle
import sys

# import the module containing the questions list
import questions

# Set current working directory to the executable's path
path = os.path.dirname(os.path.realpath(sys.argv[0])).replace("\\", "/")
os.chdir(path)

# lambda function to get the absolute path for an image
getImage = lambda name: "./images/%s.png" % name

# Initial number of questions
numQuestions = 0

# Prizes
prizes = [
    "£100", "£200", "£300", "£500", "£1,000", "£2,000", "£4,000", "£8,000",
    "£16,000", "£32,000", "£64,000", "£125,000", "£250,000", "£500,000", "£1 Million",
]


def addQuestions(window):
    """
    Add randomly-selected questions from
    the question list to the window
    Maximum number of questions is 15
    """
    _questions = questions.questions.copy()
    if len(_questions) > 15:
        _questions = _questions[:15]

    shuffle(_questions)

    for i, (question, answers) in enumerate(_questions):
        page = Page(window, i+1)
        page.setQuestion(question, answers)
        window.addWidget(page)

    global numQuestions
    numQuestions = len(_questions)

    window.widget(1).setImage()
    window.widget(1).label.setText("Congratulations!\nYou won %s!" % prizes[numQuestions-1])


class Button(QtWidgets.QPushButton):
    """
    Custom Button Widget
    """
    def __init__(self, text, parent, isRight):
        super().__init__(text, parent)

        self.setStyleSheet("background-color: #3399FF; color: #FDFEFE;  font-size: 20pt")

        if isRight:
            self.clicked.connect(self.rightClicked)

        else:
            self.clicked.connect(self.wrongClicked)

    def rightClicked(self):
        window = self.parent().parent()
        index = window.currentIndex()

        if index == numQuestions + 2:
            window.setCurrentIndex(1)

        else:
            if index == 0:
                window.setCurrentIndex(3)
                widget = window.widget(3)

            else:
                window.setCurrentIndex(index + 1)
                widget = window.widget(index + 1)

            widget.image.setPixmap(QPixmap(getImage("Picture%d" % (window.currentIndex() - 3))).scaledToHeight(580, Qt.SmoothTransformation))

    def wrongClicked(self):
        window = self.parent().parent()
        index = window.currentIndex()

        if index in [1, 2]:
            window.setCurrentIndex(0)

            for i in range(window.count(), 2, -1):
                widget = window.widget(i)
                window.removeWidget(widget)
                del widget

            global numQuestions
            numQuestions = 0

            addQuestions(window)

        else:
            window.setCurrentIndex(2)


class Page(QtWidgets.QWidget):
    """
    Page Widget for a question
    The answers are shuffled
    """
    def __init__(self, parent, quesNum):
        super().__init__(parent=parent)

        self.question = "Q%d: Question" % quesNum
        self.quesNum = quesNum

        for i in [1, 2 ,3]:
            exec('self.ans%d = "Answer %d"' % (i, i))

        self.setupUi()

    def setQuestion(self, question, ans):
        self.question = question
        self.quesLabel.setText("Q%d: %s" % (self.quesNum, self.question))

        for i in [1, 2 ,3]:
            exec('self.ans%d = ans[i-1]' \
                 '\nself.b%d.setText(self.ans%d)' % (i, i, i))

    def setupUi(self):
        quesLyt = QtWidgets.QVBoxLayout()

        self.quesLabel = QtWidgets.QLabel()
        self.quesLabel.setText(self.question)
        self.quesLabel.setStyleSheet("color: #FF0000; font-size: 20pt")
        quesLyt.addWidget(self.quesLabel)

        ansList = [1, 2 ,3]; shuffle(ansList)
        for i in ansList:
            exec('self.b%d = Button(self.ans%d, self, i == 1)' \
                 '\nquesLyt.addWidget(self.b%d)' % (i, i, i))

        imgLyt = QtWidgets.QVBoxLayout()

        self.image = QtWidgets.QLabel()
        self.image.setAlignment(Qt.AlignCenter)

        imgLyt.addWidget(self.image)

        Layout = QtWidgets.QGridLayout()
        Layout.addLayout(imgLyt, 0, 1)
        Layout.addLayout(quesLyt, 0, 0)

        self.setLayout(Layout)


class StartPage(QtWidgets.QWidget):
    """
    Start page widget
    """
    def __init__(self, parent):
        super().__init__(parent=parent)

        Layout = QtWidgets.QVBoxLayout()

        self.label = QtWidgets.QLabel()
        self.label.setText("Can you solve the following questions?\nAnswers must be in simplified form.")
        self.label.setStyleSheet("color: #FF0000; font-size: 20pt")
        Layout.addWidget(self.label)

        self.b0 = Button("Start", self, True)
        Layout.addWidget(self.b0)

        self.setLayout(Layout)


class FailedPage(QtWidgets.QWidget):
    """
    Page widget for failed answer
    """
    def __init__(self, parent):
        super().__init__(parent=parent)

        Layout = QtWidgets.QVBoxLayout()

        self.label = QtWidgets.QLabel()
        self.label.setText("Wrong answer. Better luck next time!")
        self.label.setStyleSheet("color: #FF0000; font-size: 20pt")
        Layout.addWidget(self.label)

        self.b0 = Button("Return", self, False)
        Layout.addWidget(self.b0)

        self.setLayout(Layout)


class FinalPage(QtWidgets.QWidget):
    """
    Victory page widget
    """
    def __init__(self, parent):
        super().__init__(parent=parent)

        layout = QtWidgets.QVBoxLayout()

        self.label = QtWidgets.QLabel()
        self.label.setStyleSheet("color: #FF0000; font-size: 20pt")
        layout.addWidget(self.label)

        self.b0 = Button("Return", self, False)
        layout.addWidget(self.b0)

        imgLyt = QtWidgets.QVBoxLayout()

        self.image = QtWidgets.QLabel()
        self.image.setAlignment(Qt.AlignCenter)

        imgLyt.addWidget(self.image)

        Layout = QtWidgets.QGridLayout()
        Layout.addLayout(imgLyt, 0, 1)
        Layout.addLayout(layout, 0, 0)

        self.setLayout(Layout)

    def setImage(self):
        self.image.setPixmap(QPixmap(getImage("Picture%d" % numQuestions)).scaledToHeight(580, Qt.SmoothTransformation))


class MainWindow(QtWidgets.QStackedWidget):
    """
    Main Window widget
    """
    def __init__(self):
        super().__init__()

        self.setMaximumHeight(600)
        self.setMinimumHeight(600)
        self.setMaximumWidth(800)
        self.setMinimumWidth(800)

        self.setWindowTitle("Who will win Maths?")
        self.setStyleSheet("background-image: url(%s)" % getImage("center"))


def main():
    style = QtWidgets.QStyleFactory.create("Fusion")

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle(style)

    window = MainWindow()

    w0 = StartPage(window)
    w1 = FinalPage(window)
    w2 = FailedPage(window)

    window.addWidget(w0)
    window.addWidget(w1)
    window.addWidget(w2)

    addQuestions(window)

    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
