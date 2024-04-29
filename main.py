import sqlite3
from datetime import datetime
import PySimpleGUI as sg

class FlowerShopUI:
    def __init__(self):
        self.conn = sqlite3.connect("project-stage2.db")
        self.cur = self.conn.cursor()
        self.logged_in_user = None
        self.cart = []
        self.discounts = []

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
            [sg.Button('View Orders')],  # "View Orders" butonunu ekleyin
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
            elif event == 'Define Discounts':
                self.define_discounts_window()
            elif event == 'View Discounts':
                self.view_discounts_window()
            elif event == 'View Orders':  # "View Orders" butonuna tıklandığında
                self.view_orders_window()  # view_orders_window() fonksiyonunu çağırıyoruz
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
        self.cur.execute("SELECT FID, Fname FROM Flower_arrangement")
        data = self.cur.fetchall()
        layout = [
            [sg.Text('Floral Arrangements')],
            [sg.Listbox(values=data, size=(30, 6), key='-ARRANGEMENTS-', enable_events=True, select_mode='multiple')],  # enable_events=True ve select_mode='multiple' ekleyin
            [sg.Button('View Details'), sg.Button('Close')]
        ]
        # Giriş yapılan kullanıcının türüne göre Add to Cart butonunu ekleyelim
        if self.logged_in_user == 'customer':
            layout[1].insert(-1, sg.Button('Add to Cart'))
        window = sg.Window('View Flower Arrangements', layout)
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Close':
                break
            elif event == 'View Details':
                selected_arrangements = values['-ARRANGEMENTS-']
                if selected_arrangements:
                    arrangement_ids = [arrangement[0] for arrangement in selected_arrangements]  # Seçilen düzenleme ID'lerini alın
                    for arrangement_id in arrangement_ids:
                        self.view_floral_arrangement_details(arrangement_id)
            elif event == 'Add to Cart' and self.logged_in_user == 'customer':  # Sadece müşteri kullanıcılar için Add to Cart işlevselliğini kontrol edelim
                selected_arrangements = values['-ARRANGEMENTS-']
                if selected_arrangements:
                    arrangement_ids = [arrangement[0] for arrangement in selected_arrangements]  # Seçilen düzenleme ID'lerini alın
                    self.add_to_cart(arrangement_ids)
        window.close()
    



    
    
    
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
            [sg.Text(f'Name: {arrangement_details[5]}')],  # Sütun indislerini kontrol edelim
            [sg.Text(f'Price: {arrangement_details[4]}')],
            [sg.Text(f'Quantity: {arrangement_details[3]}')],
            [sg.Text(f'Type: {arrangement_details[2]}')],
            [sg.Text(f'Size: {arrangement_details[1]}')],
            [sg.Text(f'Design: {arrangement_details[6]}')],
            [sg.Button('Edit'), sg.Button('Close')]
        ]
        window = sg.Window('Floral Arrangement Details', layout)
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Close':
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
            [sg.Button('View Orders')],
            [sg.Button('Update Delivery Status')],
            [sg.Button('Logout')]
        ]
        window = sg.Window('Deliverer Menu', layout)
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Logout':
                break
            elif event == 'View Orders':
                self.view_deliverer_orders()  # Deliverer için siparişleri görüntüleme fonksiyonu
            elif event == 'Update Delivery Status':
                self.update_delivery_status_window()  # Teslimat durumunu güncelleme fonksiyonu
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
                user_id = self.customer_authentication(username, password)  # Kullanıcı ID'sini al
                if user_id:
                    self.logged_in_user = user_id  # Kullanıcı ID'sini sakla
                    self.customer_main_menu().read(close=True)
                    break
                else:
                    sg.popup('Invalid username or password.')
            elif event == 'Logout':
                self.logged_in_user = None
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
        self.cur.execute("SELECT DID FROM User WHERE email = ? AND Upassword = ?", (username, password))
        result = self.cur.fetchone()
        if result:
            return result[0]  # Deliverer ID'sini döndür
        return None

        
    def view_orders(self):
        self.cur.execute("SELECT * FROM Orders WHERE Placing_ID = ?", (self.logged_in_user,))
        orders = self.cur.fetchall()
        if not orders:
            sg.popup('No orders found.')
            return
        layout = [
            [sg.Text('Your Orders')],
            [sg.Table(values=orders, headings=['Order ID', 'Placing ID', 'Delivering ID', 'Containing ID', 'Order Date', 'Delivery Date', 'Paid Price', 'Gift Note'], auto_size_columns=True)],
            [sg.Button('Close')]
        ]
        window = sg.Window('View Orders', layout)
        event, values = window.read()
        window.close()


    
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
        event, values = window.read()
        window.close()

    def add_to_cart(self, arrangement_ids):
        gift_note = sg.popup_get_text('Enter a gift note:')  # Kullanıcıdan hediye notunu al
        for arrangement_id in arrangement_ids:
            self.cur.execute("SELECT price FROM Flower_arrangement WHERE FID = ?", (arrangement_id,))
            price_row = self.cur.fetchone()
            if price_row:
                price = price_row[0]  # Fiyatı veritabanından al
                # cart listesine çiçek düzenlemesi ID'si, orijinal fiyatı, son fiyat (başlangıçta orijinal fiyatla aynı), ve hediye notunu ekle
                self.cart.append((arrangement_id, price, price, gift_note))
            else:
                print("Price not found for arrangement ID:", arrangement_id)



        
        
        
