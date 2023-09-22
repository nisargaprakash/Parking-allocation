import mysql.connector
import datetime
import sys
import re
import time

from PyQt5 import QtCore, QtWidgets, uic

mydb = mysql.connector.connect(host="localhost", user="smoke", passwd="hellomoto", database="car", autocommit=True)
mycursor = mydb.cursor()

mycursor.execute("DROP TABLE IF EXISTS slot")
mycursor.execute("DROP TABLE IF EXISTS duration")
mycursor.execute("DROP TABLE IF EXISTS entry")
mycursor.execute("DROP TABLE IF EXISTS exits")
mycursor.execute("DROP TABLE IF EXISTS cost")

mycursor.execute("CREATE TABLE IF NOT EXISTS slot(carNumber VARCHAR(15), slot int)")
mycursor.execute("CREATE TABLE IF NOT EXISTS entry(carNumber VARCHAR(15), entry VARCHAR(40))")
mycursor.execute("CREATE TABLE IF NOT EXISTS exits(carNumber VARCHAR(15), exit1 VARCHAR(40))")
mycursor.execute("CREATE TABLE IF NOT EXISTS duration(carNumber VARCHAR(15), durationInSec int)")
mycursor.execute("CREATE TABLE IF NOT EXISTS cost(carNumber VARCHAR(15), cost int)")

slots = [False for _ in range(16)]


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi("front.ui", self)
        self.ENTRYBUTTON.released.connect(self.entry)
        self.EXITBUTTON.released.connect(self.exit)

    def entry(self):
        try:
            carNumber = self.lineEdit.text()
            if all(slots):
                self.label_2.setText("Parking Full")
            else:
                slotNO = slots.index(False)
                slots[slotNO] = True
                slotNO += 1
                entry_time = datetime.datetime.now()
                mycursor.execute("INSERT INTO slot (carNumber, slot) VALUES (%s, %s)", (carNumber, slotNO))
                mycursor.execute("INSERT INTO entry (carNumber, entry) VALUES (%s, %s)", (carNumber, entry_time))
                self.label_2.setText(f"Slot: {slotNO}")
                self.update_slot_colors()
        except Exception as e:
            print(e)
            self.label_2.setText("Invalid")

    def exit(self):
        try:
            carNumber = self.lineEdit.text()
            self.lineEdit.clear()

            exit_time = datetime.datetime.now()
            mycursor.execute("SELECT slot FROM slot WHERE carNumber = %s", (carNumber,))
            row = mycursor.fetchone()

            if row:
                slotNO = row[0]
                slots[slotNO - 1] = False

                mycursor.execute("SELECT entry FROM entry WHERE carNumber = %s", (carNumber,))
                entry_time = mycursor.fetchone()[0]
                entry_time = datetime.datetime.fromisoformat(entry_time)

                duration = int((exit_time - entry_time).total_seconds())

                cost = duration * 1  # Change the cost calculation here
                if cost > 150:
                    cost = 150

                mycursor.execute("UPDATE exits SET exit1 = %s WHERE carNumber = %s", (exit_time, carNumber))
                mycursor.execute("UPDATE duration SET durationInSec = %s WHERE carNumber = %s", (duration, carNumber))
                mycursor.execute("UPDATE cost SET cost = %s WHERE carNumber = %s", (cost, carNumber))

                self.label_2.setText(f"Cost: Rs. {cost}")
                self.update_slot_colors()
            else:
                self.label_2.setText("Invalid Entry")

        except Exception as e:
            print(e)
            self.label_2.setText("Invalid Entry")

    def update_slot_colors(self):
        for i in range(16):
            if slots[i]:
                getattr(self, f"s{i + 1}").setStyleSheet("background-color: #FF0B00")
            else:
                getattr(self, f"s{i + 1}").setStyleSheet("background-color: #40FF50")


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
