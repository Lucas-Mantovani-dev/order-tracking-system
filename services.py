import sqlite3
from fastapi import HTTPException


def record_log(order_number: int, action_perf: str, perf_by: int, perf_to=None):
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect("system.db")
    cursor = conn.cursor()

    if perf_to:
        cursor.execute(
            """INSERT INTO orders_log (order_number, action_perf, perf_by, perf_to, act_timestamp)
            VALUES (?, ?, ?, ?, ?)""", (order_number, action_perf, perf_by, perf_to, timestamp)
        )
    else:
        cursor.execute(
            """INSERT INTO orders_log (order_number, action_perf, perf_by, perf_to, act_timestamp)
            VALUES (?, ?, ?, ?, ?)""", (order_number, action_perf, perf_by, "Not assigned", timestamp)
        )
    conn.commit()

def request_dborders():
    conn = sqlite3.connect("system.db")
    cursor = conn.cursor()

    cursor.execute(
        """SELECT
        o.order_number,
        o.cust_name,
        o.suburb,
        o.delivery_date,
        oto.assign_to
        FROM orders AS o
        INNER JOIN track_orders AS oto
        ON o.order_number = oto.order_number"""
    )

    orders_received = cursor.fetchall()

    return orders_received

def new_order_val(request):
    from datetime import date

    # ERROR IF ANY FIELD IS MISSING
    for attribute, value in vars(request).items():
        if not value:
            raise HTTPException (
                status_code=400,
                detail="Please fill the fields!"
            )

    # ERROR IF DATE PICKED IS IN THE PAST
    date_val = date.fromisoformat(request.delivery_date)
    today = date.today()
    if date_val < today:
        raise HTTPException (
            status_code=400,
            detail="Please select a valid delivery date!"
        )

    # ERROR IF SALES REP DOESNT EXISTS
    conn = sqlite3.connect("system.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sales_employees WHERE sales_rep = ?", (request.sales_rep,))
    rep_from_db = cursor.fetchone()

    if not rep_from_db:
        raise HTTPException (
            status_code=404,
            detail="Sales rep number not valid!"
        )

    # ERROR IF ORDER NUMBER ALREADY EXISTS
    cursor.execute("SELECT * FROM orders WHERE order_number = ?", (request.order_number,))
    order_from_db = cursor.fetchone()

    if order_from_db:
        raise HTTPException (
            status_code=400,
            detail="Order number already exists!"
        )

def add_new_order(request):
    conn = sqlite3.connect("system.db")
    cursor = conn.cursor()

    cursor.execute(
        """INSERT INTO orders (order_number, sales_rep, cust_name, suburb, delivery_date)
        VALUES (?, ?, ?, ?, ?)""", (request.order_number, request.sales_rep, request.cust_name, request.suburb, request.delivery_date)
    )
    conn.commit()

    return {
        "status_code": 200,
        "detail": "Order SUCCESSFULLY created!"
    }

def create_track(order_number):
    conn = sqlite3.connect("system.db")
    cursor = conn.cursor()

    cursor.execute(
        """INSERT INTO track_orders (order_number)
        VALUES (?)""", (order_number,)
    )
    conn.commit()

def new_staff_val(request):
    for attribute, value in vars(request).items():
        if not value:
            raise HTTPException (
                status_code=400,
                detail="Please fill the fields!"
            )

    if request.department == "Department":
        raise HTTPException (
            status_code=400,
            detail="Please pick a department"
        )

def adding_new_staff(request):
    conn = sqlite3.connect("system.db")
    cursor = conn.cursor()

    if request.department == "Yard":
        cursor.execute(
            """INSERT INTO yard_staff (fname, lname)
            VALUES (?, ?)""", (request.fname, request.lname)
        )

    elif request.department == "Sales":
        cursor.execute(
            """INSERT INTO sales_employees (fname, lname)
            VALUES (?, ?)""", (request.fname, request.lname)
        )

    else:
        raise HTTPException (
            status_code=404,
            detail="Department invalid!"
        )

    conn.commit()

def request_yard_staff():
    conn = sqlite3.connect("system.db")
    cursor = conn.cursor()

    cursor.execute("SELECT fname FROM yard_staff")

    y_staff = cursor.fetchall()

    return y_staff

def update_track(request):
    conn = sqlite3.connect("system.db")
    cursor = conn.cursor()

    cursor.execute(
        """UPDATE track_orders
        SET assign_to = ?
        WHERE order_number = ?""", (request.assign_to, request.order_number)
    )

    conn.commit()

def order_info(order_number):
    conn = sqlite3.connect("system.db")
    cursor = conn.cursor()

    cursor.execute(
        """SELECT * FROM orders_log
        WHERE order_number = ?""", (order_number,)
    )

    data_tuple = cursor.fetchall()
    data = []
    for info in data_tuple:
        ct = list(info)
        data.append(ct)
    

    for info in data:
        cursor.execute("SELECT * FROM sales_employees WHERE sales_rep = ?", (info[3],))
        sales_info = cursor.fetchall()
        sales_info = sales_info[0]


        info[3] = f"{sales_info[1]} {sales_info[2]}"

    return data