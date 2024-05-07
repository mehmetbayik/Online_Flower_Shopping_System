import sqlite3
from datetime import datetime
import PySimpleGUI as sg



class FlowerShopUI:
    def __init__(self):
        self.conn = sqlite3.connect("project-stage2.db")
        self.cur = self.conn.cursor()
        self.logged_in_user = None
        self.user_id = None
        self.cart = []
        self.discounts = []
        self.prepared_arrangements = []
        self.selected_discount = None


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
                [sg.Button('Define Discounts')],
                [sg.Button('View Discounts')],
                [sg.Button('View Orders')],
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
                    self.add_flower_arrangement_window()
                elif event == 'Delete Flower Arrangement':
                    self.delete_flower_arrangement_window()
                elif event == 'Define Discounts':
                    self.define_discounts_window()
                elif event == 'View Discounts':
                    self.view_discounts_window()
                elif event == 'View Orders':
                    self.view_orders_window()
            window.close()



    def add_flower_arrangement_window(self):
        # En son kullanılan ID'yi bul ve yeni ID'yi hesapla
        self.cur.execute("SELECT FID FROM Flower_arrangement ORDER BY FID DESC LIMIT 1")
        last_id = self.cur.fetchone()
        if last_id:
            next_id_number = int(last_id[0][3:]) + 1
            new_id = f'FID{next_id_number:03d}'
        else:
            new_id = 'FID001'
    
        layout = [
            [sg.Text('Add Flower Arrangement')],
            [sg.Text('ID:'), sg.Text(new_id)],
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
                try:
                    qt_int_err = int(values['-QUANTITY-'])
                    price_int_err = int(values['-PRICE-'])
                    size = values['-SIZE-']
                    type_ = values['-TYPE-']
                    quantity = values['-QUANTITY-']
                    price = values['-PRICE-']
                    name = values['-NAME-']
                    design = values['-DESIGN-']
        
                    self.cur.execute("INSERT INTO Flower_arrangement (FID, Fsize, Ftype, quantity, price, Fname, floral_description) VALUES (?, ?, ?, ?, ?, ?, ?)",
                                    (new_id, size, type_, quantity, price, name, design))
                    self.conn.commit()
                    sg.popup('Flower Arrangement added successfully!')
                    break
                except:
                    sg.popup('Invalid value/s! (Quantity and price should be integer)')
                    break
        window.close()



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
        self.cur.execute("SELECT FID, Fname FROM Flower_arrangement")
        data = self.cur.fetchall()

    
        if self.logged_in_user == "customer":
            layout = [
                [sg.Text('Floral Arrangements')],
                [sg.Listbox(values=data, size=(30, 6), key='-ARRANGEMENTS-', select_mode='multiple')],
                [sg.Button('View Details'), sg.Button('Add to Cart'), sg.Button('Close')]
            ]
        elif self.logged_in_user == "admin":
            layout = [
                [sg.Text('Floral Arrangements')],
                [sg.Listbox(values=data, size=(30, 6), key='-ARRANGEMENTS-', select_mode='multiple')],
                [sg.Button('View Details'), sg.Button('Close')]  # Remove 'Add to Cart' for non-customers
            ]
        else:
            layout = [
             [sg.Text('Available Floral Arrangements')],
             [sg.Listbox(values=data, size=(30, 6), key='-ARRANGEMENTS-', select_mode='multiple')],
             [sg.Button('Prepare'), sg.Button('Close'), sg.Button('View Details')]
         ]
    
        window = sg.Window('View Flower Arrangements', layout)
        
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Close':
                window.close()
                break
            elif event == 'View Details':
                selected_arrangements = values['-ARRANGEMENTS-']
                if selected_arrangements:
                    arrangement_id = selected_arrangements[0][0]
                    self.view_floral_arrangement_details(arrangement_id)
            elif event == 'Add to Cart' and self.logged_in_user == 'customer':  # Ensure 'Add to Cart' is handled correctly
                selected_arrangements = values['-ARRANGEMENTS-']
                if selected_arrangements:
                    arrangement_ids = [arrangement[0] for arrangement in selected_arrangements]
                    self.add_to_cart(arrangement_ids)
            elif event == 'Prepare':
                selected_arrangements = values['-ARRANGEMENTS-']
                for arrangement in selected_arrangements:
                     fid = arrangement[0]  # assuming FID is the first element in the tuple
                     self.prepared_arrangements.append((self.logged_in_user, fid))
                sg.popup('Arrangements prepared and visible to admins')
                break
            else:
                sg.popup('No arrangements selected.')



    def add_to_cart(self, arrangement_ids):
        if not arrangement_ids:
            sg.popup('No arrangements provided to add to cart.')
            return
        for arrangement_id in arrangement_ids:
            try:
                self.cur.execute("SELECT price FROM Flower_arrangement WHERE FID = ?", (arrangement_id,))
                price_row = self.cur.fetchone()
                if price_row:
                    price = price_row[0]
                    gift_note = sg.popup_get_text('Enter a gift note:')
                    if gift_note is not None:
                        self.cart.append((arrangement_id, price, price, gift_note))
                        sg.popup('Flower arrangement added to cart!')
                    else:
                        sg.popup('No gift note entered. Item not added.')
                else:
                    sg.popup(f'Price not found for arrangement ID: {arrangement_id}')
            except Exception as e:
                sg.popup(f'An error occurred: {e}')


    
    def view_floral_arrangement_details(self, arrangement_id):
        # Çiçek düzenlemesinin detaylarını veritabanından al
        self.cur.execute("SELECT * FROM Flower_arrangement WHERE FID = ?", (arrangement_id,))
        arrangement_details = self.cur.fetchone()
        
        # Eğer çiçek düzenlemesi bulunamazsa
        if arrangement_details is None:
            print("Arrangement not found in the database.")  # Hata ayıklama
            sg.popup('Floral arrangement not found.')
            return
    
        # Detayları görüntülemek için bir pencere oluştur
        layout = [
            [sg.Text('Floral Arrangement Details')],
            [sg.Text(f'ID: {arrangement_details[0]}')],
            [sg.Text(f'Size: {arrangement_details[5]}')],
            [sg.Text(f'Type: {arrangement_details[4]}')],
            [sg.Text(f'Quantity: {arrangement_details[3]}')],
            [sg.Text(f'Price: {arrangement_details[2]}')],
            [sg.Text(f'Name: {arrangement_details[1]}')],
            [sg.Text(f'Design: {arrangement_details[6]}')],
            [sg.Button('Edit'), sg.Button('Close')]
        ]
        window = sg.Window('Floral Arrangement Details', layout)
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Close':
                window.close()
                break
            elif event == 'Edit':
                self.edit_flower_arrangement_window(arrangement_id)
        window.close()


    
    def edit_flower_arrangement_window(self, arrangement_id):
        # Yönetici mi kontrol et
        if self.logged_in_user != 'admin':
            sg.popup("Only admins can edit flower arrangements.")
            return
    
        # Seçilen düzenleme için bilgileri veritabanından al
        self.cur.execute("SELECT * FROM Flower_arrangement WHERE FID = ?", (arrangement_id,))
        arrangement_data = self.cur.fetchone()
        layout = [
            [sg.Text('Edit Flower Arrangement')],
            [sg.Text('ID:'), sg.InputText(key='-ID-', default_text=arrangement_data[0], disabled=True)],
            [sg.Text('Size:'), sg.InputText(key='-SIZE-', default_text=arrangement_data[5])],
            [sg.Text('Type:'), sg.InputText(key='-TYPE-', default_text=arrangement_data[4])],
            [sg.Text('Quantity:'), sg.InputText(key='-QUANTITY-', default_text=arrangement_data[3])],
            [sg.Text('Price:'), sg.InputText(key='-PRICE-', default_text=arrangement_data[2])],
            [sg.Text('Name:'), sg.InputText(key='-NAME-', default_text=arrangement_data[1])],
            [sg.Text('Design:'), sg.InputText(key='-DESIGN-', default_text=arrangement_data[6])],
            [sg.Button('Save'), sg.Button('Cancel')]
        ]
        window = sg.Window('Edit Flower Arrangement', layout)
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Cancel':
                break
            elif event == 'Save':
                # Değişiklikleri veritabanına kaydet
                self.cur.execute("UPDATE Flower_arrangement SET Fsize=?, Ftype=?, quantity=?, price=?, Fname=?, floral_description=? WHERE FID=?",
                                 (values['-SIZE-'], values['-TYPE-'], values['-QUANTITY-'], values['-PRICE-'], values['-NAME-'], values['-DESIGN-'], arrangement_id))
                self.conn.commit()  # Veritabanını güncelle
                sg.popup('Flower Arrangement updated successfully!')
                break
        window.close()


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
            [sg.Button('View Cart')],
            [sg.Button('Check Discounts')],  
            [sg.Button('View Orders')],
            [sg.Button('Logout')]
        ]
        window = sg.Window('Customer Menu', layout)
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Logout':
                break
            elif event == 'View Flower Arrangements':
                self.view_flower_arrangements_window()
            elif event == 'View Cart':
                self.view_cart()
            elif event == 'Check Discounts':
                self.view_discounts_window()
            elif event == 'View Orders':
                self.view_orders()

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
            [sg.Button('See Floral Arrangements')],
            [sg.Button('Waiting Orders')],
            [sg.Button('Logout')]
        ]
        window = sg.Window('Deliverer Menu', layout)
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Logout':
                break
            elif event == 'See Floral Arrangements':
                self.view_flower_arrangements_window()
            elif event == 'Waiting Orders':
                self.view_assigned_orders()
        window.close()

    def view_assigned_orders(self):
        # Fetch assigned orders data from the database
        self.cur.execute("""
            SELECT o.OrderID, o.order_date, o.delivery_date, o.paid_price, u.Ustatus
            FROM Orders o
            JOIN Updates u ON o.OrderID = u.OrderID
            WHERE o.Delivering_ID = ?
        """, (self.logged_in_user,))
        assigned_orders_data = self.cur.fetchall()  # Get all results
    
        # Check if there is data to display
        if not assigned_orders_data:
            sg.popup('No assigned orders found.')
            return
    
        # Define the layout with the table
        layout = [
            [sg.Text('Assigned Orders')],
            [sg.Table(values=assigned_orders_data, headings=['Order ID', 'Order Date', 'Delivery Date', 'Status'], key='-ORDERS-', enable_events=True)],
            [sg.Button('Edit'), sg.Button('Close')]
        ]
        window = sg.Window('View Assigned Orders', layout)
    
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Close':
                window.close()
                break
            elif event == 'Edit':
                if values['-ORDERS-']:  # Check if any rows are selected
                    try:
                        selected_order = values['-ORDERS-'][0]  # Get the first (and only) selected row index
                        # Continue processing the selected order
                    except IndexError:
                        sg.popup('No order selected. Please select an order to edit.')
                else:
                    sg.popup('No order selected. Please select an order to edit.')
    
        window.close()



    
    def edit_order_status(self, order_id):
        # Fetch current status
        self.cur.execute("SELECT Ustatus FROM updates WHERE OrderID=?", (order_id,))
        current_status = self.cur.fetchone()[0]
        new_status = not current_status  # Toggle status
        # Update the status in the database
        self.cur.execute("UPDATE updates SET Ustatus=? WHERE OrderID=?", (new_status, order_id))
        self.conn.commit()
        sg.popup('Status updated successfully!')
            
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
        self.cur.execute("SELECT ID FROM User WHERE email = ? AND Upassword = ?", (username, password))
        result = self.cur.fetchone()
        if result:
            return result[0]  # Kullanıcı ID'sini döndür
        return None
    
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
                user_id = self.customer_authentication(username, password)
                if user_id:
                    self.logged_in_user = 'customer'
                    self.user_id = user_id  # Kullanıcı ID'sini saklayın
                    self.customer_main_menu().read(close=True)
                    break
                else:
                    sg.popup('Invalid username or password.')
            elif event == 'Logout':
                self.logged_in_user = None
                self.user_id = None  # Kullanıcı çıkış yaptığında ID'yi de sıfırlayın
                break
    
                    
                
                
    def customer_authentication(self, username, password):
        self.cur.execute("SELECT ID FROM User WHERE email = ? AND Upassword = ?", (username, password))
        result = self.cur.fetchone()
        if result:
            return result[0]  # Kullanıcı ID'sini döndür
        return None

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
                deliverer_id = self.deliverer_authentication(username, password)  # Deliverer ID'sini al
                if deliverer_id:
                    self.logged_in_user = deliverer_id  # Deliverer ID'sini sakla
                    self.deliverer_main_menu()  # Deliverer ana menüsünü çağır
                    break
                else:
                    sg.popup('Invalid username or password.')
            elif event == 'Logout':
                self.logged_in_user = None
                break


    def deliverer_authentication(self, username, password):
        self.cur.execute("SELECT ID FROM User WHERE email = ? AND Upassword = ?", (username, password))
        result = self.cur.fetchone()
        if result:
            return result[0]  # Deliverer ID'sini döndür
        return None

    def view_orders(self):
        if self.user_id is None:
            sg.popup('Please login first.')
            return
    
        self.cur.execute("""
            SELECT o.OrderID, u.firstname, u.lastname, u.phone_number, o.order_date, o.delivery_date,
                   o.paid_price, o.gift_note, c.Caddress, uo.Ustatus
            FROM Orders o
            JOIN Customer c ON o.Placing_ID = c.CID
            JOIN User u ON c.CID = u.ID
            LEFT JOIN Updates uo ON o.OrderID = uo.OrderID
            WHERE o.Placing_ID = ?
        """, (self.user_id,))
        orders = self.cur.fetchall()
        if not orders:
            sg.popup('No orders found.')
            return
    
        # Ustatus değerlerini kontrol et ve ona göre "Complete" veya "Incomplete" ile değiştir
        formatted_orders = []
        for order in orders:
            formatted_order = list(order)
            if formatted_order[-1] == 1:  # Ustatus son sütunda olduğu için -1 kullanıldı ve sayısal karşılaştırma yapılıyor
                formatted_order[-1] = "Complete"
            else:
                formatted_order[-1] = "Incomplete"
            formatted_orders.append(formatted_order)
    
        layout = [
            [sg.Text('Your Orders')],
            [sg.Table(values=formatted_orders, headings=['Order ID', 'First Name', 'Last Name', 'Phone Number', 'Order Date', 'Delivery Date', 'Paid Price', 'Gift Note', 'Address', 'Status'], auto_size_columns=True)],
            [sg.Button('Close')]
        ]
        window = sg.Window('View Orders', layout)
        event, values = window.read()
        window.close()
    
    def view_orders_window(self):
        # Siparişleri veritabanından alın ve uygun şekilde göster
        self.cur.execute("""
            SELECT o.OrderID, u.ID, o.order_date, o.Containing_ID, uo.Ustatus
            FROM Orders o
            JOIN Customer c ON o.Placing_ID = c.CID
            JOIN User u ON c.CID = u.ID
            LEFT JOIN Updates uo ON o.OrderID = uo.OrderID
        """)
        orders_data = self.cur.fetchall()
    
        # Ustatus değerlerini "Completed" veya "Incomplete" olarak güncelle
        formatted_orders = []
        for order in orders_data:
            status = "Completed" if order[4] else "Incomplete"  # Ustatus değerini doğrudan kullan
            formatted_order = order[:4] + (status,)
            formatted_orders.append(formatted_order)
    
        # Siparişleri göstermek için bir pencere oluştur
        layout = [
            [sg.Text('Orders')],
            [sg.Table(values=formatted_orders, headings=['Order ID', 'Customer ID', 'Date', 'FID', 'Status'],
                      display_row_numbers=False, auto_size_columns=True, justification='left', enable_events=True, key='-ORDERS-')],
            [sg.Button('Assign Order'), sg.Button('Close')]
        ]
        window = sg.Window('View Orders', layout)
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Close':
                window.close()
                break
            elif event == 'Assign Order':
                if values['-ORDERS-']:  # Ensure a row is selected
                    selected_order_index = values['-ORDERS-'][0]
                    self.current_order_id = formatted_orders[selected_order_index][0]  # Assuming OrderID is at index 0
                    selected_fid = formatted_orders[selected_order_index][3]  # Assuming FID is at index 3
                    self.assign_orders(selected_fid)

        window.close()

    
    def assign_orders(self, selected_fid):
        filtered_pairs = [(did, fid) for did, fid in self.prepared_arrangements if fid == selected_fid]
        layout = [
            [sg.Text('Assign Orders to Deliverer')],
            [sg.Table(values=filtered_pairs, headings=['DID', 'FID'], display_row_numbers=False, auto_size_columns=True, key='-TABLE-')],
            [sg.Button('Assign'), sg.Button('Close')]
        ]
        window = sg.Window('Available Deliverers for Assignment', layout)
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Close':
                window.close()
                break
            elif event == 'Assign':
                if values['-TABLE-']:  # Check if any row is selected
                    selected_row_index = values['-TABLE-'][0]  # Get the first (and only) selection
                    did = filtered_pairs[selected_row_index][0]  # DID is the first element in the tuple
                    # Assuming you have a current_order_id attribute to store the order ID of the selected order
                    self.cur.execute("UPDATE updates SET DID=?, Ustatus=? WHERE OrderID=?", (did, True, self.current_order_id))
                    self.conn.commit()
                    sg.popup('Order assigned successfully!')
        window.close()



    def define_discounts_window(self):
        layout = [
            [sg.Text('Define Discounts')],
            [sg.Text('Code:'), sg.InputText(key='-DISCOUNT_CODE-')],
            [sg.Text('Start Date:'), sg.Input(key='-START_DATE-', enable_events=True), sg.CalendarButton('Choose', target='-START_DATE-', key='-START_DATE_PICKER-')],
            [sg.Text('End Date:'), sg.Input(key='-END_DATE-', enable_events=True), sg.CalendarButton('Choose', target='-END_DATE-', key='-END_DATE_PICKER-')],
            [sg.Text('Discount Percentage:'), sg.Input(key='-DISCOUNT_PERCENTAGE-')],
            [sg.Button('Save'), sg.Button('Cancel')]
        ]
        window = sg.Window('Define Discounts', layout)
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Cancel':
                break
            elif event == 'Save':
                discount_code = values['-DISCOUNT_CODE-']
                start_date = values['-START_DATE-']
                end_date = values['-END_DATE-']
                discount_percentage = values['-DISCOUNT_PERCENTAGE-']
                
                # İndirim kodunun benzersiz olup olmadığını kontrol et
                self.cur.execute("SELECT COUNT(*) FROM Discount WHERE discount_code = ?", (discount_code,))
                count = self.cur.fetchone()[0]
                if count > 0:
                    sg.popup("Discount code already exists. Please choose a different code.")
                else:
                    # Yeni indirimi veritabanına ekle
                    Entering_ID = self.logged_in_user
                    self.cur.execute("INSERT INTO Discount (discount_code, Entering_ID, Sdate, Edate, discount_perc) VALUES (?, ?, ?, ?, ?)",
                                     (discount_code, Entering_ID, start_date, end_date, discount_percentage))
                    self.conn.commit()
                    sg.popup('Discount defined successfully!')
                    break
        window.close()

    
    def view_cart(self):
        cart_display = [(arrangement_id, original_price, final_price, gift_note) for arrangement_id, original_price, final_price, gift_note in self.cart]
        layout = [
            [sg.Text('Cart')],
            [sg.Table(values=cart_display, headings=['Arrangement ID', 'Original Price', 'Final Price', 'Gift Note'], auto_size_columns=True)],
            [sg.Button('Order'), sg.Button('Close')]
        ]
        window = sg.Window('View Cart', layout)
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Close':
                window.close()
                break
            elif event == 'Order':
                self.place_order()
        window.close()


    def check_discounts(self):
            # Admin tarafından tanımlanan indirimleri veritabanından al
            self.cur.execute("SELECT discount_code, Entering_ID, discount_perc, Sdate, Edate FROM Discount")
            discounts_data = self.cur.fetchall()
        
            # Indirimleri göstermek için bir pencere oluştur
            layout = [
                [sg.Text('Available Discounts')],
                [sg.Table(values=discounts_data, headings=['Code', 'Start Date', 'End Date', 'Discount Percentage'],
                          display_row_numbers=False, auto_size_columns=True, justification='left')],
                [sg.Button('Close')]
            ]
            window = sg.Window('Available Discounts', layout)
            event, values = window.read()
            window.close()
            
    def check_cart_discounts(self):
        # Sepetteki diğer indirimleri kontrol et
        for item in self.cart:
            arrangement_id, _ = item
            # Eğer sepette başka bir indirim varsa, uyarı mesajı göster
            if self.is_discounted(arrangement_id):
                sg.popup('You cannot use more than one discount at the same time.')
                return False
        return True
    
    def is_discounted(self, arrangement_id):
        # Verilen çiçek düzenlemesi için bir indirim var mı kontrol et
        self.cur.execute("SELECT discount_code FROM Discount WHERE arrangement_id = ?", (arrangement_id,))
        discount_row = self.cur.fetchone()
        return discount_row is not None

    
    def view_discounts(self):
        self.cur.execute("SELECT discount_code, Entering_ID, discount_perc, Sdate, Edate FROM Discount")  # Sadece gerekli sütunları seç
        discounts_data = self.cur.fetchall()
    
        # Verileri alt listeler halinde düzenle
        formatted_discounts_data = [[code, enter_id, perc, str(start_date), str(end_date)] for code, enter_id, perc, start_date, end_date in discounts_data]
    
        layout = [
            [sg.Text('Discounts')],
            [sg.Listbox(values=formatted_discounts_data, size=(50, 6), key='-DISCOUNTS-', enable_events=True)],
            [sg.Button('Select Discount'), sg.Button('Close')]
        ]
        window = sg.Window('View Discounts', layout)
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Close':
                window.close()
                break
            elif event == 'Select Discount':
                selected_discount = values['-DISCOUNTS-']
                if selected_discount:
                    self.use_discount(selected_discount[3])  # İndirimleri bir liste olarak alıyorsunuz, bu yüzden ilk öğeyi seçin
        window.close()



    def use_discount(self, discount_code):
        # Veritabanından indirim yüzdesini al
        self.cur.execute("SELECT discount_perc FROM Discount WHERE discount_code = ?", (discount_code,))
        discount_row = self.cur.fetchone()
        if discount_row:
            discount_percentage = discount_row[0]  # Seçilen indirim yüzdesini al
    
            # Sepete indirimi uygula
            self.apply_discount_to_cart(discount_code)
    
            # Siparişi oluştur
            self.create_order(discount_code)

        
    def view_discounts_window(self):
        self.cur.execute("SELECT discount_code, discount_perc FROM Discount")
        discounts = self.cur.fetchall()
        if self.logged_in_user == "customer":
    
            layout = [
                [sg.Text('Available Discounts')],
                [sg.Table(values=discounts, headings=['Code', 'Percentage'], key='-TABLE-', enable_events=True)],
                [sg.Button('Apply Discount'), sg.Button('Cancel')]
            ]
        else:
            layout = [
                [sg.Text('Available Discounts')],
                [sg.Table(values=discounts, headings=['Code', 'Percentage'], key='-TABLE-', enable_events=True)],
                [sg.Button('Cancel')]
            ]
    
        window = sg.Window('Select Discount', layout, modal=True)  # Modal ekleyerek arka planın etkileşime kapatılması
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Cancel':
                break
            elif event == 'Apply Discount':
                if values['-TABLE-']:  # Seçim yapılmışsa
                    selected_index = values['-TABLE-'][0]
                    discount_code = discounts[selected_index][0]
                    discount_percentage = discounts[selected_index][1]
    
                    # Indirimi doğrulayın ve uygulayın
                    if self.check_discount_eligibility(discount_code):
                        self.apply_discount_to_cart(discount_percentage)
                        self.selected_discount = discount_code  # Seçilen indirimi sakla
                        sg.popup('Discount applied successfully!')
                        break
                    else:
                        sg.popup('This discount has already been used.')
        window.close()

    
    def apply_discount_to_cart(self, discount_percentage):
        for i, (arrangement_id, original_price, _, gift_note) in enumerate(self.cart):
            discounted_price = original_price * (1 - discount_percentage / 100)
            self.cart[i] = (arrangement_id, original_price, discounted_price, gift_note)
        sg.popup('Discount applied to cart!')

    
    def check_discount_eligibility(self, discount_code):
        self.cur.execute("SELECT * FROM enters WHERE CID = ? AND discount_code = ?", (self.user_id, discount_code))
        return not self.cur.fetchone()


    
    def select_discount(self, selected_discount):
        discount_code = selected_discount
        # Sepete indirim uygulayın
        self.apply_discount_to_cart(discount_code)


    def create_order(self, discount_code):
        total_price = self.calculate_total_price()
        
        # Sepetteki diğer indirimleri kontrol edin
        if not self.check_cart_discounts():
            return
        
        # Müşteriye indirim seçme penceresi gösterin
        selected_discount = self.select_discount_window()
        if selected_discount is None:
            return
        
        # Seçilen indirimi sepetteki toplam fiyata uygulayın
        discounted_price = self.apply_discount_to_cart(selected_discount)
        
        # Indirimi gösteren bir pop-up oluşturun ve altına "Place Order" butonunu ekleyin
        layout = [
            [sg.Text('Order Details')],
            [sg.Text(f'Total Price: {discounted_price}')],
            [sg.Button('View Order Details')]
        ]
        window = sg.Window('Order Details', layout)
        event, values = window.read()
        window.close()
        
        # "View Order Details" butonuna basıldığında siparişi oluşturun
        if event == 'View Order Details':
            self.create_order(discounted_price)  # Seçilen indirim kodunu parametre olarak geçirin


    def update_cart(self):
        for i, (arrangement_id, price) in enumerate(self.cart):
            discounted_price = price
            if self.selected_discount:
                discounted_price = self.apply_discount_to_cart(self.selected_discount)
            self.cart[i] = (arrangement_id, discounted_price)
    
    def select_discount_window(self):
        # İndirimleri veritabanından al
        self.cur.execute("SELECT discount_code, Entering_ID, discount_perc, Sdate, Edate FROM Discount")
        discounts = self.cur.fetchall()
    
        # İndirimleri göstermek için bir pencere oluştur
        layout = [
            [sg.Text('Select Discount')],
            [sg.Table(values=discounts, headings=['Discount Code', 'Entering ID', 'Discount Percentage', 'Start Date', 'End Date'], auto_size_columns=True, display_row_numbers=False, justification='left')],
            [sg.Button('Select Discount')]
        ]
        window = sg.Window('Discounts', layout)
        event, values = window.read()
        window.close()
    
        # "Select Discount" butonuna basıldığında seçili indirimin yüzdesini döndür
        if event == 'Select Discount':
            selected_row = values[0]
            selected_discount_percentage = discounts[selected_row][2]  # Seçilen satırdaki "discount percentage" sütununu al
            return selected_discount_percentage
        else:
            return None
    
    def apply_discount(self):
        if not self.selected_discount:
            sg.popup('Please select a discount first.')
            return
    
        # Müşteri tarafından daha önce kullanılan indirimleri kontrol et
        self.cur.execute("SELECT * FROM enters WHERE CID = ? AND discount_code = ?", (self.logged_in_user, self.selected_discount))
        if self.cur.fetchone():
            sg.popup('This discount has already been used.')
            return  # İndirim zaten kullanılmış
    
        # İndirim kullanılmamışsa, indirimi uygula ve kaydet
        self.cur.execute("INSERT INTO enters (CID, discount_code) VALUES (?, ?)", (self.logged_in_user, self.selected_discount))
        self.conn.commit()
    
        # Sepeti güncelle
        self.update_cart()
    
        # Sepeti yeniden görüntüle
        self.view_cart()
        sg.popup('Discount applied successfully!')


    def place_order(self):
        if not self.user_id:
            sg.popup("Lütfen sipariş vermek için önce giriş yapın.")
            return
    
        order_date = datetime.now().strftime('%Y-%m-%d')
        default_delivering_id = 0  # Teslimatçı henüz atanmadığı için varsayılan değer
    
        for arrangement_id, _, final_price, gift_note in self.cart:
            order_id = self.generate_order_id()
            self.cur.execute(
                "INSERT INTO Orders (OrderID, Placing_ID, Delivering_ID, Containing_ID, order_date, delivery_date, paid_price, gift_note) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (order_id, self.user_id, default_delivering_id, arrangement_id, order_date, None, final_price, gift_note))
            self.conn.commit()
    
        sg.popup('Order placed successfully!')
        self.cart.clear()  # Sipariş verildikten sonra sepeti temizle
        self.selected_discount = None  # Seçilen indirimi sıfırla


    def check_discount_usage(self, discount_code, user_id):
        """Belirli bir kullanıcı için belirli bir indirim kodunun daha önce kullanılıp kullanılmadığını kontrol eder."""
        self.cur.execute("SELECT * FROM enters WHERE CID = ? AND discount_code = ?", (user_id, discount_code))
        return self.cur.fetchone() is not None




    def calculate_total_price(self):
        total_price = 0
        for arrangement_id, _ in self.cart:
            # Retrieve the price of each arrangement from the database and add it to the total price
            self.cur.execute("SELECT price FROM Flower_arrangement WHERE FID = ?", (arrangement_id,))
            price_row = self.cur.fetchone()
            if price_row:
                total_price += price_row[0]
        return total_price

    def order_flowers(self):
        # Sepetteki toplam fiyatı hesaplayın
        total_price = self.calculate_total_price()
        
        # Sepetteki diğer indirimleri kontrol edin
        if not self.check_cart_discounts():
            return
        
        # Müşteriye indirim seçme penceresi gösterin
        selected_discount = self.select_discount_window()
        if selected_discount is None:
            return
        
        # Seçilen indirimi sepetteki toplam fiyata uygulayın
        discounted_price = self.apply_discount_to_cart(selected_discount)
        
        # Indirimi gösteren bir pop-up oluşturun ve altına "Place Order" butonunu ekleyin
        layout = [
            [sg.Text('Order Details')],
            [sg.Text(f'Total Price: {discounted_price}')],
            [sg.Button('View Order Details')]
        ]
        window = sg.Window('Order Details', layout)
        event, values = window.read()
        window.close()
        
        # "View Order Details" butonuna basıldığında siparişi oluşturun
        if event == 'View Order Details':
            self.create_order(selected_discount)  # Seçilen indirim kodunu parametre olarak geçirin

    def view_order_history_window(self):
        # Sipariş geçmişini veritabanından al
        self.cur.execute("SELECT * FROM Orders WHERE Placing_ID = ?", (self.logged_in_user,))
        order_history = self.cur.fetchall()
    
        # Sipariş geçmişini göstermek için bir pencere oluştur
        layout = [
            [sg.Text('Order History')],
            [sg.Table(values=order_history, headings=['Order ID', 'Placing ID', 'Delivery ID', 'Containing ID', 'Order Date', 'Delivery Date', 'Paid Price', 'Gift Note'], auto_size_columns=True, display_row_numbers=False, justification='left')],
            [sg.Button('Close')]
        ]
        window = sg.Window('Order History', layout)
        event, values = window.read()
        window.close()
        

    def generate_order_id(self):
        # Veritabanından son OrderID'yi alıp bir sonraki ID'yi üret
        self.cur.execute("SELECT OrderID FROM Orders ORDER BY OrderID DESC LIMIT 1")
        last_order_id = self.cur.fetchone()
        if last_order_id:
            last_order_num = int(last_order_id[0][3:])  # "ORD001" formatından sayı kısmını al
            new_order_id = f"ORD{last_order_num + 1:03d}"  # Yeni ID'yi formatla
        else:
            new_order_id = "ORD001"  # Eğer sipariş yoksa, ilk ID
        return new_order_id
    
    
    def update_delivery_id(self, order_id, deliverer_id):
        self.cur.execute("UPDATE Orders SET Delivering_ID = ? WHERE OrderID = ? AND Delivering_ID = 0", (deliverer_id, order_id))
        self.conn.commit()
        sg.popup('Delivery ID updated successfully!')

# END OF FUNCTIONAL REQ 2



app = FlowerShopUI()
app.run()