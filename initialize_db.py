import sqlite3
conn = sqlite3.connect('example.db')

c = conn.cursor()

# Create table
# c.execute('''CREATE TABLE orders
#              (text, trans text, symbol text, qty real, price real)''')


# Insert a row of data
# c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

# EXISTING ORDERS
# Create table
c.execute('''CREATE TABLE orders
             (order_date, order_number, order_email, color, size, status)''')

# data to be added
purchases = [('2006-01-05',123456,'example@rasa.com','blue', 9, 'shipped'),
             ('2021-01-05',123457,'me@rasa.com','black', 10, 'order pending'),
             ('2021-01-05',123458,'me@gmail.com','gray', 11, 'delivered'),
            ]

# add data
c.executemany('INSERT INTO orders VALUES (?,?,?,?,?,?)', purchases)

# AVAILABLE INVENTORY
# Create table
c.execute('''CREATE TABLE menu
             (name, price)''')

# data to be added
menu = [('Пицца Маргарита', 550),
        ('Спагетти Болоньезе', 450),
        ('Салат Цезарь', 450)
        ]

# add data
c.executemany('INSERT INTO menu VALUES (?,?)', menu)


# Save (commit) the changes
conn.commit()

# end connection
conn.close()