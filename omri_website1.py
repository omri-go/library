from flask import Flask, request,render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date, timedelta

BOOK_TYPE_1_LOAN_LENGTH = 10
BOOK_TYPE_2_LOAN_LENGTH = 5
BOOK_TYPE_3_LOAN_LENGTH = 2

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Books.sqlite3'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    published_year = db.Column(db.Integer, nullable=False)
    type = db.Column(db.Integer, nullable=False)
    copies = db.Column(db.Integer, nullable=False)

    def __init__(self, name, author, published_year, type, copies):
        self.name = name
        self.author = author
        self.published_year = published_year
        self.type = type
        self.copies = copies

class Customers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    city =  db.Column(db.String(50), nullable=False)

    def __init__(self, name, age, city):
        self.name = name
        self.age = age
        self.city = city

class Loans(db.Model):    
    customer_id = db.Column(db.Integer, db.ForeignKey(Customers.id), primary_key=True, nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey(Books.id), primary_key=True, nullable=False)
    loan_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date, nullable=False)

    def __init__(self, customer_id, book_id, loan_date, return_date):
        self.customer_id = customer_id
        self.book_id = book_id
        self.loan_date = loan_date
        self.return_date = return_date

@app.route("/")
def home():
    return  render_template('index.html') 


######## show books data ########
@app.route("/books_data/<ind>/")
@app.route("/books_data/", methods=['GET', 'POST'])
def books_data():
    if request.method == 'GET':
        # all books
        return render_template('books_all.html',books= Books.query.all(), title="All books") 
    else:
        # method == POST
        # search for single customer
        book_name = request.form['book_name'] 
        
        books2=[]
        for b in Books.query.all(): 
            if b.name == book_name:
                books2.append(b)
        return render_template('books_all.html',books= books2, title="Books Search Results") 


######## add a book ########
@app.route("/add_book/", methods=['POST','GET'])
def add_book():
    if request.method == 'POST':        
        name = request.form['name']
        author = request.form['author']
        published_year = request.form['published_year']
        book_type = request.form['type']
        copies = request.form['copies']
         
        newbook= Books(name, author, published_year, book_type, copies)
        db.session.add (newbook)
        db.session.commit()
         
        return render_template('show_message.html', user_message="Added a new book")
    else:
        #method is GET
        return render_template('add_book.html')

######## delete a book ########
@app.route("/delete/<ind>", methods=['DELETE','GET'])
def delete_book(ind=-1):
        book=Books.query.get(int(ind))
        if book:
            db.session.delete(book)
            db.session.commit()
                                
            return render_template('show_message.html', user_message="Book deleted")  
        else:            
            return render_template('show_message.html', user_message="book not found")


######## update a book ########
@app.route("/update/<ind>", methods=['GET', 'POST'])
def update_book(ind=-1):
    if int(ind) > -1:

        book=Books.query.get(int(ind))
        if not book:                      
           return render_template('show_message.html', user_message="no such book to update")

        if request.method == 'GET':
            return render_template('update_book.html', book=book)
        else:
           # request.method == 'POST'
           # update book data                      
           book.name = request.form['name']
           book.author = request.form['author']
           book.published_year = request.form['published_year']
           book.book_type = request.form['type']
           book.copies = request.form['copies']

           db.session.commit()
           
           # tell user the book was updated succesfully           
           return render_template('show_message.html', user_message="updated book data")           


######## Customers ########

######## show customer data ########
@app.route("/customers_data/", methods=['GET', 'POST'])
def customers_data():
    if request.method == 'GET':
        # all customers
        return render_template('customer_all.html',customers= Customers.query.all(), title="All Customers") 
    else:
        # method == POST
        # search for single customer
        customer_name = request.form['customer_name'] 
        
        customers2=[]
        for c in Customers.query.all(): 
            if c.name == customer_name:
                customers2.append(c)
        return render_template('customer_all.html',customers= customers2, title="Customers Search Results") 

######## add a customer ########
@app.route("/add_customer/", methods=['POST','GET'])
def add_customer():
    if request.method == 'POST':        
        name = request.form['name']
        age = request.form['age']
        city = request.form['city']        
         
        new_customer= Customers(name, age, city)
        db.session.add (new_customer)
        db.session.commit()
                 
        return render_template('show_message.html', user_message="Added a new customer")
    else:
        #method is GET
        return render_template('add_customer.html')

######## delete a customer ########
@app.route("/delete_customer/<ind>", methods=['DELETE','GET'])
def delete_customer(ind=-1):
        customer=Customers.query.get(int(ind))
        if customer:
            db.session.delete(customer)
            db.session.commit()
                                
            return render_template('show_message.html', user_message="Customer deleted")  
        else:            
            return render_template('show_message.html', user_message="Customer not found")

