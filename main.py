import sqlite3
import PySimpleGUI as sg

class FlowerShopUI:
    def __init__(self):
        self.conn = sqlite3.connect("project-stage2.db")
        self.cur = self.conn.cursor()
        self.logged_in_user = None
        self.cart = []

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
            [sg.Button('Define Discounts')],  # Define Discounts butonunu ekleyin
            [sg.Button('View Discounts')],  # View Discounts butonunu ekleyin
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
                self.define_discounts_window().read(close=True)
            elif event == 'View Discounts':
                self.view_discounts_window().read(close=True)  # View Discounts butonuna tıklandığında view_discounts_window fonksiyonunu çağırın
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
            [sg.Button('Check Discounts')],  # Check Discounts butonunu ekle
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
            elif event == 'Check Discounts':  # Check Discounts butonuna basıldığında
                self.view_discounts_window()  # view_discounts_window fonksiyonunu çağır
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

    def add_to_cart(self, arrangement_ids):
        layout = [
            [sg.Text('Enter a gift note:')],
            [sg.InputText(key='-GIFT_NOTE-')],
            [sg.Button('Add to Cart')]
        ]
        window = sg.Window('Add Gift Note', layout)
        event, values = window.read()
        window.close()
        gift_note = values['-GIFT_NOTE-']
    
        for arrangement_id in arrangement_ids:
            self.cart.append((arrangement_id, gift_note))
        sg.popup('Selected arrangements added to cart successfully!')

        
        
        
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
                # Kullanıcının kimliğini belirleyin
                Entering_ID = self.logged_in_user
                # Indirimi veritabanına ekleyin
                self.cur.execute("INSERT INTO Discount (discount_code, Entering_ID, Sdate, Edate, discount_perc) VALUES (?, ?, ?, ?, ?)",
                                 (discount_code, Entering_ID, start_date, end_date, discount_percentage))
                self.conn.commit()
                sg.popup('Discount defined successfully!')
                break
        window.close()
    

    def view_cart(self):
        layout = [
            [sg.Text('Your Cart')],
            [sg.Listbox(values=[f"ID: {arrangement[0]} - Gift Note: {arrangement[1]}" for arrangement in self.cart], size=(60, 6), key='-CART-')],
            [sg.Button('Close')]
        ]
        window = sg.Window('View Cart', layout)
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Close':
                break
        window.close()

    def check_discounts(self):
            # Admin tarafından tanımlanan indirimleri veritabanından al
            self.cur.execute("SELECT * FROM Discount")
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
                arrangement_id, gift_note = item
                # Eğer sepette başka bir indirim varsa, uyarı mesajı göster
                if self.is_discounted(arrangement_id):
                    sg.popup('You cannot use more than one discount at the same time.')
                    return False
            return True
    
    def is_discounted(self, arrangement_id):
            # Verilen çiçek düzenlemesi için bir indirim var mı kontrol et
            # Bu işlev gerçek veritabanı sorgusu ile değiştirilmelidir
            return True  # Örnek olarak her zaman True döndürüyoruz, gerçek sorguyu eklemeniz gerekiyor

    def view_discounts(self):
        self.cur.execute("SELECT * FROM Discount")
        discounts_data = self.cur.fetchall()

        layout = [
            [sg.Text('Discounts')],
            [sg.Listbox(values=discounts_data, size=(50, 6), key='-DISCOUNTS-', enable_events=True)],
            [sg.Button('Select Discount'),sg.Button('Close')]
        ]
        window = sg.Window('View Discounts', layout)
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Close':
                break
            elif event == 'Select Discount':
                selected_discount = values['-DISCOUNTS-']
                if selected_discount:
                    self.use_discount(selected_discount[0])  # İndirimleri bir liste olarak alıyorsunuz, bu yüzden ilk öğeyi seçin
        window.close()

    def use_discount(self, selected_discount):
        # Seçilen indirimin yüzdesini ve kodunu alın
        discount_code, discount_percentage = selected_discount
    
        # Sepet fiyatına seçilen indirimi uygulayın
        discounted_price = self.apply_discount_to_cart(discount_percentage)
    
        # Sipariş oluşturmak için indirimli fiyatı kullanın
        self.create_order(discounted_price)

        
    def view_discounts_window(self):
        self.cur.execute("SELECT * FROM Discount")
        data = [list(row) for row in self.cur.fetchall()]  # Demetlerden oluşan bir listeye dönüştür
        layout = [
            [sg.Text('Discounts')],
            [sg.Table(values=data, headings=["Code", "Enter ID", "Discount Percentage", "Start Date", "End Date"], auto_size_columns=True, display_row_numbers=True, justification='center', key='-DISCOUNTS-')],
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
                    self.select_discount(selected_discount[0])  
        window.close()



    
    def select_discount(self, selected_discount):
        discount_code = selected_discount
        # Sepete indirim uygulayın
        self.apply_discount_to_cart(discount_code)



    
    def create_order(self, total_price):
            layout = [
                [sg.Text('Enter your address:')],
                [sg.InputText(key='-ADDRESS-')],
                [sg.Button('Submit Order')]
            ]
            window = sg.Window('Address Entry', layout)
            event, values = window.read()
            window.close()
            address = values['-ADDRESS-']
        
            # Sipariş bilgilerini veritabanına ekleyin
            self.cur.execute("INSERT INTO Orders (CID, total_price, address) VALUES (?, ?, ?)",
                             (self.logged_in_user, total_price, address))
            self.conn.commit()
            sg.popup('Order submitted successfully!')
    
    
    def apply_discount_to_cart(self, discount_code):
        print("Selected discount code:", discount_code)
        discounted_prices = []
        # Indirim bilgilerini al
        self.cur.execute("SELECT discount_code, Sdate, Edate, discount_perc FROM Discount WHERE discount_code = ?", (discount_code,))
        discount_row = self.cur.fetchone()
        if discount_row:
            discount_code, start_date, end_date, discount_percentage = discount_row
            print("Discount Code:", discount_code)
            print("Start Date:", start_date)
            print("End Date:", end_date)
            print("Discount Percentage:", discount_percentage)
            for arrangement_id, _ in self.cart:
                self.cur.execute("SELECT price FROM Flower_arrangement WHERE FID = ?", (arrangement_id,))
                price_row = self.cur.fetchone()
                if price_row:
                    arrangement_price = price_row[0]
                    discounted_price = arrangement_price * (1 - discount_percentage / 100)
                    discounted_prices.append(discounted_price)
        return discounted_prices







app = FlowerShopUI()
app.run()
