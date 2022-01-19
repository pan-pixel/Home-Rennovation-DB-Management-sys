import mysql.connector
import datetime
# Put your mysql password here before running the program
mysqlPass = "sql123"

db = mysql.connector.connect(host='localhost',user='root',passwd=mysqlPass)
mycursor = db.cursor()
mycursor.execute("create database if not exists Reno")
db = mysql.connector.connect(host='localhost',user='root',passwd=mysqlPass,database='Reno')
mycursor = db.cursor()
mycursor.execute("CREATE TABLE if not exists Paint(type varchar(50), quantity int,price decimal(7,2))")
mycursor.execute("CREATE TABLE if not exists Flooring(type varchar(50),price decimal(7,2))")
mycursor.execute("CREATE TABLE if not exists Purchase(cust_name varchar(50), cust_num bigint, address varchar(50),order_date DATE, appoitment_date DATE, total int)")

def check_type(ctype):
    mycursor.execute("Select type from Paint where type=%s",(ctype,))
    rec = mycursor.fetchall()
    for i in rec:
        a = i[0]
        return(a)

def check_ftype(ctype):
    mycursor.execute("Select type from flooring where type=%s",(ctype,))
    rec = mycursor.fetchall()
    for i in rec:
        a = i[0]
        return(a)



def create_paint():
    c_type = input("Enter the paint types you have:")
    quantity = int(input("Enter the quantity of buckets you have of that type:"))
    price = float(input("Enter the price per bucket"))
    query = "INSERT INTO Paint(type,quantity,price)values(%s,%s,%s)"
    values = (c_type,quantity,price)
    mycursor.execute(query,values)
    #mucursor.execute('INSERT INTO Paint(type,quantity,price)values(%s,%s,%s)',(c_type,quantity,price))
    db.commit()
    print("Record added succefully!!")

def update_paint():
    utype = input("Enter the type of paint to update its price per bucket:")
    prev = check_type(utype)
    if utype == prev:
        uprice = float(input("Enter the new price of the paint"))
        query = "UPDATE Paint set price=%s where type=%s"
        values = (uprice,utype)
        mycursor.execute(query,values)
        db.commit()
        print("Succefully updated")
        q = "SELECT * FROM Paint WHERE type=%s"
        mycursor.execute(q,(utype,))
        rec = mycursor.fetchall()
        print(rec[0])
    else:
        print('No such record exists')
        update_paint()

def update_paint_quantity():
    utype = input("Enter the type of paint to update its quantity:")
    prev = check_type(utype)
    if utype == prev:
        uquant = int(input("Enter the updated quantity of the paint:"))
        query = "UPDATE Paint set quantity=%s WHERE type=%s"
        values = (uquant,utype)
        mycursor.execute(query,values)
        db.commit()
        q = "SELECT * FROM Paint WHERE type=%s"
        mycursor.execute(q,(utype,))
        rec = mycursor.fetchall()
        print(rec[0])
    else:
        print('No such record exists')
        update_paint_quantity()


def create_floor():
    f_type = input("Enter the floor types you have:")
    price = float(input("Enter the price per sq foot"))
    query = "INSERT INTO flooring(type,price)values(%s,%s)"
    values = (f_type,price)
    mycursor.execute(query,values)
    db.commit()
    print("Record added succefully!!")


def update_floor():
    uf_type = input("Enter the floor type you want to update:")
    prev = check_ftype(uf_type)
    if uf_type == prev:
        uprice = float(input("Enter the new price of this floor per sq foot:"))
        query = "UPDATE Flooring set price=%s where type=%s"
        values = (uprice,uf_type)
        mycursor.execute(query,values)
        db.commit()
        print("Record updated succefully!!")
        q = "SELECT * FROM flooring WHERE type=%s"
        mycursor.execute(q,(uf_type,))
        rec = mycursor.fetchall()
        print(rec[0])
    else:
        print('No such record exists')
        update_floor()

def fetchdata_paint():
    mycursor.execute("SELECT * FROM Paint")
    rec = mycursor.fetchall()
    for x in rec:
        print(x)


def fetchdata_flooring():
    mycursor.execute("SELECT * FROM flooring")
    rec = mycursor.fetchall()
    for x in rec:
        print(x)

def product_availability(bil_quant,type):
        mycursor.execute("SELECT * FROM Paint WHERE type=%s",(type,))
        stav=mycursor.fetchall()
        for k in stav:
                l1=list(k)
                if l1[1]<bil_quant:
                    print("Product unavailable")
                    print("Kindly update the product!!!")
                    global avail_check
                    avail_check = True
                    stock_menu()

def stock_menu():
    choice = 'y'
    while choice == 'y':
        print("1. Type of paint entery")
        print("2. Type of flooring entery")
        print("3. Update paint-->")
        print("4. Update price of flooring")
        print("5. All types of paint in stock")
        print("6. All types of flooring in stock")
        print("7. Back")
        ch = int(input("Enter your choice:"))
        if ch == 1:
            create_paint()
        elif ch == 2:
            create_floor()
        elif ch == 3:
            while True:
                print("1. Update price")
                print("2. Update quantity")
                print("3. Back")
                c = int(input("Enter your choice:"))
                if c == 1:
                    update_paint()
                elif c == 2:
                    update_paint_quantity()
                elif c == 3:
                    break
                else:
                    print("Invalid option")
                    stock_menu()
        elif ch == 4:
            update_floor()
        elif ch == 5:
            fetchdata_paint()
        elif ch == 6:
            fetchdata_flooring()
        elif ch == 7:
            main_menu()
        else:
            print("Invalid Option")
            stock_menu()

