""" Define the contents of control panel. """

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QFrame, QHBoxLayout, QVBoxLayout, QFormLayout,
                             QComboBox, QDoubleSpinBox, QGroupBox, QPushButton,
                             QLabel, QRadioButton, QTextEdit, QCheckBox)

from display_panel import DisplayFrame
from fuzzier_viewer import FuzzierViewer
from car import Car
from run import RunCar


class ControlFrame(QFrame):

    def __init__(self, dataset, display_panel):
        super().__init__()
        if isinstance(display_panel, DisplayFrame):
            self.display_panel = display_panel
        else:
            raise TypeError("'display_panel' must be the instance of "
                            "'DisplayFrame'")
        self.dataset = dataset

        self.__car = None
        self.__thread = None

        self.__layout = QVBoxLayout()
        self.setLayout(self.__layout)
        self.__layout.setContentsMargins(0, 0, 0, 0)

        self.__setCaseComboboxUI()
        self.__setFuzzySetOperationTypeUI()
        self.__setFuzzyVariableUI()
        self.__setConsoleUI()

    def __setCaseComboboxUI(self):
        group_box = QGroupBox("Case Data Selection")
        inner_layout = QHBoxLayout()
        group_box.setLayout(inner_layout)

        self.data_selector = QComboBox(group_box)
        self.data_selector.addItems(self.dataset.keys())
        self.data_selector.setStatusTip("Select the road map case.")
        self.data_selector.currentIndexChanged.connect(self.__change_map)

        self.start_btn = QPushButton("Run")
        self.start_btn.setStatusTip("Run the car.")
        self.start_btn.clicked.connect(self.__run)

        self.stop_btn = QPushButton("Stop")
        self.stop_btn.setStatusTip("Force the simulation stop running.")
        self.stop_btn.setDisabled(True)

        self.__change_map()
        inner_layout.addWidget(self.data_selector, 1)
        inner_layout.addWidget(self.start_btn)
        inner_layout.addWidget(self.stop_btn)

        self.__layout.addWidget(group_box)

    def __setFuzzySetOperationTypeUI(self):
        group_box = QGroupBox("Fuzzy Sets Operation Types")
        inner_layout = QFormLayout()
        group_box.setLayout(inner_layout)

        self.composition_tnorm_selection = RadioButtonSet({
            "tn_min": QRadioButton("Minimum"),
            "tn_ap": QRadioButton("Algebraic Product"),
            "tn_bp": QRadioButton("Bounded Product"),
            "tn_dp": QRadioButton("Drastic Product")
        })
        self.composition_tconorm_selection = RadioButtonSet({
            "tc_max": QRadioButton("Maximum"),
            "tc_as": QRadioButton("Algebraic Sum"),
            "tc_bs": QRadioButton("Bounded Sum"),
            "tc_ds": QRadioButton("Drastic Sum")
        })
        self.implication_selections = RadioButtonSet({
            "imp_dr": QRadioButton("Dienes-Rescher"),
            "imp_l": QRadioButton("Lukasieweicz"),
            "imp_z": QRadioButton("Zadel"),
            "imp_g": QRadioButton("Godel"),
            "imp_m": QRadioButton("Mamdani"),
            "imp_p": QRadioButton("Product")
        })
        self.vars_combine_selection = RadioButtonSet({
            "tn_min": QRadioButton("Minimum"),
            "tn_ap": QRadioButton("Algebraic Product"),
            "tn_bp": QRadioButton("Bounded Product"),
            "tn_dp": QRadioButton("Drastic Product")
        })
        self.rules_combine_selection = RadioButtonSet({
            "tc_max": QRadioButton("Maximum"),
            "tc_as": QRadioButton("Algebraic Sum"),
            "tc_bs": QRadioButton("Bounded Sum"),
            "tc_ds": QRadioButton("Drastic Sum")
        })

        self.composition_tnorm_selection.setStatusTip("Choose the method of "
                                                      "t-norm for fuzzy "
                                                      "composition.")
        self.composition_tconorm_selection.setStatusTip("Choose the method of "
                                                        "t-conorm for fuzzy "
                                                        "composition.")
        self.implication_selections.setStatusTip("Choose the methods for fuzzy "
                                                 "implication.")
        self.vars_combine_selection.setStatusTip("Choose the methods of "
                                                 "combination of multiple fuzzy "
                                                 "variables.")
        self.rules_combine_selection.setStatusTip("Choose the methods of "
                                                  "combination of multiple fuzzy "
                                                  "rules.")

        inner_layout.addRow(QLabel("Composition T-Norm:"),
                            self.composition_tnorm_selection)
        inner_layout.addRow(QLabel("Composition T-Conorm:"),
                            self.composition_tconorm_selection)
        inner_layout.addRow(QLabel("Implication:"),
                            self.implication_selections)
        inner_layout.addRow(QLabel("Combination of Variables:"),
                            self.vars_combine_selection)
        inner_layout.addRow(QLabel("Combination of Rules:"),
                            self.rules_combine_selection)

        self.__layout.addWidget(group_box)

    def __setFuzzyVariableUI(self):
        self.in_fuzzyvar_setting = FuzzierVarSetting("Input Fuzzy Variables")
        self.out_fuzzyvar_setting = FuzzierVarSetting("Output Fuzzy Varaibles")
        self.__layout.addWidget(self.in_fuzzyvar_setting)
        self.__layout.addWidget(self.out_fuzzyvar_setting)

    def __setConsoleUI(self):
        self.__console = QTextEdit()
        self.__console.setReadOnly(True)
        self.__console.setStatusTip("Show the logs of status changing.")
        self.__layout.addWidget(self.__console)

    @pyqtSlot()
    def __change_map(self):
        current_data = self.dataset[self.data_selector.currentText()]
        self.__car = Car(current_data['start_pos'],
                         current_data['start_angle'],
                         3,
                         current_data['route_edge'])
        self.display_panel.change_map(current_data)

    @pyqtSlot(str)
    def __print_console(self, text):
        self.__console.append(text)

    @pyqtSlot()
    def __init_widgets(self):
        self.start_btn.setDisabled(True)
        self.stop_btn.setEnabled(True)
        self.data_selector.setDisabled(True)
        self.composition_tnorm_selection.setDisabled(True)
        self.composition_tconorm_selection.setDisabled(True)
        self.implication_selections.setDisabled(True)
        self.vars_combine_selection.setDisabled(True)
        self.rules_combine_selection.setDisabled(True)
        self.in_fuzzyvar_setting.setDisabled(True)
        self.out_fuzzyvar_setting.setDisabled(True)

    @pyqtSlot()
    def __reset_widgets(self):
        self.start_btn.setEnabled(True)
        self.stop_btn.setDisabled(True)
        self.data_selector.setEnabled(True)
        self.composition_tnorm_selection.setEnabled(True)
        self.composition_tconorm_selection.setEnabled(True)
        self.implication_selections.setEnabled(True)
        self.vars_combine_selection.setEnabled(True)
        self.rules_combine_selection.setEnabled(True)
        self.in_fuzzyvar_setting.setEnabled(True)
        self.out_fuzzyvar_setting.setEnabled(True)

    @pyqtSlot()
    def __run(self):
        self.__thread = RunCar(self.__car)
        self.__thread.started.connect(self.__init_widgets)
        self.__thread.finished.connect(self.__reset_widgets)
        self.__thread.sig_console.connect(self.__print_console)
        self.__thread.sig_car.connect(self.display_panel.move_car)
        self.__thread.sig_dists.connect(self.display_panel.show_dists)
        self.__thread.start()

