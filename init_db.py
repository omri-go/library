from omri_website1 import db, app, Books, Customers, Loans

book1 = Books(name= "omri", author= "susana", published_year= 1991, type= 1, copies= 1)
book2 = Books(name= "Winnie-the-Pooh", author= "Alan Alexander Milne", published_year= 1924, type= 2, copies= 10)
book3 = Books(name= "X-Men", author= "Stan Lee", published_year= 1963, type= 3, copies= 20)

customer1 = Customers(name= "omri", age= 30 , city= "Hadera")
customer2 = Customers(name= "maria", age= 26 , city= "Had nes")
customer3 = Customers(name= "Karl", age= 90 , city= "Had ofan")

# loans1 = Loans(customers_id= 1, book_id= 1)
# loans2 = Loans(customers_id= 2, book_id= 2)
# loans3 = Loans(customers_id= 3, book_id= 3)

with app.app_context():
    db.session.add_all([book1, book2, book3, customer1, customer2,customer3])#,loans1,loans2,loans3
    db.session.commit()