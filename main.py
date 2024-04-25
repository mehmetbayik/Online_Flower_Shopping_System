import sqlite3
import PySimpleGUI as sg

class FlowerShopUI:
    def __init__(self):
        self.conn = sqlite3.connect("project-stage2.db")
        self.cur = self.conn.cursor()

    def welcome_window(self):
        layout = [
            [sg.Text('Welcome to the Online Flower Shopping System.')],
            [sg.Button('Admin Login')],
            [sg.Button('Customer Login')],
            [sg.Button('Deliverer Login')],
            [sg.Button('Exit')]
        ]
        return sg.Window('Login Window', layout)

    def admin_login_window(self):
        layout = [
            [sg.Text('Admin Login')],
            [sg.Text('Username:'), sg.InputText(key='-USERNAME-')],
            [sg.Text('Password:'), sg.InputText(key='-PASSWORD-', password_char='*')],
            [sg.Button('Login'), sg.Button('Cancel')]
        ]
        return sg.Window('Admin Login', layout)

    def admin_main_window(self):
        layout = [
            [sg.Text('Admin Menu')],
            [sg.Button('Add Flower Arrangement')],
            [sg.Button('Delete Flower Arrangement')],
            [sg.Button('View Flower Arrangements')],
            [sg.Button('Logout')]
        ]
        return sg.Window('Admin Menu', layout)

    def add_flower_arrangement_window(self):
        layout = [
            [sg.Text('Add Flower Arrangement')],
            [sg.Text('ID:'), sg.InputText(key='-ID-')],
            [sg.Text('Size:'), sg.InputText(key='-SIZE-')],
            [sg.Text('Type:'), sg.InputText(key='-TYPE-')],
            [sg.Text('Quantity:'), sg.InputText(key='-QUANTITY-')],
            [sg.Text('Price:'), sg.InputText(key='-PRICE-')],
            [sg.Text('Name:'), sg.InputText(key='-NAME-')],
            [sg.Text('Design:'), sg.InputText(key='-DESIGN-')],
            [sg.Button('Add'), sg.Button('Cancel')]
        ]
        return sg.Window('Add Flower Arrangement', layout)

    def delete_flower_arrangement_window(self):
        layout = [
            [sg.Text('Delete Flower Arrangement')],
            [sg.Text('Enter ID to delete:'), sg.InputText(key='-DELETE_ID-')],
            [sg.Button('Delete'), sg.Button('Cancel')]
        ]
        return sg.Window('Delete Flower Arrangement', layout)

    def view_flower_arrangements_window(self):
        self.cur.execute("SELECT * FROM Flower_arrangement")
        data = self.cur.fetchall()
        layout = [
            [sg.Table(values=data, headings=['FID', 'Fname', 'price', 'quantity', 'Ftype', 'Fsize', 'floral_description'],
                      display_row_numbers=False, auto_size_columns=True, justification='left')],
            [sg.Button('Select'), sg.Button('Cancel')]
        ]
        return sg.Window('View Flower Arrangements', layout)

    def edit_flower_arrangement_window(self, arrangement_id):
        layout = [
            [sg.Text('Edit Flower Arrangement')],
            [sg.Text('ID:'), sg.InputText(key='-ID-', default_text=arrangement_id, disabled=True)],
            # Include input fields for other attributes
            [sg.Button('Save'), sg.Button('Cancel')]
        ]
        return sg.Window('Edit Flower Arrangement', layout)

    def customer_login_window(self):
        layout = [
            [sg.Text('Customer Login')],
            [sg.Text('Username:'), sg.InputText(key='-USERNAME-')],
            [sg.Text('Password:'), sg.InputText(key='-PASSWORD-', password_char='*')],
            [sg.Button('Login'), sg.Button('Cancel')]
        ]
        return sg.Window('Customer Login', layout)

    def customer_main_window(self):
        layout = [
            [sg.Text('Customer Menu')],
            [sg.Button('View Flower Arrangements')],
            [sg.Button('Add to Cart')],
            [sg.Button('View Cart')],
            [sg.Button('Logout')]
        ]
        return sg.Window('Customer Menu', layout)

    def deliverer_login_window(self):
        layout = [
            [sg.Text('Deliverer Login')],
            [sg.Text('Username:'), sg.InputText(key='-USERNAME-')],
            [sg.Text('Password:'), sg.InputText(key='-PASSWORD-', password_char='*')],
            [sg.Button('Login'), sg.Button('Cancel')]
        ]
        return sg.Window('Deliverer Login', layout)

    def deliverer_main_window(self):
        layout = [
            [sg.Text('Deliverer Menu')],
            [sg.Button('View Orders')],
            [sg.Button('Logout')]
        ]
        return sg.Window('Deliverer Menu', layout)

    def run(self):
        while True:
            window = self.welcome_window()
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Exit':
                break
            elif event == 'Admin Login':
                window.close()
                self.admin_login()
            elif event == 'Customer Login':
                window.close()
                self.customer_login()
            elif event == 'Deliverer Login':
                window.close()
                self.deliverer_login()
            window.close()

    def admin_login(self):
        while True:
            window = self.admin_login_window()
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Cancel':
                break
            elif event == 'Login':
                username = values['-USERNAME-']
                password = values['-PASSWORD-']
                if self.admin_authentication(username, password):
                    window.close()
                    self.admin_main_menu()
                else:
                    sg.popup('Invalid username or password.')
            window.close()

    def admin_authentication(self, username, password):
        if username == 'hande' and password == 'hande123':
            return True
        elif username == 'baran' and password == 'baran123':
            return True
        elif username == 'mehmet' and password == 'mehmet123':
            return True
        elif username == 'zeynep' and password == 'zeynep123':
            return True
        elif username == 'inci' and password == 'inci123':
            return True
        elif username == 'onur' and password == 'onur123':
            return True
        else:
            return False

    def admin_main_menu(self):
        while True:
            window = self.admin_main_window()
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Logout':
                break
            elif event == 'Add Flower Arrangement':
                window.close()
                self.add_flower_arrangement()
            elif event == 'Delete Flower Arrangement':
                window.close()
                self.delete_flower_arrangement()
            elif event == 'View Flower Arrangements':
                window.close()
                self.view_flower_arrangements()
            window.close()

    def add_flower_arrangement(self):
        while True:
            window = self.add_flower_arrangement_window()
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Cancel':
                break
            elif event == 'Add':
                # Implement adding flower arrangement functionality
                pass
            window.close()

    def delete_flower_arrangement(self):
        while True:
            window = self.delete_flower_arrangement_window()
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Cancel':
                break
            elif event == 'Delete':
                # Implement deleting flower arrangement functionality
                pass
            window.close()

    def view_flower_arrangements(self):
        while True:
            window = self.view_flower_arrangements_window()
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Cancel':
                break
            elif event == 'Select':
                selected_row = values[event]
                if selected_row:  # Check if a row is actually selected
                    arrangement_id = selected_row[0]
                    self.view_arrangement_details(arrangement_id)
            window.close()

    def view_arrangement_details(self, arrangement_id):
        query = "SELECT * FROM Flower_arrangement WHERE FID = ?"
        self.cur.execute(query, (arrangement_id,))
        arrangement_details = self.cur.fetchone()

        if arrangement_details:
            layout = [
                [sg.Text('Arrangement Details')],
                [sg.Text(f'ID: {arrangement_details[0]}')],
                [sg.Text(f'Name: {arrangement_details[1]}')],
                [sg.Text(f'Price: {arrangement_details[2]}')],
                [sg.Text(f'Quantity: {arrangement_details[3]}')],
                [sg.Text(f'Type: {arrangement_details[4]}')],
                [sg.Text(f'Size: {arrangement_details[5]}')],
                [sg.Text(f'Description: {arrangement_details[6]}')],
                [sg.Button('Add to Cart'), sg.Button('Close')]
            ]

            window = sg.Window('Arrangement Details', layout)
            while True:
                event, values = window.read()
                if event == sg.WIN_CLOSED or event == 'Close':
                    break
                elif event == 'Add to Cart':
                    self.add_to_cart(arrangement_id)
            window.close()
        else:
            sg.popup('Arrangement not found.')

    def add_to_cart(self, arrangement_id):
        # Implement adding arrangement to cart functionality
        pass

    def view_cart(self):
        # Implement viewing cart functionality
        pass

    # Define other necessary methods for admin operations
    # Define methods for customer operations

app = FlowerShopUI()
app.run()
