import sqlite3
import PySimpleGUI as sg

# con = sqlite3.connect('database.db')
# print(con)
# cur = con.cursor()

class ciceksepeti_ui:
    def __init__(self):
        pass
    def welcome_window(self):
        
        self.layout = [[sg.Text('Welcome to the Online Flower Shopping System.')],
                       [sg.Button('New Customer')],
                       [sg.Button('New Deliverers')],
                       [sg.Button('Login Screen')],
                       [sg.Button('Exit')]]
        return sg.Window('Login Window', self.layout)
    
    
app = ciceksepeti_ui()
while True:
    window = app.welcome_window()
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if event == 'New Customer':
        print('New Customer')
    if event == 'New Deliverers':
        print('New Deliverers')
    if event == 'Login Screen':
        print('Login Screen')
    if event == 'Exit':
        print('Exit')
        break
    window.close()
    
    