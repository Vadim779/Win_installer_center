import sys
import json
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QWidget, QFileDialog, QComboBox, QHeaderView, QInputDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Table Data to JSON")
        self.setGeometry(100, 100, 800, 600)  # Increased window size

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.table = QTableWidget(0, 3, self)  # Start with an empty table
        self.layout.addWidget(self.table)

        self.table.setHorizontalHeaderLabels(["Name", "URL", "Setup"])

        self.add_row_button = QPushButton("Add Row", self)
        self.add_row_button.clicked.connect(self.add_row)
        self.layout.addWidget(self.add_row_button)

        self.open_button = QPushButton("Open", self)
        self.open_button.clicked.connect(self.open_config)
        self.layout.addWidget(self.open_button)

        self.save_button = QPushButton("Save", self)
        self.save_button.clicked.connect(self.save_data)
        self.layout.addWidget(self.save_button)

        self.load_from_url_button = QPushButton("Load from URL", self)
        self.load_from_url_button.clicked.connect(self.load_from_url)
        self.layout.addWidget(self.load_from_url_button)

        self.auto_load_config()

        self.create_table_layout()

    def create_table_layout(self):
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.table)
        self.layout.addLayout(h_layout)

    def add_row(self):
        row_count = self.table.rowCount()
        self.table.setRowCount(row_count + 1)

        setup_combobox = QComboBox()
        setup_combobox.addItems(["True", "False"])
        self.table.setCellWidget(row_count, 2, setup_combobox)

    def auto_load_config(self):
        default_config = "default_config.json"
        try:
            with open(default_config, "r") as file:
                config_data = json.load(file)
                self.load_config_into_table(config_data)
        except FileNotFoundError:
            print(f"File '{default_config}' not found.")

    def open_config(self):
        file_dialog = QFileDialog()
        filename, _ = file_dialog.getOpenFileName(self, "Open Configuration File", "", "JSON Files (*.json)")
        if filename:
            with open(filename, "r") as file:
                config_data = json.load(file)
                self.load_config_into_table(config_data)

    def load_config_into_table(self, config_data):
        self.table.setRowCount(0)  # Clear existing table
        for row_data in config_data:
            row_number = self.table.rowCount()
            self.table.insertRow(row_number)
            for col, (key, value) in enumerate(row_data.items()):
                item = QTableWidgetItem(str(value))
                self.table.setItem(row_number, col, item)

            setup_combobox = QComboBox()
            setup_combobox.addItems(["True", "False"])
            if 'Setup' in row_data and row_data['Setup'] in ('True', 'False'):
                index = setup_combobox.findText(row_data['Setup'])
                setup_combobox.setCurrentIndex(index)
            self.table.setCellWidget(row_number, 2, setup_combobox)

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def save_data(self):
        data = []
        for row in range(self.table.rowCount()):
            row_data = {}
            empty_row = False
            for col in range(self.table.columnCount()):
                if col == 2:
                    widget = self.table.cellWidget(row, col)
                    if widget is not None:
                        value = widget.currentText()
                        if value == 'True':
                            value = True
                        elif value == 'False':
                            value = False
                        row_data['Setup'] = value
                    else:
                        row_data['Setup'] = ""
                else:
                    item = self.table.item(row, col)
                    if item is not None and item.text().strip():
                        row_data[self.table.horizontalHeaderItem(col).text()] = item.text()
                    else:
                        empty_row = True
                        break
            if not empty_row:
                data.append(row_data)

        with open("output.json", "w") as file:
            json.dump(data, file, indent=4)
        print("Data saved to output.json")

    def load_from_url(self):
        url, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter URL:')
        if ok:
            try:
                response = requests.get(url)
                config_data = response.json()
                self.load_config_into_table(config_data)
            except requests.RequestException as e:
                print(f"Error fetching data from URL: {e}")
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON data: {e}")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
