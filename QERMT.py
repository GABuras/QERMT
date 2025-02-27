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
    QComboBox
)
import csv

# Subclass QMainWindow to customize application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QERMT")

        self.layout = QVBoxLayout()

        # Meta Data Entry
        self.metaDataEntryLayout = QHBoxLayout()
        self.layout.addLayout(self.metaDataEntryLayout)

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
        self.electionIDField.setPlaceholderText("e.g. mm/dd/yy Race")
        self.electionIDField.setFixedSize(self.standardLineEditWidth, self.standardLineEditHeight)
        self.metaDataEntryLayout.addWidget(self.electionIDField)

        self.metaDataEntryLayout.addWidget(self.metaSpacingLabel)
        
        self.votesCountedLabel = QLabel("[Expected] Number of Votes Counted:")
        self.votesCountedLabel.setFont(standardMetaDataFont)
        self.metaDataEntryLayout.addWidget(self.votesCountedLabel)

        # TODO input validation
        self.votesCountedField = QLineEdit()
        self.votesCountedField.setPlaceholderText("e.g. 50000")
        self.votesCountedField.setFixedSize(self.standardLineEditWidth, self.standardLineEditHeight)
        self.metaDataEntryLayout.addWidget(self.votesCountedField)

        self.metaDataEntryLayout.addWidget(self.metaSpacingLabel)

        # TODO Improve ToolTip; it's too slow and appearing below is not ideal
        self.marginOfVictoryVotesLabel = QLabel("[Expected] Margin of Victory in Votes*:")
        self.marginOfVictoryVotesLabel.setFont(standardMetaDataFont)
        self.marginOfVictoryVotesLabel.setToolTip("(First Place Votes - Second Place Votes)")
        self.metaDataEntryLayout.addWidget(self.marginOfVictoryVotesLabel)

        # TODO input validation
        self.marginOfVictoryVotesField = QLineEdit()
        self.marginOfVictoryVotesField.setPlaceholderText("e.g. 1000")
        self.marginOfVictoryVotesField.setFixedSize(self.standardLineEditWidth, self.standardLineEditHeight)
        self.metaDataEntryLayout.addWidget(self.marginOfVictoryVotesField)

        self.metaDataEntryLayout.addWidget(self.metaSpacingLabel)

        # Data Entry
        # TODO Validate data being entered (QItemDelegate? inputmask? for line edit)
        self.dataEntryLayout = QVBoxLayout()
        self.layout.addLayout(self.dataEntryLayout)
        
        self.dataTable = QTableWidget()
        self.dataEntryLayout.addWidget(self.dataTable)

        self.dataTable.setColumnCount(7)
        self.dataTable.setRowCount(20)

        self.dataTableHeaderLabels = ["Risk Name", "Type of Vote Manipulation\n(Adding, Subtracting, or Changing)", "Probability of Manipulation\nOver 1 Election Cycle", "Lower Bound of Impact\n(95% Chance Value Is Higher)", "Upper Bound of Impact\n(95% Chance Value Is Lower)", "Total Cost of Controls", "Control Effectiveness"]
        self.dataTable.setHorizontalHeaderLabels(self.dataTableHeaderLabels)

        for c in range(len(self.dataTableHeaderLabels)):
            self.dataTable.setColumnWidth(c, 200)

        # Buttons
        self.buttonsLayout = QHBoxLayout()
        self.layout.addLayout(self.buttonsLayout)

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

        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

        # TODO Control ranking

    def executeAnalyzeBtnClicked(self):
        print("Analyze button clicked")
        # TODO Read all data into LEC Generator
        DataHandling.analyzeData(DataHandling.loadData("sample"))

    def executeSaveBtnClicked(self):
        print("Save button clicked")
        # TODO Save all data to csv files

    def executeLoadBtnClicked(self):
        print("Load button clicked")
        # TODO Load all data from csv files

    def executeDeleteBtnClicked(self):
        print("Delete button clicked")
        print(self.electionIDDropdown.currentText())
        DataHandling.deleteData(self.electionIDDropdown.currentText())
        self.electionIDDropdown.removeItem(self.electionIDDropdown.currentIndex())


    def executeAddBtnClicked(self):
        print("Add button clicked")
        self.dataTable.insertRow(self.dataTable.rowCount())

    def executeReduceBtnClicked(self):
        print("Reduce button clicked")
        self.dataTable.removeRow(self.dataTable.rowCount()-1)







if __name__ == '__main__':
    # Create an instance of Qapplication
    app = QApplication([])

    # Create and display main window
    window = MainWindow()
    window.showMaximized()

    # Start the event loop.
    app.exec()
