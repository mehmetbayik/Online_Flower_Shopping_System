# CS281 Computers and Data Organization Term Project

## Project Description

Online Flower Shopping System is implemented using SqLite3, pysimplegui, and python. The system has three different user roles: admin, customer, and deliverer. Admins can add, delete, edit, and view flower arrangements. They can also define discounts and assign orders to deliverers. Customers can view flower arrangements, add them to their cart, and give orders. They can also view their order history. Deliverers can see the orders assigned to them, update the delivery status, and delivery date.

## Functional Requirements

- Log into the system as an admin. Add flower arrangement information into the database, including the floral arrangement ID, size, type, quantity, price, name, and floral design. Delete one of the flower arrangement information. View the list of existing floral arrangements; you will see the details separately when you click on them. Then, select one and edit its information. Log out and log in as a customer. List all the flower arrangements. Select one and see its details in a separate window. Choose one or more arrangements and add them to your cart. Then, go and check your cart.

- Log in to the system as admin, and define some discounts with detailed information (code, start date, end date, discount percentage). Then, log out and log in to the system as a customer. List the flower arrangements you have. Choose one or more arrangements and add them to your cart. Then, go and check your cart. Enter a gift note. Afterwards, check the discounts defined by the admin. See detailed discount information (code, start date, end date, discount percentage). Choose one discount, and show that you cannot use two discounts at the same time. After the price deduction, give the order. Now go back and see your order history and detailed floral arrangement information along with receiver information, order ID, price, gift note, date of order, date of delivery, and delivery status. The delivery status should seem as “Incomplete” since it is the default situation until the deliverer updates the delivery status; in that case, the delivery date is null. Make sure that you cannot use the same discount twice.

- Log in to the system as a deliverer. See the floral arrangements available in the dataset. Choose the arrangements you can prepare for the orders, and then you will be visible for the admins to assign the orders to you. Log out and log in as the customer and give two orders, and one order should include a discount code. Log out and log in as admin. Assign the orders to the deliverers available. Log out and log in as a deliverer having a waiting order. List the orders you got. Approve the delivery status of your order(s) as “Complete” and update the delivery dates. Log out and log in as the customer. See the order history. The status of your previous order needs to be “Complete” as the deliverer updated the status.

## License  
[MIT](https://choosealicense.com/licenses/mit/)  
