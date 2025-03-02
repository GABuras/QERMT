# Author: George Adler Buras

import DataHandling

from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QLineEdit,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QComboBox,
    QStackedWidget,
    QHeaderView,
    QMessageBox
)
from PyQt6.QtGui import QIntValidator, QRegularExpressionValidator
from PyQt6 import QtCore
import csv
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.ticker as mtick
from matplotlib.text import Annotation

# TODO Create more breathing room

# TODO Double check "self"s

# TODO Don't crash when loading nothing

# Subclass QMainWindow to customize application's data entry window
class EntryWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.entryLayout = QVBoxLayout()

        # Meta Data Entry
        self.metaDataEntryLayout = QHBoxLayout()
        self.entryLayout.addLayout(self.metaDataEntryLayout)

        self.metaSpacingLabel = QLabel("")
        standardMetaDataFont = self.metaSpacingLabel.font()
        standardMetaDataFont.setPointSize(15)
        self.metaSpacingLabel.setFont(standardMetaDataFont)
        self.metaDataEntryLayout.addWidget(self.metaSpacingLabel)

        self.electionIDLabel = QLabel("Election ID:")
        self.electionIDLabel.setFont(standardMetaDataFont)
        self.metaDataEntryLayout.addWidget(self.electionIDLabel)

        self.standardLineEditWidth = 175
        self.standardLineEditHeight = 30

        self.electionIDField = QLineEdit()
        self.electionIDField.setValidator(QRegularExpressionValidator(QtCore.QRegularExpression("^[a-zA-Z0-9_-]+$")))
        self.electionIDField.setPlaceholderText("e.g. mm-dd-yy_Race")
        self.electionIDField.setFixedSize(self.standardLineEditWidth, self.standardLineEditHeight)
        self.metaDataEntryLayout.addWidget(self.electionIDField)

        self.metaDataEntryLayout.addWidget(self.metaSpacingLabel)
        
        self.votesCountedLabel = QLabel("[Expected] Number of Votes Counted:")
        self.votesCountedLabel.setFont(standardMetaDataFont)
        self.metaDataEntryLayout.addWidget(self.votesCountedLabel)

        # Max value is 2147483647 because signed int. To increase, must extend QIntValidator
        # https://forum.qt.io/topic/115662/qintvalidator-for-unsigned-long-values/3
        self.votesCountedField = QLineEdit()
        self.votesCountedField.setValidator(QIntValidator())
        self.votesCountedField.setPlaceholderText("e.g. 50000")
        self.votesCountedField.setFixedSize(self.standardLineEditWidth, self.standardLineEditHeight)
        self.metaDataEntryLayout.addWidget(self.votesCountedField)

        self.metaDataEntryLayout.addWidget(self.metaSpacingLabel)

        self.marginOfVictoryVotesLabel = QLabel("[Expected] Margin of Victory in Votes \U0001F6C8:")
        self.marginOfVictoryVotesLabel.setFont(standardMetaDataFont)
        self.marginOfVictoryVotesLabel.setToolTip("(First Place Votes - Second Place Votes)")
        self.metaDataEntryLayout.addWidget(self.marginOfVictoryVotesLabel)


        # This code makes the tooltip only appear when hovering over the info icon, but it destroys my formatting. 
        # Use if I ever swap to a grid layout
        # self.marginOfVictoryVotesLabel0 = QLabel("[Expected] Margin of Victory in Votes ")
        # self.marginOfVictoryVotesLabel0.setFont(standardMetaDataFont)
        # self.metaDataEntryLayout.addWidget(self.marginOfVictoryVotesLabel0)

        # self.marginOfVictoryVotesLabel1 = QLabel("\U0001F6C8")
        # self.marginOfVictoryVotesLabel1.setFont(standardMetaDataFont)
        # self.marginOfVictoryVotesLabel1.setToolTip("(First Place Votes - Second Place Votes)")
        # self.metaDataEntryLayout.addWidget(self.marginOfVictoryVotesLabel1)

        # self.marginOfVictoryVotesLabel2 = QLabel(":")
        # self.marginOfVictoryVotesLabel2.setFont(standardMetaDataFont)
        # self.metaDataEntryLayout.addWidget(self.marginOfVictoryVotesLabel2)





        # Max value is 2147483647 because signed int. To increase, must extend QIntValidator
        self.marginOfVictoryVotesField = QLineEdit()
        self.marginOfVictoryVotesField.setValidator(QIntValidator())
        self.marginOfVictoryVotesField.setPlaceholderText("e.g. 1000")
        self.marginOfVictoryVotesField.setFixedSize(self.standardLineEditWidth, self.standardLineEditHeight)
        self.metaDataEntryLayout.addWidget(self.marginOfVictoryVotesField)

        self.metaDataEntryLayout.addWidget(self.metaSpacingLabel)

        # Data Entry
        # TODO Validate data being entered. Are percentages percentages?
        self.dataEntryLayout = QHBoxLayout()
        self.entryLayout.addLayout(self.dataEntryLayout)
        
        self.dataTable = QTableWidget()

        self.dataTable.setColumnCount(7)
        self.initialRowCount = 20
        self.dataTable.setRowCount(self.initialRowCount)

        self.dataTableHeaderLabels = ["Risk Name", "Type of Vote Manipulation\n(Adding, Subtracting, or Changing)", "Probability of Manipulation\nOver 1 Election Cycle", "Lower Bound of Impact\n(95% Chance Value Is Higher)", "Upper Bound of Impact\n(95% Chance Value Is Lower)", "Total Cost of Controls", "Control Effectiveness"]
        self.dataTable.setHorizontalHeaderLabels(self.dataTableHeaderLabels)

        self.dataTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # TODO enforce % and $ on necesairy columns
        # for row in range(self.dataTable.rowCount()):
        #     for column in range(self.dataTable.columnCount()):
        #         self.dataTable.item(row, column).
                

        self.dataEntryLayout.addWidget(self.dataTable)

        # Buttons
        self.buttonsLayout = QHBoxLayout()
        self.entryLayout.addLayout(self.buttonsLayout)

        self.standardBtnWidth = 150
        self.standardBtnHeight = 50

        self.analyzeBtn = QPushButton("Analyze")
        self.analyzeBtn.clicked.connect(self.executeAnalyzeBtnClicked)
        self.analyzeBtn.setFixedSize(self.standardBtnWidth, self.standardBtnHeight)
        self.standardBtnFont = self.analyzeBtn.font()
        self.standardBtnFont.setPointSize(15)
        self.analyzeBtn.setFont(self.standardBtnFont)
        self.buttonsLayout.addWidget(self.analyzeBtn)

        self.saveBtn = QPushButton("Save")
        self.saveBtn.clicked.connect(self.executeSaveBtnClicked)
        self.saveBtn.setFixedSize(self.standardBtnWidth, self.standardBtnHeight)
        self.saveBtn.setFont(self.standardBtnFont)
        self.buttonsLayout.addWidget(self.saveBtn)

        self.loadBtn = QPushButton("Load")
        self.loadBtn.clicked.connect(self.executeLoadBtnClicked)
        self.loadBtn.setFixedSize(self.standardBtnWidth, self.standardBtnHeight)
        self.loadBtn.setFont(self.standardBtnFont)
        self.buttonsLayout.addWidget(self.loadBtn)

        # TODO Improve visual clarity: popup window when load/delete clicked with dropdown in it
        # electionID picker for loadBtn and deleteBtn
        self.electionIDDropdown = QComboBox()
        self.electionIDDropdown.setFixedSize(self.standardBtnWidth, self.standardBtnHeight)
        with open(f"./data/savedElectionIDs.csv", "r", newline='') as csvfile:
            savedElectionIDs = csv.reader(csvfile)
            for row in savedElectionIDs:
                self.electionIDDropdown.addItem(row[0])
        self.buttonsLayout.addWidget(self.electionIDDropdown)

        self.deleteBtn = QPushButton("Delete")
        self.deleteBtn.clicked.connect(self.executeDeleteBtnClicked)
        self.deleteBtn.setFixedSize(self.standardBtnWidth, self.standardBtnHeight)
        self.deleteBtn.setFont(self.standardBtnFont)
        self.buttonsLayout.addWidget(self.deleteBtn)        

        self.addBtn = QPushButton("Add Row")
        self.addBtn.clicked.connect(self.executeAddBtnClicked)
        self.addBtn.setFixedSize(self.standardBtnWidth, self.standardBtnHeight)
        self.addBtn.setFont(self.standardBtnFont)
        self.buttonsLayout.addWidget(self.addBtn)

        self.reduceBtn = QPushButton("Reduce Rows")
        self.reduceBtn.clicked.connect(self.executeReduceBtnClicked)
        self.reduceBtn.setFixedSize(self.standardBtnWidth, self.standardBtnHeight)
        self.reduceBtn.setFont(self.standardBtnFont)
        self.buttonsLayout.addWidget(self.reduceBtn)

        self.clearBtn = QPushButton("Clear All")
        self.clearBtn.clicked.connect(self.executeClearBtnClicked)
        self.clearBtn.setFixedSize(self.standardBtnWidth, self.standardBtnHeight)
        self.clearBtn.setFont(self.standardBtnFont)
        self.buttonsLayout.addWidget(self.clearBtn)


        self.widget = QWidget()
        self.widget.setLayout(self.entryLayout)
        self.setCentralWidget(self.widget)

    # Retreive all entered data, returns dataProfile
    def getEnteredData(self):
        try:
            votesCounted = int(self.votesCountedField.text())
        except ValueError: 
            QMessageBox.warning(self, "ERROR", "Number of Votes Counted must be filled", buttons=QMessageBox.StandardButton.Ok)
            return None

        try:
            marginOfVictoryVotes = int(self.marginOfVictoryVotesField.text())
        except ValueError:
            QMessageBox.warning(self, "ERROR", "Margin of Victory must be filled", buttons=QMessageBox.StandardButton.Ok)
            return None

        # Delete excees rows 
        emptyRows = []
        for row in range(self.dataTable.rowCount()):
            if self.dataTable.item(row, 0) is None and self.dataTable.item(row, 1) is None and self.dataTable.item(row, 2) is None and self.dataTable.item(row, 3) is None and self.dataTable.item(row, 4) is None and self.dataTable.item(row, 5) is None and self.dataTable.item(row, 6) is None:
                emptyRows.append(row)
        emptyRows.reverse()
        for row in emptyRows:
            self.dataTable.removeRow(row)

        # Read data into variable
        data = []
        for row in range(self.dataTable.rowCount()):
            risk = [row+1]
            for column in range(self.dataTable.columnCount()):
                try:
                    risk.append(self.dataTable.item(row, column).text())
                except AttributeError:
                    QMessageBox.warning(self, "ERROR", "Rows must be completely filled", buttons=QMessageBox.StandardButton.Ok)
                    return None
            data.append(risk)

        # correct data formatting
        # TODO 80% to .8, after I figure out enforcing %        
        for risk in data:
            try:
                risk[3] = float(risk[3])
            except ValueError:
                QMessageBox.warning(self, "ERROR", "Probability of Manipulation must be a percentage", buttons=QMessageBox.StandardButton.Ok)
                return None
            try:
                risk[4] = int(risk[4])
            except ValueError:
                QMessageBox.warning(self, "ERROR", "Lower Bound of Impact must be a whole number", buttons=QMessageBox.StandardButton.Ok)
                return None
            try:
                risk[5] = int(risk[5])
            except ValueError:
                QMessageBox.warning(self, "ERROR", "Upper Bound of Impact must be a whole number", buttons=QMessageBox.StandardButton.Ok)
                return None
            try:
                risk[6] = float(risk[6])
            except ValueError:
                QMessageBox.warning(self, "ERROR", "Total Cost of Controls should be a monetary amount", buttons=QMessageBox.StandardButton.Ok)
                return None
            try:
                risk[7] = float(risk[7])
            except ValueError:
                QMessageBox.warning(self, "ERROR", "Control Effectiveness must be a percentage", buttons=QMessageBox.StandardButton.Ok)
                return None
        return [votesCounted, marginOfVictoryVotes, data]

    # TODO Create a new page with LEC and control ranking and swap to it
    # Read all entered data into LEC Generator
    def executeAnalyzeBtnClicked(self):
        dataProfile = self.getEnteredData()
        # Error handling
        if dataProfile is None:
            return

        AnalysisWindow.displayInfo(analysisPage, dataProfile)
        pages.setCurrentWidget(analysisPage)

    # Save all entered data 
    def executeSaveBtnClicked(self):
        # input validation: no ''
        electionID = self.electionIDField.text()
        if electionID == '':
            QMessageBox.warning(self, "ERROR", "Election ID must be filled", buttons=QMessageBox.StandardButton.Ok)
            return

        dataProfile = self.getEnteredData()
        # Error handling
        if dataProfile is None:
            return

        DataHandling.saveData(electionID, dataProfile)
        if(self.electionIDDropdown.findText(electionID) == -1):
            self.electionIDDropdown.addItem(electionID)
        
        index = self.electionIDDropdown.findText(electionID)
        if index != -1: 
            self.electionIDDropdown.setCurrentIndex(index)

    # Load all data from csv files
    def executeLoadBtnClicked(self):
        dataProfile = DataHandling.loadData(self.electionIDDropdown.currentText())
        # Set:
        # Election ID
        self.electionIDField.clear()
        self.electionIDField.insert(self.electionIDDropdown.currentText())
        # Votes Counted
        self.votesCountedField.clear()
        self.votesCountedField.insert(str(dataProfile[0]))
        # Margin of Victory
        self.marginOfVictoryVotesField.clear()
        self.marginOfVictoryVotesField.insert(str(dataProfile[1]))
        # Data Table
        data = dataProfile[2]
        self.dataTable.clearContents()
        self.dataTable.setRowCount(len(data))
        for row in range(len(data)):
            for column in range(1, len(data[0])):
                self.dataTable.setItem(row, column-1, QTableWidgetItem(str(data[row][column])))
                
    def executeDeleteBtnClicked(self):
        DataHandling.deleteData(self.electionIDDropdown.currentText())
        self.electionIDDropdown.removeItem(self.electionIDDropdown.currentIndex())
        self.executeClearBtnClicked()
        self.dataTable.setRowCount(self.initialRowCount)

    # TODO Change to add row below selected row; if none selected, default to bottom
    def executeAddBtnClicked(self):
        self.dataTable.insertRow(self.dataTable.rowCount())

    # TODO Change to delete selected row; if none selected, default to bottom
    def executeReduceBtnClicked(self):
        self.dataTable.removeRow(self.dataTable.rowCount()-1)

    def executeClearBtnClicked(self):
        self.electionIDField.clear()
        self.votesCountedField.clear()
        self.marginOfVictoryVotesField.clear()
        self.dataTable.clearContents()

class AnalysisWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.analysisLayout = QVBoxLayout()

        # Information
        self.infoLayout = QHBoxLayout()
        self.analysisLayout.addLayout(self.infoLayout)

        # Loss Exceedance Curve
        self.lossExceedanceCurveCanvas = FigureCanvas(Figure())
        self.lossExceedanceCurveAx = self.lossExceedanceCurveCanvas.figure.subplots()
        self.xValues = []
        self.yValues = []
        self.line, = self.lossExceedanceCurveAx.plot(self.xValues, self.yValues)

        self.lossExceedanceCurveAx.set_title("Loss Exceedance Curve")
        self.lossExceedanceCurveAx.set_xlabel("Margin of Manipulation (Manipulated Votes / Counted Votes)")
        self.lossExceedanceCurveAx.set_ylabel("Chance of Margin of Manipulation or Greater")
        self.lossExceedanceCurveAx.grid(True, which='both', linestyle='--', color='gray', linewidth=0.5)

        self.marginOfVictoryAnnotation = Annotation("temp", (0,0))
        self.lossExceedanceCurveAx.add_artist(self.marginOfVictoryAnnotation)

        self.graphLayout = QVBoxLayout()
        self.graphLayout.addWidget(self.lossExceedanceCurveCanvas)

        self.graphToolbar = NavigationToolbar(self.lossExceedanceCurveCanvas, self)
        self.graphLayout.addWidget(self.graphToolbar)

        self.infoLayout.addLayout(self.graphLayout)

        # Control ranking Table
        self.controlRankingTable = QTableWidget()

        self.controlRankingTable.setColumnCount(6)
        self.controlRankingTableHeaderLabels = ["Risk ID", "Risk Name", "Total Cost of Controls", "Control Effectiveness", "Votes/Dollar \U0001F6C8", "Dollars/Vote \U0001F6C8"]
        self.controlRankingTable.setHorizontalHeaderLabels(self.controlRankingTableHeaderLabels)
        # self.controlRankingTable.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.controlRankingTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Add tooltip to last two column headers
        self.controlRankingTable.horizontalHeaderItem(4).setToolTip("The average number of manipulated votes mitigated per dollar spent if all controls for this risk are implemented")
        self.controlRankingTable.horizontalHeaderItem(5).setToolTip("The average cost of mitigating a single manipulated vote if all controls for this risk are implemented")


        # TODO Enforce % and $ on necessary columns

        self.infoLayout.addWidget(self.controlRankingTable)


        # TODO Buttons to swap view between LEC, Control Ranking, and both
        # Buttons
        self.buttonsLayout = QHBoxLayout()
        self.analysisLayout.addLayout(self.buttonsLayout)

        self.standardBtnWidth = 150
        self.standardBtnHeight = 50

        self.backBtn = QPushButton("Back")
        self.backBtn.clicked.connect(self.executeBackBtnClicked)
        self.backBtn.setFixedSize(self.standardBtnWidth, self.standardBtnHeight)
        self.standardBtnFont = self.backBtn.font()
        self.standardBtnFont.setPointSize(15)
        self.backBtn.setFont(self.standardBtnFont)
        self.analysisLayout.addWidget(self.backBtn)

        # TODO Rerun Simulations Button
    
        # TODO Variable number of simulations

        self.widget = QWidget()
        self.widget.setLayout(self.analysisLayout)
        self.setCentralWidget(self.widget)

    def displayInfo(self, dataProfile):
        self.votesCounted = dataProfile[0]
        self.marginOfVictoryVotes = dataProfile[1]

        # Loss Exceedance Curve
        analysisValues = DataHandling.analyzeData(dataProfile)
        self.xValues = analysisValues[0] 
        self.yValues = analysisValues[1]
        self.marginOfVictoryPercentage = analysisValues[2]
        self.marginOfVictoryY = analysisValues[3]
        self.controlRanking = analysisValues[4]

        self.line.set_data(self.xValues, self.yValues)

        self.lossExceedanceCurveAx.set_xlim(min(self.xValues), max(self.xValues))
        self.lossExceedanceCurveAx.set_ylim(0, max(self.yValues) + 0.01)

        self.lossExceedanceCurveAx.xaxis.set_major_formatter(mtick.PercentFormatter(1))
        self.lossExceedanceCurveAx.yaxis.set_major_formatter(mtick.PercentFormatter(1))

        # Add second x axis scale for "Manipulated Votes"
        self.lossExceedanceCurveSecAx = self.lossExceedanceCurveAx.secondary_xaxis('top', functions=(lambda x: x*self.votesCounted, lambda x: x/self.votesCounted))
        self.lossExceedanceCurveSecAx.set_xlabel("Manipulated Votes")
        # TODO Improve formatting when Manipulated Votes enters e teritory
        # self.lossExceedanceCurveSecAx.xaxis.set_major_formatter(...)

        # Label Margin of Victory Percentage
        # TODO Improve to look good regardless of data
        self.marginOfVictoryAnnotation.remove()
        self.marginOfVictoryAnnotation = Annotation("Margin of Victory\n(%.4f%%, %.4f%%)"%(self.marginOfVictoryPercentage*100, self.marginOfVictoryY*100), xy=(self.marginOfVictoryPercentage, self.marginOfVictoryY), xytext=(self.marginOfVictoryPercentage-0.005, self.marginOfVictoryY+0.15), arrowprops=dict(facecolor = 'red', shrink = 0.05),)
        self.lossExceedanceCurveAx.add_artist(self.marginOfVictoryAnnotation)

        self.line.figure.canvas.draw()

        # Display Control Ranking
        self.controlRankingTable.clearContents()
        self.controlRankingTable.setRowCount(len(self.controlRanking))

        for row in range(len(self.controlRanking)):
            for column in range(len(self.controlRanking[0])):
                # self.controlRankingTable.setItem(row, column, QTableWidgetItem(str(self.controlRanking[row][column])))
                
                item = QTableWidgetItem()
                item.setText(str(self.controlRanking[row][column]))
                item.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEnabled)
                self.controlRankingTable.setItem(row, column, item)
        # self.controlRankingTable.resizeColumnsToContents()



    def executeBackBtnClicked(self):
        pages.setCurrentWidget(entryPage)



if __name__ == '__main__':
    # Create an instance of Qapplication
    app = QApplication([])

    pages = QStackedWidget()
    pages.setWindowTitle("QERMT")

    entryPage = EntryWindow()
    pages.addWidget(entryPage)

    analysisPage =  AnalysisWindow()
    pages.addWidget(analysisPage)

    pages.setCurrentWidget(entryPage)
    pages.showMaximized()

    # Start the event loop.
    app.exec()
