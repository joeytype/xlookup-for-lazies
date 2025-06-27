import sys
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QComboBox,
    QLineEdit, QFileDialog, QMessageBox, QGridLayout
)
from PyQt5.QtCore import Qt

class XLookupApp(QWidget):
    def __init__(self):
        super().__init__()
        self.df_a = None
        self.df_b = None
        self.file_a = None
        self.file_b = None

        self.setWindowTitle("CSV XLOOKUP Tool")
        self.setFixedSize(600, 350)

        self.init_ui()

    def init_ui(self):
        layout = QGridLayout()
        layout.setSpacing(10)
        self.setLayout(layout)

        # File A
        layout.addWidget(QLabel("File you wish to add a column to:"), 0, 0)
        self.file_a_label = QLabel("No file selected")
        self.file_a_label.setStyleSheet("background-color: white; border: 1px solid gray; padding: 4px;")
        layout.addWidget(self.file_a_label, 0, 1)
        file_a_btn = QPushButton("Browse")
        file_a_btn.clicked.connect(self.load_file_a)
        layout.addWidget(file_a_btn, 0, 2)

        # New column name
        layout.addWidget(QLabel("Name of column to add:"), 1, 0)
        self.new_col_name = QLineEdit()
        layout.addWidget(self.new_col_name, 1, 1, 1, 2)

        # Lookup column in A
        layout.addWidget(QLabel("Column to use for lookup:"), 2, 0)
        self.lookup_col_a = QComboBox()
        layout.addWidget(self.lookup_col_a, 2, 1, 1, 2)

        # File B
        layout.addWidget(QLabel("File you will pull values from:"), 3, 0)
        self.file_b_label = QLabel("No file selected")
        self.file_b_label.setStyleSheet("background-color: white; border: 1px solid gray; padding: 4px;")
        layout.addWidget(self.file_b_label, 3, 1)
        file_b_btn = QPushButton("Browse")
        file_b_btn.clicked.connect(self.load_file_b)
        layout.addWidget(file_b_btn, 3, 2)

        # Lookup column in B
        layout.addWidget(QLabel("Column to look up values in:"), 4, 0)
        self.lookup_col_b = QComboBox()
        layout.addWidget(self.lookup_col_b, 4, 1, 1, 2)

        # Value column in B
        layout.addWidget(QLabel("Column to add values from:"), 5, 0)
        self.value_col_b = QComboBox()
        layout.addWidget(self.value_col_b, 5, 1, 1, 2)

        # Run button
        run_btn = QPushButton("Run XLOOKUP")
        run_btn.clicked.connect(self.run_xlookup)
        layout.addWidget(run_btn, 6, 1, 1, 2, alignment=Qt.AlignCenter)

        # Set white background and black text
        self.setStyleSheet("background-color: white; color: black;")

    def load_file_a(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open File A", "", "CSV files (*.csv)")
        if path:
            try:
                self.df_a = pd.read_csv(path)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to read file:\n{e}")
                self.df_a = None
                return
            self.file_a = path
            self.file_a_label.setText(path.split('/')[-1])
            self.lookup_col_a.clear()
            self.lookup_col_a.addItems(self.df_a.columns)

    def load_file_b(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open File B", "", "CSV files (*.csv)")
        if path:
            try:
                self.df_b = pd.read_csv(path)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to read file:\n{e}")
                self.df_b = None
                return
            self.file_b = path
            self.file_b_label.setText(path.split('/')[-1])
            self.lookup_col_b.clear()
            self.value_col_b.clear()
            self.lookup_col_b.addItems(self.df_b.columns)
            self.value_col_b.addItems(self.df_b.columns)

    def run_xlookup(self):
        if self.df_a is None or self.df_b is None:
            QMessageBox.warning(self, "Error", "Please load both files.")
            return

        new_col = self.new_col_name.text().strip()
        if not new_col:
            QMessageBox.warning(self, "Error", "Please specify a name for the new column.")
            return

        lookup_a = self.lookup_col_a.currentText()
        lookup_b = self.lookup_col_b.currentText()
        value_b = self.value_col_b.currentText()

        if not lookup_a or not lookup_b or not value_b:
            QMessageBox.warning(self, "Error", "Please select all required columns.")
            return

        try:
            map_series = self.df_b.drop_duplicates(subset=[lookup_b]).set_index(lookup_b)[value_b]
            self.df_a[new_col] = self.df_a[lookup_a].map(map_series)
        except KeyError as e:
            QMessageBox.critical(self, "Error", f"Column not found:\n{e}")
            return
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred:\n{e}")
            return

        save_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "CSV files (*.csv)")
        if save_path:
            try:
                self.df_a.to_csv(save_path, index=False)
                QMessageBox.information(self, "Done", f"File saved to {save_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save file:\n{e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = XLookupApp()
    window.show()
    sys.exit(app.exec())
