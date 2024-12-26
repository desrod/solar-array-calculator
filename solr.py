#!/usr/bin/env python3

import sys

from PyQt5.QtWidgets import (QApplication, QComboBox, QFormLayout, QHBoxLayout,
                             QLabel, QLineEdit, QMessageBox, QPushButton,
                             QVBoxLayout, QWidget)


class SolarBatteryCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()

        # Battery settings
        self.battery_layout = QVBoxLayout()
        self.setup_battery_section(self.battery_layout, self.calculate_battery_details)

        # Solar panel settings
        self.solar_layout = QVBoxLayout()
        self.setup_solar_section(self.solar_layout, self.calculate_solar_output)

        # About button
        about_btn = QPushButton("About", self)
        about_btn.clicked.connect(self.show_about_dialog)

        main_layout.addLayout(self.battery_layout)
        main_layout.addLayout(self.solar_layout)
        main_layout.addWidget(about_btn)

        self.setLayout(main_layout)
        self.setWindowTitle("Solar and Battery Capacity Calculator")

    def setup_battery_section(self, layout, calculation_func):
        # Capacity and Voltage
        capacity_layout = QHBoxLayout()
        capacity_layout.addWidget(QLabel("Enter Battery Capacity (Ah):"))
        entry_capacity = QLineEdit()
        capacity_layout.addWidget(entry_capacity)

        voltage_layout = QHBoxLayout()
        voltage_layout.addWidget(QLabel("Enter Battery Voltage (V):"))
        entry_voltage = QLineEdit()
        voltage_layout.addWidget(entry_voltage)

        # Count and Connection Type
        count_layout = QHBoxLayout()
        count_layout.addWidget(QLabel("Number of Batteries:"))
        entry_count = QLineEdit()
        entry_count.textChanged.connect(
            lambda: self.update_series_parallel(
                entry_count, entry_series, entry_parallel, connection_combobox
            )
        )
        count_layout.addWidget(entry_count)

        connection_combobox = QComboBox()
        connection_combobox.addItems(["Parallel", "Series", "Series + Parallel"])
        connection_combobox.currentIndexChanged.connect(
            lambda: self.update_series_parallel(
                entry_count, entry_series, entry_parallel, connection_combobox
            )
        )

        # Series and Parallel Entry
        series_parallel_layout = QFormLayout()
        entry_series = QLineEdit()
        entry_parallel = QLineEdit()
        series_parallel_layout.addRow("In Series:", entry_series)
        series_parallel_layout.addRow("In Parallel:", entry_parallel)
        entry_series.setVisible(False)
        entry_parallel.setVisible(False)

        # Result Labels
        result_capacity_label = QLabel("Total Battery Capacity:")
        result_voltage_label = QLabel("Total Battery Voltage:")
        result_amps_label = QLabel("Total Battery Amps:")
        result_watts_label = QLabel("Total Battery Energy:")
        calc_btn = QPushButton("Calculate Battery Details", self)
        calc_btn.clicked.connect(
            lambda: calculation_func(
                entry_capacity,
                entry_voltage,
                entry_count,
                connection_combobox,
                entry_series,
                entry_parallel,
                result_capacity_label,
                result_voltage_label,
                result_amps_label,
                result_watts_label,
            )
        )

        layout.addLayout(capacity_layout)
        layout.addLayout(voltage_layout)
        layout.addLayout(count_layout)
        layout.addWidget(connection_combobox)
        layout.addLayout(series_parallel_layout)
        layout.addWidget(result_capacity_label)
        layout.addWidget(result_voltage_label)
        layout.addWidget(result_amps_label)
        layout.addWidget(result_watts_label)
        layout.addWidget(calc_btn)

    def setup_solar_section(self, layout, calculation_func):
        # Panel Vmp and Imp
        panel_vmp_layout = QHBoxLayout()
        panel_vmp_layout.addWidget(QLabel("Enter Max Power Voltage (Vmp):"))
        self.entry_panel_vmp = QLineEdit()
        panel_vmp_layout.addWidget(self.entry_panel_vmp)

        panel_imp_layout = QHBoxLayout()
        panel_imp_layout.addWidget(QLabel("Enter Max Power Current (Imp):"))
        self.entry_panel_imp = QLineEdit()
        panel_imp_layout.addWidget(self.entry_panel_imp)

        # Count and Connection Type
        count_layout = QHBoxLayout()
        count_layout.addWidget(QLabel("Number of Panels:"))
        self.entry_panel_count = QLineEdit()
        self.entry_panel_count.textChanged.connect(
            lambda: self.update_series_parallel(
                self.entry_panel_count,
                self.entry_panel_series,
                self.entry_panel_parallel,
                self.panel_connection_combobox,
            )
        )
        count_layout.addWidget(self.entry_panel_count)

        connection_layout = QHBoxLayout()
        connection_layout.addWidget(QLabel("Connection Type:"))
        self.panel_connection_combobox = QComboBox()
        self.panel_connection_combobox.addItems(
            ["Select", "Series", "Parallel", "Series + Parallel"]
        )
        self.panel_connection_combobox.currentIndexChanged.connect(
            lambda: self.update_series_parallel(
                self.entry_panel_count,
                self.entry_panel_series,
                self.entry_panel_parallel,
                self.panel_connection_combobox,
            )
        )
        connection_layout.addWidget(self.panel_connection_combobox)

        # Series and Parallel Counts
        series_parallel_layout = QHBoxLayout()
        series_parallel_layout.addWidget(QLabel("Series Count:"))
        self.entry_panel_series = QLineEdit()
        series_parallel_layout.addWidget(self.entry_panel_series)
        self.entry_panel_series.setVisible(False)

        series_parallel_layout.addWidget(QLabel("Parallel Count:"))
        self.entry_panel_parallel = QLineEdit()
        series_parallel_layout.addWidget(self.entry_panel_parallel)
        self.entry_panel_parallel.setVisible(False)

        # Results
        self.result_capacity_label = QLabel("")
        self.result_voltage_label = QLabel("")
        self.result_amps_label = QLabel("")

        # Calculate Button
        calculate_btn = QPushButton("Calculate Solar", self)
        calculate_btn.clicked.connect(
            lambda: calculation_func(
                self.entry_panel_vmp,
                self.entry_panel_imp,
                self.entry_panel_count,
                self.panel_connection_combobox,
                self.entry_panel_series,
                self.entry_panel_parallel,
                self.result_capacity_label,
                self.result_voltage_label,
                self.result_amps_label,
            )
        )

        # Add widgets to layout
        layout.addLayout(panel_vmp_layout)
        layout.addLayout(panel_imp_layout)
        layout.addLayout(count_layout)
        layout.addLayout(connection_layout)
        layout.addLayout(series_parallel_layout)
        layout.addWidget(calculate_btn)
        layout.addWidget(self.result_capacity_label)
        layout.addWidget(self.result_voltage_label)
        layout.addWidget(self.result_amps_label)

    def calculate_battery_details(
        self,
        entry_capacity,
        entry_voltage,
        entry_count,
        connection_combobox,
        entry_series,
        entry_parallel,
        result_capacity_label,
        result_voltage_label,
        result_amps_label,
        result_watts_label,
    ):
        try:
            capacity = float(entry_capacity.text())
            voltage = float(entry_voltage.text())
            count = int(entry_count.text())
            series_count = (
                int(entry_series.text()) if entry_series.isVisible() else count
            )
            parallel_count = (
                int(entry_parallel.text()) if entry_parallel.isVisible() else count
            )

            if connection_combobox.currentText() == "Parallel":
                total_capacity = capacity * count
                total_voltage = voltage
                total_amps = total_capacity / total_voltage
            elif connection_combobox.currentText() == "Series":
                total_capacity = capacity
                total_voltage = voltage * count
                total_amps = total_capacity / total_voltage
            elif connection_combobox.currentText() == "Series + Parallel":
                total_capacity = capacity * parallel_count
                total_voltage = voltage * series_count
                total_amps = total_capacity / total_voltage
            else:
                raise ValueError("Invalid connection type.")

            total_watt_hours = total_capacity * total_voltage

            result_capacity_label.setText(
                f"Total Battery Capacity: {total_capacity} Ah"
            )
            result_voltage_label.setText(f"Total Battery Voltage: {total_voltage} V")
            result_amps_label.setText(f"Total Battery Amps: {total_amps:.2f} A")
            result_watts_label.setText(
                f"Total Battery Energy: {total_watt_hours:.2f} Wh"
            )

        except ValueError as e:
            result_capacity_label.setText("Error: " + str(e))
            result_voltage_label.setText("")
            result_amps_label.setText("")
            result_watts_label.setText("")

    def calculate_solar_output(
        self,
        entry_vmp,
        entry_imp,
        entry_count,
        connection_combobox,
        entry_series,
        entry_parallel,
        result_capacity_label,
        result_voltage_label,
        result_amps_label,
        result_watts_label,
    ):
        try:
            vmp = float(entry_vmp.text())
            imp = float(entry_imp.text())
            count = int(entry_count.text())
            series_count = (
                int(entry_series.text()) if entry_series.isVisible() else count
            )
            parallel_count = (
                int(entry_parallel.text()) if entry_parallel.isVisible() else count
            )

            if connection_combobox.currentText() == "Parallel":
                total_vmp = vmp  # Voltage remains the same
                total_imp = imp * count  # Currents summed
                total_capacity = total_vmp * total_imp  # Power calculation
            elif connection_combobox.currentText() == "Series":
                total_vmp = vmp * count  # Voltages summed
                total_imp = imp  # Current remains the same
                total_capacity = total_vmp * total_imp  # Power calculation
            elif connection_combobox.currentText() == "Series + Parallel":
                total_vmp = vmp * series_count  # Sum of voltages in series
                total_imp = imp * parallel_count  # Sum of currents in parallel
                total_capacity = total_vmp * total_imp  # Power calculation
            else:
                raise ValueError("Invalid connection type.")

            result_capacity_label.setText(
                f"Total Solar Panel Capacity: {total_capacity:.2f} Watts"
            )
            result_voltage_label.setText(
                f"Total Solar Panel Voltage (Vmp): {total_vmp:.2f} V"
            )
            result_amps_label.setText(
                f"Total Solar Panel Current (Imp): {total_imp:.2f} A"
            )
        except ValueError as e:
            result_capacity_label.setText("Error: " + str(e))
            result_voltage_label.setText("")
            result_amps_label.setText("")

    def update_series_parallel(self, count_entry, series_entry, parallel_entry, combo):
        count = int(count_entry.text()) if count_entry.text().isdigit() else 0
        if combo.currentText() == "Parallel":
            series_entry.setVisible(False)
            parallel_entry.setVisible(True)
            series_entry.setText("")
            parallel_entry.setText(str(count))
        elif combo.currentText() == "Series":
            series_entry.setVisible(True)
            parallel_entry.setVisible(False)
            series_entry.setText(str(count))
            parallel_entry.setText("")
        elif combo.currentText() == "Series + Parallel":
            series_entry.setVisible(True)
            parallel_entry.setVisible(True)
            series_entry.setText("")
            parallel_entry.setText("")
        else:
            series_entry.setVisible(False)
            parallel_entry.setVisible(False)
            series_entry.setText("")
            parallel_entry.setText("")

    def show_about_dialog(self):
        about_text = (
            "Solar and Battery Capacity Calculator\n"
            "Version 1.0\n"
            "© 2024 David A. Desrosiers\n"
            "All rights reserved."
        )
        QMessageBox.about(self, "About", about_text)


def main():
    app = QApplication(sys.argv)
    ex = SolarBatteryCalculator()
    ex.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