class RadioButtonSet(QFrame):
    def __init__(self, named_radiobtns):
        super().__init__()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        self.named_radiobtns = named_radiobtns
        next(iter(self.named_radiobtns.values())).toggle()
        for radiobtn in self.named_radiobtns.values():
            layout.addWidget(radiobtn)


class FuzzierVarSetting(QGroupBox):
    def __init__(self, name):
        super().__init__(name)
        self.__layout = QFormLayout()
        self.setLayout(self.__layout)

        self.small = GaussianFuzzierSetting()
        self.medium = GaussianFuzzierSetting()
        self.large = GaussianFuzzierSetting()

        self.__layout.addRow(QLabel("Small:"), self.small)
        self.__layout.addRow(QLabel("Medium:"), self.medium)
        self.__layout.addRow(QLabel("Large:"), self.large)

        self.viewer = FuzzierViewer()

        self.__layout.addRow(self.viewer)

        self.small.mean.setValue(0)
        self.medium.mean.setValue(5)
        self.large.mean.setValue(10)

        self.update_viewer()

        self.small.mean.valueChanged.connect(self.update_viewer)
        self.small.sd.valueChanged.connect(self.update_viewer)
        self.small.ascending.stateChanged.connect(self.update_viewer)
        self.small.descending.stateChanged.connect(self.update_viewer)
        self.medium.mean.valueChanged.connect(self.update_viewer)
        self.medium.sd.valueChanged.connect(self.update_viewer)
        self.medium.ascending.stateChanged.connect(self.update_viewer)
        self.medium.descending.stateChanged.connect(self.update_viewer)
        self.large.mean.valueChanged.connect(self.update_viewer)
        self.large.sd.valueChanged.connect(self.update_viewer)
        self.large.ascending.stateChanged.connect(self.update_viewer)
        self.large.descending.stateChanged.connect(self.update_viewer)

    def setDisabled(self, boolean):
        self.small.setDisabled(boolean)
        self.medium.setDisabled(boolean)
        self.large.setDisabled(boolean)

    def setEnabled(self, boolean):
        self.small.setEnabled(boolean)
        self.medium.setEnabled(boolean)
        self.large.setEnabled(boolean)

    @pyqtSlot()
    def update_viewer(self):
        means = [self.small.mean.value(),
                 self.medium.mean.value(),
                 self.large.mean.value()]
        sds = [self.small.sd.value(),
               self.medium.sd.value(),
               self.large.sd.value()]
        ascendings = [self.small.ascending.isChecked(),
                      self.medium.ascending.isChecked(),
                      self.large.ascending.isChecked()]
        descendings = [self.small.descending.isChecked(),
                       self.medium.descending.isChecked(),
                       self.large.descending.isChecked()]
        self.viewer.remove_curves()
        self.viewer.add_curves(means, sds, ascendings, descendings)


class GaussianFuzzierSetting(QFrame):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout()

        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        self.mean = QDoubleSpinBox()
        self.mean.setMinimum(-100)
        self.mean.setStatusTip("The mean (mu) value for Gaussian function.")

        self.sd = QDoubleSpinBox()
        self.sd.setDecimals(3)
        self.sd.setValue(2)
        self.sd.setMinimum(0.1)
        self.sd.setStatusTip("The standard deviation (sigma) value for "
                             "Gaussian function.")

        self.ascending = QCheckBox()
        self.ascending.setIcon(QIcon('icons/ascending_icon.png'))
        self.ascending.setStatusTip("Make the fuzzier strictly ascending.")
        self.descending = QCheckBox()
        self.descending.setIcon(QIcon('icons/descending_icon.png'))
        self.descending.setStatusTip("Make the fuzzier strictly descending.")

        layout.addWidget(QLabel("Mean"))
        layout.addWidget(self.mean, 1)
        layout.addWidget(QLabel("Standard Deviation"))
        layout.addWidget(self.sd, 1)
        layout.addWidget(self.ascending)
        layout.addWidget(self.descending)