def check_phoneno(cphoneno):
        spn=str(cphoneno)
        if len(spn)==10:
                pass
        else:
            print("Please check the correct no")
            billing()


def decrease(type,quantity):
        upqua="update Paint set quantity=quantity-%s where type=%s"
        up2=(quantity,type)
        mycursor.execute(upqua,up2)
        db.commit()


def billing():
    amnt = 0
    avail_check = False
    floor_check = False
    paint_check = False
    cust_name = input("Enter customer name:")
    contact = int(input("Enter phone number:"))
    check_phoneno(contact)
    address = input("Enter customer address:")
    ch = 'y'
    while ch == 'y' or ch == 'Y':
        print("RENOVATION OPTIONS-->")
        print("1. Paint")
        print("2. Flooring")
        print("3. Back")
        choice = int(input("Enter the option:"))
        if choice == 1:
            paint_check = True
            col_dic = {}
            print("Type of paints we have-->")
            mycursor.execute("SELECT * from Paint")
            rec = mycursor.fetchall()
            for i in rec:
                print("Type of paint\t\tPrice per bucket")
                print("*"*60)
                print(i[0],'\t\t',i[2])
                print("*"*60)
                print()
            paint_choice = input("Enter the type of paint you like:")
            prev_rec = check_type(paint_choice)
            if paint_choice!=prev_rec:
                print("Please enter only from available types!!")
                billing()
            else:
                mycursor.execute("SELECT price FROM Paint WHERE type=%s",(paint_choice,))
                rec = mycursor.fetchall()
                for i in rec:
                    priceof_p= i[0]
                quantity = int(input("Enter the number of buckets you want:"))
                product_availability(quantity,paint_choice)
                if avail_check == True:
                    break
                else:
                    i = 0
                    while i < quantity:
                        colour = input("Enter the color you want:")
                        colquan = int(input("Enter the number of buckets of this color:"))
                        if colquan > quantity:
                            print("Total number of buckets is less than the desired for this color\nWe suggest you increase the number of buckets first")
                            break
                            billing()
                        else:
                            i += colquan
                            col_dic[colour] = colquan
                    decrease(paint_choice,quantity)
                    amnt += priceof_p*quantity
        elif choice == 2:
            floor_check = True
            print("Types of flooring we have-->")
            mycursor.execute("SELECT * from flooring")
            rec = mycursor.fetchall()
            for i in rec:
                print("Type of flooring\t\tPrice per sq foot")
                print("*"*60)
                print(i[0],'\t\t',i[1])
                print("*"*60)
                print()
            floor_choice = input("Enter the type of flooring you like:")
            prev_rec = check_ftype(floor_choice)
            if floor_choice!=prev_rec:
                print("Please enter only from available types!!")
                billing()
            else:
                mycursor.execute("SELECT price FROM Flooring WHERE type=%s",(floor_choice,))
                rec = mycursor.fetchall()
                for i in rec:
                    priceof_f= i[0]
                area = int(input("Enter the area of your house in sq foot:"))
                amnt += priceof_f*area
        elif choice == 3:
                break
        else:
            print("Wrong input")
            billing()
        ch = input("Do you want to continue (y/n)?")

    now=datetime.datetime.now()
    odate=now.strftime("%y-%m-%d")
    appoitment_date = input("Enter appointment date for the renovation(yyyy-mm-dd):")
    query = "INSERT INTO Purchase(cust_name,cust_num,address,order_date,appoitment_date,total)values(%s,%s,%s,%s,%s,%s)"
    values = (cust_name,contact,address,odate,appoitment_date,amnt)
    mycursor.execute(query,values)
    db.commit()
    print("Done Billing!!")
    bil_choice = input("Do you want to print the bill (y/n)?")
    if bil_choice == 'Y' or bil_choice == 'y':
        mycursor.execute("SELECT * FROM Purchase where cust_name=%s",(cust_name,))
        record = mycursor.fetchall()
        for i in record:
            print("*"*50)
            print("Name-->",i[0])
            print("Mobile No.-->",i[1])
            print("Address-->",i[2])
            print("Oder date-->",i[3])
            print("appoitment_date-->",i[4])
            print("Total Amount-->",i[5])
            # res = str(not bool(col_dic))
            if paint_check == True:
                print("Type of paint-->",paint_choice)
                print("Color You opted for-->")
                for i in col_dic.keys():
                    print(i)
            if floor_check == True:
                print("Type of flooring-->",floor_choice)
            print("*"*50)
            print("Thank you")
            menu_ch = int(input("Enter 1 to open main menu and press 2 to continue billing:"))
            if menu_ch == 1:
                main_menu()
            else:
                billing()
    else:
        print("Thank You")
        menu_ch = int(input("Enter 1 to open main menu and press 2 to continue billing:"))
        if menu_ch == 1:
            main_menu()
        else:
            billing()


def main_menu():
    while True:
        print("Welcome to Universal Renovations!!")
        print("1. Stock")
        print("2. Billing")
        print("3. Orders Placed")
        print("4. Exit")
        ch = int(input("Enter the choice:"))
        if ch ==1:
            stock_menu()
        elif ch == 2:
            billing()
        elif ch == 3:
            mycursor.execute('SELECT * FROM Purchase')
            rec = mycursor.fetchall()
            for i in rec:
                print(i)
        elif ch == 4:
            quit()
            break

        else:
            print('Invalid Input!')

main_menu()
