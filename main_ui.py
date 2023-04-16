# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cosik.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets

import GenAlg.run_genetic_algorithm
from GenAlg import shared_types
from DataGeneration import generate_data

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.lineEdit_5 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_5.setGeometry(QtCore.QRect(40, 100, 113, 22))
        self.lineEdit_5.setObjectName("lineEdit_5")

        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(40, 80, 111, 16))
        self.label_5.setObjectName("label_5")

        self.lineEdit_6 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_6.setGeometry(QtCore.QRect(170, 100, 113, 22))
        self.lineEdit_6.setObjectName("lineEdit_6")

        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(170, 80, 81, 16))
        self.label_6.setObjectName("label_6")

        self.lineEdit_7 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_7.setGeometry(QtCore.QRect(300, 100, 113, 22))
        self.lineEdit_7.setObjectName("lineEdit_7")

        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(300, 80, 81, 16))
        self.label_7.setObjectName("label_7")

        self.lineEdit_8 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_8.setGeometry(QtCore.QRect(660, 40, 113, 22))
        self.lineEdit_8.setObjectName("lineEdit_8")

        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(660, 20, 121, 16))
        self.label_8.setObjectName("label_8")

        self.lineEdit_9 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_9.setGeometry(QtCore.QRect(660, 90, 113, 22))
        self.lineEdit_9.setObjectName("lineEdit_9")

        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(660, 70, 111, 16))
        self.label_9.setObjectName("label_9")

        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(660, 130, 111, 16))
        self.label_10.setObjectName("label_10")

        self.lineEdit_10 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_10.setGeometry(QtCore.QRect(660, 150, 113, 22))
        self.lineEdit_10.setObjectName("lineEdit_10")

        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(660, 210, 111, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItems([selection.name for selection in shared_types.Selection])

        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(660, 190, 111, 16))
        self.label_11.setObjectName("label_11")

        self.comboBox_2 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_2.setGeometry(QtCore.QRect(660, 260, 111, 22))
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItems([crossover.name for crossover in shared_types.Crossover])

        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setGeometry(QtCore.QRect(660, 240, 111, 16))
        self.label_12.setObjectName("label_12")

        self.comboBox_3 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_3.setGeometry(QtCore.QRect(660, 310, 111, 22))
        self.comboBox_3.setObjectName("comboBox_3")
        self.comboBox_3.addItems([mutation.name for mutation in shared_types.Mutation])

        self.label_13 = QtWidgets.QLabel(self.centralwidget)
        self.label_13.setGeometry(QtCore.QRect(660, 290, 111, 16))
        self.label_13.setObjectName("label_13")

        self.label_14 = QtWidgets.QLabel(self.centralwidget)
        self.label_14.setGeometry(QtCore.QRect(430, 80, 161, 16))
        self.label_14.setObjectName("label_14")

        self.lineEdit_11 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_11.setGeometry(QtCore.QRect(430, 100, 113, 22))
        self.lineEdit_11.setObjectName("lineEdit_11")

        self.start_button = QtWidgets.QPushButton(self.centralwidget)
        self.start_button.setGeometry(QtCore.QRect(430, 140, 113, 22))
        self.start_button.setObjectName("button_start")
        self.start_button.clicked.connect(self.start_algorithm)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def get_selection(self):
        return self.comboBox.currentText()

    def get_crossover(self):
        return self.comboBox_2.currentText()

    def get_mutation(self):
        return self.comboBox_3.currentText()

    def get_classrooms(self):
        return generate_data.generate_classrooms(int(self.lineEdit.text()))

    def start_algorithm(self):
        solution = GenAlg.run_genetic_algorithm.run_genetic_algorithm(20, int(self.lineEdit_10.text()),
                                                           getattr(shared_types.Selection, self.get_selection()),
                                                           getattr(shared_types.Mutation, self.get_mutation()),
                                                           getattr(shared_types.Crossover, self.get_crossover()))
        solution[0].display()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_5.setText(_translate("MainWindow", "Waga czasu pracy"))
        self.label_6.setText(_translate("MainWindow", "Waga slotu"))
        self.label_7.setText(_translate("MainWindow", "Waga ucznia"))
        self.label_8.setText(_translate("MainWindow", "Prawd. krzyżowania"))
        self.label_9.setText(_translate("MainWindow", "Prawd. mutacji"))
        self.label_10.setText(_translate("MainWindow", "Max iteracji"))
        self.label_11.setText(_translate("MainWindow", "Selekcja"))
        self.label_12.setText(_translate("MainWindow", "Krzyżowanie"))
        self.label_13.setText(_translate("MainWindow", "Mutacja"))
        self.label_14.setText(_translate("MainWindow", "Prawd. połączenia grup"))
        self.start_button.setText(_translate("MainWindow", "Start"))