#### END OF FUNCTIONAL REG 1

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
        self.cur.execute("SELECT discount_code, Entering_ID, discount_perc, Sdate, Edate FROM Discount")
        data = self.cur.fetchall()

        layout = [
            [sg.Text('Discounts')],
            [sg.Table(values=data, headings=["Code", "Enter ID", "Discount Percentage", "Start Date", "End Date"], auto_size_columns=True, display_row_numbers=False, justification='center', key='-DISCOUNTS-')],
            [sg.Button('Select Discount'), sg.Button('Close')]
        ]
        window = sg.Window('View Discounts', layout)
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Close':
                break
            elif event == 'Select Discount':
                selected_row = values['-DISCOUNTS-'][0]
                selected_discount = data[selected_row][2]  # Seçilen satırdaki "discount_perc" sütununu al
                if selected_discount:
                    self.selected_discount = selected_discount  # Seçilen indirim yüzdesini kaydet
                    confirmation_layout = [
                        [sg.Text(f'You selected discount percentage: {self.selected_discount}%. Do you want to apply this discount?')],
                        [sg.Button('Yes'), sg.Button('No')]
                    ]
                    confirmation_window = sg.Window('Confirm Discount Selection', confirmation_layout)
                    confirmation_event, _ = confirmation_window.read()
                    confirmation_window.close()
                    if confirmation_event == 'Yes':
                        self.apply_discount_to_cart(self.selected_discount)
                    self.selected_discount = None  # Seçilen indirimi sıfırla
        window.close()


    
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


    
    
    def apply_discount_to_cart(self, discount_percentage):
        for i, (arrangement_id, original_price, final_price, gift_note) in enumerate(self.cart):
            try:
                original_price = float(original_price)
                discounted_price = original_price * (1 - discount_percentage / 100)
                # cart listesini güncelle
                self.cart[i] = (arrangement_id, original_price, discounted_price, gift_note)
            except ValueError:
                print("Error: Price must be a number. Received:", original_price)
                continue


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
    
        # Sepetin güncellenmesi
        self.update_cart()
        
        # Sepeti yeniden görüntüleme
        self.view_cart()



    def place_order(self):
        print("Placing ID:", self.logged_in_user)  # Kullanıcı ID'sini kontrol et
        placing_id = sg.popup_get_text('Please enter your Customer ID:')
        if not placing_id:
            sg.popup('No Customer ID provided. Order canceled.')
            return
    
        order_date = datetime.now().strftime('%Y-%m-%d')
        default_delivering_id = 0  # Teslimatçı henüz atanmadığı için varsayılan değer
    
        for arrangement_id, _, final_price, gift_note in self.cart:
            order_id = self.generate_order_id()
            self.cur.execute(
                "INSERT INTO Orders (OrderID, Placing_ID, Delivering_ID, Containing_ID, order_date, delivery_date, paid_price, gift_note) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (order_id, placing_id, default_delivering_id, arrangement_id, order_date, None, final_price, gift_note))
            self.conn.commit()
        
        sg.popup('Order placed successfully!')
        self.cart.clear()  # Sipariş verildikten sonra sepeti temizle



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


app = FlowerShopUI()
app.run()
