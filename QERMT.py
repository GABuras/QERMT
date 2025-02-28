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
    QStackedWidget
)
from PyQt6.QtGui import QIntValidator
import csv
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.ticker as mtick
from matplotlib.text import Annotation

# TODO Either make table stretech all the way across, or move buttons to right side

# TODO Create more breathing room

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

        # TODO do I need these labels, or can I do like:
        # layout = QFormLayout()
        # layout.addRow("Integers:", self.int_line_edit)
        # layout.addRow("Uppercase letters:", self.uppercase_line_edit)
        # layout.addRow("Signal:", self.signal_label)
        # self.setLayout(layout)

        self.electionIDLabel = QLabel("Election ID:")
        self.electionIDLabel.setFont(standardMetaDataFont)
        self.metaDataEntryLayout.addWidget(self.electionIDLabel)

        self.standardLineEditWidth = 175
        self.standardLineEditHeight = 30

        # TODO only accept str
        self.electionIDField = QLineEdit()
        self.electionIDField.setPlaceholderText("e.g. mm/dd/yy Race")
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

        # TODO Improve ToolTip; it's too slow and appearing below is not ideal
        self.marginOfVictoryVotesLabel = QLabel("[Expected] Margin of Victory in Votes*:")
        self.marginOfVictoryVotesLabel.setFont(standardMetaDataFont)
        self.marginOfVictoryVotesLabel.setToolTip("(First Place Votes - Second Place Votes)")
        self.metaDataEntryLayout.addWidget(self.marginOfVictoryVotesLabel)

        # Max value is 2147483647 because signed int. To increase, must extend QIntValidator
        self.marginOfVictoryVotesField = QLineEdit()
        self.marginOfVictoryVotesField.setValidator(QIntValidator())
        self.marginOfVictoryVotesField.setPlaceholderText("e.g. 1000")
        self.marginOfVictoryVotesField.setFixedSize(self.standardLineEditWidth, self.standardLineEditHeight)
        self.metaDataEntryLayout.addWidget(self.marginOfVictoryVotesField)

        self.metaDataEntryLayout.addWidget(self.metaSpacingLabel)

        # Data Entry
        # TODO Validate data being entered (QItemDelegate? inputmask? for line edit)
        self.dataEntryLayout = QHBoxLayout()
        self.entryLayout.addLayout(self.dataEntryLayout)
        
        self.dataTable = QTableWidget()

        self.dataTable.setColumnCount(7)
        self.initialRowCount = 20
        self.dataTable.setRowCount(self.initialRowCount)

        self.dataTableHeaderLabels = ["Risk Name", "Type of Vote Manipulation\n(Adding, Subtracting, or Changing)", "Probability of Manipulation\nOver 1 Election Cycle", "Lower Bound of Impact\n(95% Chance Value Is Higher)", "Upper Bound of Impact\n(95% Chance Value Is Lower)", "Total Cost of Controls", "Control Effectiveness"]
        self.dataTable.setHorizontalHeaderLabels(self.dataTableHeaderLabels)

        for c in range(len(self.dataTableHeaderLabels)):
            self.dataTable.setColumnWidth(c, 200)

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

        # TODO Improve visual clarity
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

    # TODO Improve error handling

    # Retreive all entered data, returns dataProfile
    def getEnteredData(self):
        votesCounted = int(self.votesCountedField.text())
        marginOfVictoryVotes = int(self.marginOfVictoryVotesField.text())
        # TODO delete excees rows 
        # TODO error message if important columns missing data/incorrect data type
        data = []
        for row in range(self.dataTable.rowCount()):
            risk = [row+1]
            for column in range(self.dataTable.columnCount()):
                risk.append(self.dataTable.item(row, column).text())
            data.append(risk)

        # correct data formatting
        for risk in data:
            risk[0] = int(risk[0])
            risk[3] = float(risk[3])
            risk[4] = int(risk[4])
            risk[5] = int(risk[5])
            risk[6] = int(risk[6])
            risk[7] = float(risk[7])

        return [votesCounted, marginOfVictoryVotes, data]

    # TODO Create a new page with LEC and control ranking and swap to it
    # Read all entered data into LEC Generator
    def executeAnalyzeBtnClicked(self):
        AnalysisWindow.displayInfo(analysisPage)
        pages.setCurrentWidget(analysisPage)

    # Save all entered data 
    def executeSaveBtnClicked(self):
        electionID = self.electionIDField.text()
        DataHandling.saveData(electionID, self.getEnteredData())
        if(self.electionIDDropdown.findText(electionID) == -1):
            self.electionIDDropdown.addItem(electionID)

    # Load all data from csv files
    def executeLoadBtnClicked(self):
        dataProfile = DataHandling.loadData(self.electionIDDropdown.currentText())
        # Set:
        # Election ID
        self.electionIDField.clear()
        self.electionIDField.insert(self.electionIDDropdown.currentText()) # TODO Why is this appending instead or replacing like the others?
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


        # TODO Consider ...Figure(tight_layout=True)
        self.lossExceedanceCurveCanvas = FigureCanvas(Figure())
        self.lossExceedanceCurveAx = self.lossExceedanceCurveCanvas.figure.subplots()
        self.xValues = []
        self.yValues = []
        self.line, = self.lossExceedanceCurveAx.plot(self.xValues, self.yValues)

        # TODO LEC Formatting
        # self.lossExceedanceCurveAx.annotate("Margin of Victory\n(%.4f%%, %.4f%%)"%(marginOfVictoryPercentage*100, marginOfVictoryY*100), xy=(marginOfVictoryPercentage, marginOfVictoryY), xytext=(marginOfVictoryPercentage-0.005, marginOfVictoryY+0.15), arrowprops=dict(facecolor = 'red', shrink = 0.05),)
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

        self.widget = QWidget()
        self.widget.setLayout(self.analysisLayout)
        self.setCentralWidget(self.widget)

    def displayInfo(self):
        self.dataProfile = entryPage.getEnteredData()
        self.votesCounted = self.dataProfile[0]
        self.marginOfVictoryVotes = self.dataProfile[1]

        # Loss Exceedance Curve
        graphValues = DataHandling.analyzeData(self.dataProfile)
        self.xValues = graphValues[0] 
        self.yValues = graphValues[1]
        self.marginOfVictoryPercentage = graphValues[2]
        self.marginOfVictoryY = graphValues[3]

        self.line.set_data(self.xValues, self.yValues)

        self.lossExceedanceCurveAx.set_xlim(min(self.xValues), max(self.xValues))
        self.lossExceedanceCurveAx.set_ylim(0, max(self.yValues) + 0.01)

        self.lossExceedanceCurveAx.xaxis.set_major_formatter(mtick.PercentFormatter(1))
        self.lossExceedanceCurveAx.yaxis.set_major_formatter(mtick.PercentFormatter(1))

        # Label Margin of Victory Percentage
        self.marginOfVictoryAnnotation.remove()
        self.marginOfVictoryAnnotation = Annotation("Margin of Victory\n(%.4f%%, %.4f%%)"%(self.marginOfVictoryPercentage*100, self.marginOfVictoryY*100), xy=(self.marginOfVictoryPercentage, self.marginOfVictoryY), xytext=(self.marginOfVictoryPercentage-0.005, self.marginOfVictoryY+0.15), arrowprops=dict(facecolor = 'red', shrink = 0.05),)
        self.lossExceedanceCurveAx.add_artist(self.marginOfVictoryAnnotation)

        self.line.figure.canvas.draw()

        # TODO Replace graph instead of adding another one
        # Can I simply move everything to init except lossExceedance Curve Update?

        # TODO Display Control Ranking



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

    # Create and display main window
    # window = MainWindow()
    # window.showMaximized()

    # Start the event loop.
    app.exec()
