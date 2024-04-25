import sqlite3
import PySimpleGUI as sg

class FlowerShopUI:
    def __init__(self):
        self.conn = sqlite3.connect("project-stage2.db")
        self.cur = self.conn.cursor()
        self.logged_in_user = None

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

    def admin_main_menu(self):
        layout = [
            [sg.Text('Admin Menu')],
            [sg.Button('Add Flower Arrangement')],
            [sg.Button('Delete Flower Arrangement')],
            [sg.Button('View Flower Arrangements')],
            [sg.Button('Logout')]
        ]
        window = sg.Window('Admin Menu', layout)
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Logout':
                break
            elif event == 'View Flower Arrangements':
                self.view_flower_arrangements_window()
            elif event == 'Add Flower Arrangement':
                self.add_flower_arrangement_window().read(close=True)
            elif event == 'Delete Flower Arrangement':
                self.delete_flower_arrangement_window().read(close=True)
        window.close()
        
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
        window = sg.Window('Add Flower Arrangement', layout)
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Cancel':
                break
            elif event == 'Add':
                # Girilen bilgileri al
                arrangement_id = values['-ID-']
                size = values['-SIZE-']
                type_ = values['-TYPE-']
                quantity = values['-QUANTITY-']
                price = values['-PRICE-']
                name = values['-NAME-']
                design = values['-DESIGN-']
                
                # Veritabanına ekleme işlemi
                self.cur.execute("INSERT INTO Flower_arrangement (FID, Fsize, Ftype, quantity, price, Fname, floral_description) VALUES (?, ?, ?, ?, ?, ?, ?)",
                                 (arrangement_id, size, type_, quantity, price, name, design))
                self.conn.commit()
                sg.popup('Flower Arrangement added successfully!')
                break
        window.close()
        return window

    def delete_flower_arrangement_window(self):
        layout = [
            [sg.Text('Delete Flower Arrangement')],
            [sg.Text('Enter ID to delete:'), sg.InputText(key='-DELETE_ID-')],
            [sg.Button('Delete'), sg.Button('Cancel')]
        ]
        window = sg.Window('Delete Flower Arrangement', layout)
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Cancel':
                break
            elif event == 'Delete':
                # Girilen ID'ye sahip çiçek düzenlemesini veritabanından sil
                arrangement_id = values['-DELETE_ID-']
                self.cur.execute("DELETE FROM Flower_arrangement WHERE FID = ?", (arrangement_id,))
                self.conn.commit()
                sg.popup('Flower Arrangement deleted successfully!')
                break
        window.close()
        return window


    def view_flower_arrangements_window(self):
        self.cur.execute("SELECT * FROM Flower_arrangement")
        data = self.cur.fetchall()
        layout = [
            [sg.Text('Floral Arrangements')],
            [sg.Table(values=data, headings=['FID', 'Fname', 'price', 'quantity', 'Ftype', 'Fsize', 'floral_description'],
                      display_row_numbers=False, auto_size_columns=True, justification='left', key='-TABLE-')],
            [sg.Button('Close')]
        ]
        window = sg.Window('View Flower Arrangements', layout)
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Close':
                break
        window.close()

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

    def customer_main_menu(self):
        layout = [
            [sg.Text('Customer Menu')],
            [sg.Button('View Flower Arrangements')],
            [sg.Button('Add to Cart')],
            [sg.Button('View Cart')],
            [sg.Button('Logout')]
        ]
        window = sg.Window('Customer Menu', layout)
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Logout':
                break
            elif event == 'View Flower Arrangements':
                self.view_flower_arrangements_window()
        window.close()
        
    def deliverer_login_window(self):
        layout = [
            [sg.Text('Deliverer Login')],
            [sg.Text('Username:'), sg.InputText(key='-USERNAME-')],
            [sg.Text('Password:'), sg.InputText(key='-PASSWORD-', password_char='*')],
            [sg.Button('Login'), sg.Button('Cancel')]
        ]
        return sg.Window('Deliverer Login', layout)

    def deliverer_main_menu(self):
        layout = [
            [sg.Text('Deliverer Menu')],
            [sg.Button('View Orders')],
            [sg.Button('Logout')]
        ]
        window = sg.Window('Deliverer Menu', layout)
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Logout':
                break
            elif event == 'View Orders':
                self.view_orders_window()  # view_orders_window() fonksiyonunu çağırıyoruz
        window.close()

        
        
    def run(self):
        while True:
            window = self.welcome_window()
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Exit':
                break
            elif event == 'Admin Login':
                window.close()
                self.logged_in_user = 'admin'
                self.admin_login()
            elif event == 'Customer Login':
                window.close()
                self.logged_in_user = 'customer'
                self.customer_login()
            elif event == 'Deliverer Login':
                window.close()
                self.logged_in_user = 'deliverer'
                self.deliverer_login()
        window.close()
        self.conn.close()  # Close the database connection when the application exits

    def admin_login(self):
        while True:
            window = self.admin_login_window()
            event, values = window.read()
            window.close()
            if event == sg.WIN_CLOSED or event == 'Cancel':
                break
            elif event == 'Login':
                username = values['-USERNAME-']
                password = values['-PASSWORD-']
                if self.admin_authentication(username, password):
                    self.admin_main_menu()  # admin_main_menu() fonksiyonunu doğrudan çağırıyorum
                    break
                else:
                    sg.popup('Invalid username or password.')
            elif event == 'Logout':
                self.logged_in_user = None
                break

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

    def customer_login(self):
        while True:
            window = self.customer_login_window()
            event, values = window.read()
            window.close()
            if event == sg.WIN_CLOSED or event == 'Cancel':
                break
            elif event == 'Login':
                username = values['-USERNAME-']
                password = values['-PASSWORD-']
                if self.customer_authentication(username, password):
                    self.customer_main_menu().read(close=True)
                    break
                else:
                    sg.popup('Invalid username or password.')
            elif event == 'Logout':
                self.logged_in_user = None
                break

    def customer_authentication(self, username, password):
        if username == 'customer' and password == 'customer123':
            return True
        else:
            return False

    def deliverer_login(self):
        while True:
            window = self.deliverer_login_window()
            event, values = window.read()
            window.close()
            if event == sg.WIN_CLOSED or event == 'Cancel':
                break
            elif event == 'Login':
                username = values['-USERNAME-']
                password = values['-PASSWORD-']
                if self.deliverer_authentication(username, password):
                    self.deliverer_main_menu()  # deliverer_main_menu() fonksiyonunu doğrudan çağırıyorum
                    break
                else:
                    sg.popup('Invalid username or password.')
            elif event == 'Logout':
                self.logged_in_user = None
                break

    def deliverer_authentication(self, username, password):
        if username == 'deliverer' and password == 'deliverer123':
            return True
        else:
            return False
    
    def view_orders_window(self):
        # Siparişleri veritabanından alın ve uygun şekilde göster
        self.cur.execute("SELECT * FROM Orders")
        orders_data = self.cur.fetchall()
    
        # Siparişleri göstermek için bir pencere oluştur
        layout = [
            [sg.Text('Orders')],
            [sg.Table(values=orders_data, headings=['Order ID', 'Customer ID', 'Date', 'Status'],
                      display_row_numbers=False, auto_size_columns=True, justification='left')],
            [sg.Button('Close')]
        ]
        window = sg.Window('View Orders', layout)
    
        # Pencereyi görüntüle ve kullanıcının "Close" düğmesine tıklamasını bekleyin
        event, values = window.read()
        window.close()


app = FlowerShopUI()
app.run()
