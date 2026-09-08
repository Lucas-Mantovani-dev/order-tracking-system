import sqlite3
from nicegui import ui
from datetime import datetime, date, timedelta
conn = sqlite3.connect("system.db")
cursor = conn.cursor()

request = "Tomorrow"

if request == "Today" or request == "Tomorrow":
    if request == "Today":
        date_val = datetime.now()
        date_val = date_val.strftime("%Y-%m-%d")
    elif request == "Tomorrow":
        date_val = (date.today() + timedelta(days=1)).isoformat()

    cursor.execute(
    """SELECT
    o.order_number,
    o.cust_name,
    o.suburb,
    o.delivery_date,
    oto.assign_to
    FROM orders AS o
    INNER JOIN track_orders AS oto
    ON o.order_number = oto.order_number
    WHERE o.delivery_date = ?""", (date_val,)
    )

    data = cursor.fetchall()

    print(data)
