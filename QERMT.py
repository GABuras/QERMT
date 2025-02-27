# Author: George Adler Buras

from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QLineEdit,
    QLabel,
    QTableWidget
)

# from PyQt6.QtGui import QFont

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

        self.addBtn = QPushButton("Add Row")
        self.addBtn.clicked.connect(self.executeAddBtnClicked)
        self.addBtn.setFixedSize(self.standardBtnWidth, self.standardBtnHeight)
        self.standardBtnFont = self.addBtn.font()
        self.standardBtnFont.setPointSize(15)
        self.addBtn.setFont(self.standardBtnFont)
        self.buttonsLayout.addWidget(self.addBtn)

        self.reduceBtn = QPushButton("Reduce Rows")
        self.reduceBtn.clicked.connect(self.executeReduceBtnClicked)
        self.reduceBtn.setFixedSize(self.standardBtnWidth, self.standardBtnHeight)
        self.reduceBtn.setFont(self.standardBtnFont)
        self.buttonsLayout.addWidget(self.reduceBtn)

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

        self.analyzeBtn = QPushButton("Analyze")
        self.analyzeBtn.clicked.connect(self.executeAnalyzeBtnClicked)
        self.analyzeBtn.setFixedSize(self.standardBtnWidth, self.standardBtnHeight)
        self.analyzeBtn.setFont(self.standardBtnFont)
        self.buttonsLayout.addWidget(self.analyzeBtn)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

    def executeAddBtnClicked(self):
        print("Add button clicked")
        self.dataTable.insertRow(self.dataTable.rowCount())

    def executeReduceBtnClicked(self):
        print("Reduce button clicked")
        self.dataTable.removeRow(self.dataTable.rowCount()-1)

    def executeSaveBtnClicked(self):
        print("Save button clicked")
        # TODO Save all data to csv files

    def executeLoadBtnClicked(self):
        print("Load button clicked")
        # TODO Load all data from csv files

    def executeAnalyzeBtnClicked(self):
        print("Analyze button clicked")
        # TODO Read all data into LEC Generator







if __name__ == '__main__':
    # Create an instance of Qapplication
    app = QApplication([])

    # Create and display main window
    window = MainWindow()
    window.show()

    # Start the event loop.
    app.exec()