######## update a customer ########
@app.route("/update_customer/<ind>", methods=['GET', 'POST'])
def update_customer(ind=-1):
    if int(ind) > -1:

        customer=Customers.query.get(int(ind))
        if not customer:                
           return render_template('show_message.html', user_message="no such book to update")

        if request.method == 'GET':
            return render_template('update_customer.html', customer=customer)
        else:
           # request.method == 'POST'
           # update book data                      
           customer.name = request.form['name']
           customer.age = request.form['age']
           customer.city = request.form['city']           

           db.session.commit()
           
           # tell user the book was updated succesfully              
           return render_template('show_message.html', user_message="updated customer data")           




###### Loans #######

######## show loans data ########
@app.route("/loans_data/<cust_id>_<book_id>/")
@app.route("/loans_data/late_loans/")
@app.route("/loans_data/")
def loans_data(cust_id=-1, book_id=-1):

    # late loans
    if request.path=="/loans_data/late_loans/":        
        late_loans1 = Loans.query.all()
        late_loans2 = []
        for l in late_loans1: 
            if l.return_date < date.today():
                late_loans2.append(l)

        return render_template('loans_all.html',loans= late_loans2, title="Late Loans") 

    # one loan data
    elif int(cust_id)>-1 and int(book_id)>-1:   
        loan = [Loans.query.get((cust_id, book_id))]
        return render_template('loans_all.html',loans=loan, title="One Loan Data") 
    
    # all loans data
    return render_template('loans_all.html',loans= Loans.query.all(), title="All Loans") 
    

# return how long the book can be loaned based on its type
def get_loan_length_by_book_type(book_id):
    b_type = Books.query.get(int(book_id)).type
    if b_type==1:
        return BOOK_TYPE_1_LOAN_LENGTH
    elif b_type==2:
        return BOOK_TYPE_2_LOAN_LENGTH
    elif b_type==3:
        return BOOK_TYPE_3_LOAN_LENGTH
    else:
        print("unreconized book type " + str(b_type))
        return BOOK_TYPE_1_LOAN_LENGTH


######## add a loan ########
@app.route("/add_loan/", methods=['POST','GET'])
def add_loan():
    if request.method == 'POST':        
        customer_name = request.form['customer_name']
        book_name = request.form['book_name']      

        # find ids of customer and book
        customer_id = None
        for c in Customers.query.all(): 
            if c.name==customer_name:
                customer_id = c.id

        book_id = None
        for b in Books.query.all(): 
            if b.name==book_name:
                book_id = b.id        

        loan_date = date.today()
        loan_length = get_loan_length_by_book_type(book_id)        
        return_date = date.today() + timedelta(days=loan_length)

        if customer_id==None: return render_template('show_message.html', user_message="Can't find customer with the given name")             
        elif book_id == None: return render_template('show_message.html', user_message="Can't find book with the given name")
        elif Books.query.get(int(book_id)).copies <=0: return render_template("No available copies")

        l = Loans.query.get((customer_id, book_id))
        if l!=None: return render_template('show_message.html', user_message="Loan already exists")                 
        
        new_loan= Loans(customer_id, book_id, loan_date, return_date)
        Books.query.get(int(book_id)).copies -=1
        db.session.add (new_loan)
        db.session.commit()
        return render_template('show_message.html', user_message="Added a new loan. Return date is: " + str(return_date))
        
    else:
        #method is GET
        return render_template('add_loan.html')

######## delete a loan ########
@app.route("/delete_loan/<cust_id>_<book_id>", methods=['GET'])
def delete_loan(cust_id=-1, book_id=-1):
        # find the loan
        loan = Loans.query.get((cust_id, book_id))

        if loan:
            Books.query.get(int(book_id)).copies +=1
            db.session.delete(loan)
            db.session.commit()
                        
            return render_template('show_message.html', user_message="loan deleted")  
        else:             
            return render_template('show_message.html', user_message="loan not found")


######## update a loan ########
@app.route("/update_loan/<cust_id>_<book_id>", methods=['GET', 'POST'])
def update_loan(cust_id=-1, book_id=-1):
    loan = Loans.query.get((cust_id, book_id))
    # if loan not found
    if not loan: return render_template('show_message.html', user_message="loan not found")

    if request.method == 'GET':
        return render_template('update_loan.html', loan=loan)
    else:
        # request.method == 'POST'
        loan = Loans.query.get((cust_id, book_id))
                        
        # update loan data
        loan.loan_date = datetime.strptime(request.form['loan_date'], "%Y-%m-%d")
        loan.return_date = datetime.strptime(request.form['return_date'], "%Y-%m-%d")

        db.session.commit()
           
        # tell user the loan was updated succesfully
        return render_template('show_message.html', user_message="updated customer data")               



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

