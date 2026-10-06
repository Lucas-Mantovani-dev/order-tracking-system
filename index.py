from nicegui import ui
import httpx
from datetime import date, timedelta

# HOME PAGE
@ui.page("/")
def login_page():
    def access_login():
        response = httpx.post(
            "http://127.0.0.1:8000/access_login",
            json= {
                "user_id": int(user_id.value),
                "user_pw": user_pw.value
            }
        )
        data = response.json()

        if response.status_code != 200:
            ui.notification(f"{response.status_code} - {data["detail"]}", color="red", timeout=2)
        else:
            ui.notification(f"Welcome in {response.text}", color="green", timeout=2)

    ui.query(".nicegui-content").classes("p-0 h-screen w-full items-center justify-center")
    with ui.card().props("flat"):
        with ui.column().classes("items-center justify-center"):
            ui.image("assets/hardwarengeneral_logo.jpg").style("border-radius: 30px;").classes("w-40 mb-10")
            user_id = ui.input("Employee ID:").props("outlined rounded").classes("h-15 w-50 text-xl")
            user_pw = ui.input("Password:", password=True, password_toggle_button=True).props("outlined rounded").classes("h-15 w-50 text-xl")
            ui.button("Login", color="#eb1c24", on_click=access_login).classes("w-50 text-xl text-white mt-10").style("border-radius: 30px;")

# CONTENT PAGE
@ui.page("/orders")
def orders_page():

    # GET ALL ORDERS TO DISPLAY ON THE SCREEN
    def request_orders():
        response = httpx.post(
            "http://127.0.0.1:8000/request_orders",
            json= {
                "filter_date": filter_choice.text,
                "filter_search": filter_search.value
            }
        )
        data = response.json()
        return data

    # ADD ORDER FUNCTION/BUTTON
    def add_order():

        # REQUEST TO THE ADD_ORDER ENDPOINT
        def request_create_order():
            response = httpx.post(
                "http://127.0.0.1:8000/add_order",
                json={
                    "order_number": order_number.value,
                    "sales_rep": sales_rep.value,
                    "cust_name": cust_name.value.strip().upper(),
                    "suburb": suburb.value.strip().capitalize(),
                    "delivery_date": delivery_date.value
                }
            )

            data = response.json()

            # NOTIFY IF THE REQUEST WORKED PROPERLY
            if response.status_code == 422:
                ui.notification("Please fill the fields correctly!", color="red", timeout=2.0)
            elif response.status_code != 200:
                ui.notification(data["detail"], color="red", timeout=1.0)
            else:
                ui.notification(data["detail"], color="green", timeout=1.0, on_dismiss=dialog.close)
                content_row.refresh()

        tomorrow = (date.today() + timedelta(days=1)).isoformat()

        # DIALOG POPUP
        with ui.dialog() as dialog, ui.card().classes("w-300 h-220").style("max-width: none;"):

            # CLOSE DIALOG BUTTON
            ui.button(icon="cancel", on_click=dialog.close, color=None).props("flat round dense").style("color: #eb1c24; font-size: 20px;").classes("self-end")

            ui.label("Create Order").classes("text-bold self-center text-white mb-15").style("font-size: 30px; background-color: #eb1c24; border-radius: 30px; padding: 15px;")

            # ROW WITH THE ORDER CREATION FORM
            with ui.row().classes("w-full items-center justify-center gap-15"):
                with ui.column().classes("gap-7"):
                    order_number = ui.input("Order Number:").props("outlined rounded").classes("h-15 w-100 text-xl")
                    sales_rep = ui.input("Sales Rep.:").props("outlined rounded").classes("h-15 w-100 text-xl")
                    cust_name = ui.input("Customer Name:").props("outlined rounded").classes("h-15 w-100 text-xl")
                    suburb = ui.input("Suburb:").props("outlined rounded").classes("h-15 w-100 text-xl")
                with ui.column().classes(""):
                    delivery_date = ui.input("Date:", value=tomorrow).props("outlined rounded disable").classes("h-15 w-100 text-xl")
                    ui.date(value=tomorrow, on_change=lambda e: delivery_date.set_value(e.value)).classes("w-100")
            ui.button("Create Order", color="#eb1c24", on_click=request_create_order).classes("self-center text-2xl text-white mt-15").style("border-radius: 30px;")
        dialog.open()

    # ADD STAFF REQUEST
    def request_add_staff():
        import bcrypt
        attp_pw = user_pw.value.encode('utf-8')
        salt = bcrypt.gensalt()
        hash_pw = bcrypt.hashpw(attp_pw, salt)
        print(attp_pw, hash_pw)

        response = httpx.post(
            "http://127.0.0.1:8000/new_staff",
            json={
                "fname": fname.value.strip().capitalize(),
                "lname": lname.value.strip().capitalize(),
                "department": dpt_dropdown.text,
                "hash_pw": hash_pw.decode()
            }
        )
        data = response.json()

        if response.status_code != 200:
            ui.notification(data["detail"], color="red", timeout=1.0)
        else:
            ui.notification(data["detail"], color="green", timeout=1.0, on_dismiss=staff_dialog.close)

    # ADD STAFF DIALOG
    with ui.dialog() as staff_dialog, ui.card().classes("w-300 h-220").style("max-width: none;"):
        ui.button(icon="cancel", on_click=staff_dialog.close, color=None).props("flat round dense").style("color: #eb1c24; font-size: 20px;").classes("self-end")
        ui.label("Add Staff").classes("text-bold self-center text-white mb-15").style("font-size: 30px; background-color: #eb1c24; border-radius: 30px; padding: 15px;")

        # ADD STAFF FORM
        with ui.row().classes("w-full justify-center items-center"):
            fname = ui.input("First Name:").props("outlined rounded").classes("h-15 w-100 text-xl")
            lname = ui.input("Last Name:").props("outlined rounded").classes("h-15 w-100 text-xl")
            user_pw = ui.input("Password:", password=True, password_toggle_button=True).props("outlined rounded").classes("h-15 w-100 text-xl")
        with ui.dropdown_button("Department", auto_close=True, color="#eb1c24").classes(
            "self-center w-70 h-15 text-white text-xl items-center justify-center"
        ).style("border-radius: 30px;") as dpt_dropdown:
            ui.item("Yard", on_click=lambda: dpt_dropdown.set_text("Yard"))
            ui.item("Sales", on_click=lambda: dpt_dropdown.set_text("Sales"))
            
        ui.button("Add Staff", color="#eb1c24", on_click=request_add_staff).classes("self-center text-2xl text-white mt-15").style("border-radius: 30px;")

             
    # FUNTION ONCE AN ORDER IS CLICKED
    def order_info(order):

        # REQUEST TO UPDATE THE ORDER ASSIGNMENT
        def update_track(selected_staff):
            upd_response = httpx.post(
                "http://127.0.0.1:8000/update_track",
                json= {
                    "order_number": order[0],
                    "assign_to": selected_staff
                }
            )

            content_row.refresh()

        # DROPDOWN BUTTON WITH YARD STAFF
        @ui.refreshable
        def dropdown_button():

            response = httpx.get("http://127.0.0.1:8000/yard_staff")
            data = response.json()

            with ui.dropdown_button(text=order[4], auto_close=True).props("flat").classes("w-70 h-13 text-xl text-black").style("border-radius: 30px; border: 2px solid #eb1c24") as dpd_btn:
                ui.item("Not assigned", on_click=lambda:(update_track("Not assigned"), dpd_btn.set_text("Not assigned")))
                for staff in data:
                    ui.item(text=staff[0], on_click=lambda selected_staff = staff[0]: (update_track(selected_staff), dpd_btn.set_text(selected_staff)))

        # ORDER DATA DIALOG
        with ui.dialog() as dialog, ui.card().classes("w-180 h-210").style("max-width: none;"):
            ui.button(icon="cancel", on_click=dialog.close, color=None).props("flat round dense").style("color: #eb1c24; font-size: 20px;").classes("self-end")

            # COLUMN CONTAINING ORDER DATA
            with ui.column().classes("w-full h-full items-center justify-center").style("font-size: 25px;"):
                with ui.row().classes("w-[80%] justify-between"):
                    ui.label(order[1]).classes("text-bold").style("font-size: 30px;") # CUSTOMER NAME
                    ui.label(order[0]) # ORDER NUMBER
                with ui.row().classes("w-[80%] justify-between mb-7"):
                    ui.label(order[2]) # SUBURB
                    ui.label(f"Delivery date: {order[3]}") # DELIVERY DATE

                # TABS FOR ORDER MANAGEMENT OR INFO
                with ui.tabs().classes("w-[80%] mt-5") as tabs:
                    manag = ui.tab("Management")
                    info = ui.tab("Info")
                with ui.tab_panels(tabs, value=manag).classes("w-[80%] h-80 items-center justify-center mb-10"):
                    with ui.tab_panel(manag).classes("w-full items-center pt-10"):
                        dropdown_button()
                    with ui.tab_panel(info).classes("w-full items-center"):
                        response = httpx.post(
                            "http://127.0.0.1:8000/order_info",
                            json= {
                                "order_number": order[0]
                            }
                        )
                        data = response.json()
                        ui.label(f"Sales rep: {data[0][3]}").style("font-size: 20px;")

                        # ORDER INFO LOG INTO A TABLE
                        info_columns = [
                            {'name': 'action_perf', 'label': 'Action:', 'field': 'action_perf'},
                            {'name': 'perf_by', 'label': 'Done by:', 'field': 'perf_by'},
                            {'name': 'perf_to', 'label': 'Assign to:', 'field': 'perf_to'},
                            {'name': 'act_timestamp', 'label': 'Date/Time:', 'field': 'act_timestamp'},
                        ]
                        info_rows = []

                        for info in data:

                            # FIXING DATE YYYY-MM-DD -> DD/MM/YYYY
                            old_date = info[5][0:10]
                            from datetime import datetime
                            date_obj = datetime.strptime(old_date, "%Y-%m-%d")
                            new_date = date_obj.strftime("%d/%m/%Y")

                            new_row = {
                                'action_perf': info[2],
                                'perf_by': info[3],
                                'perf_to': info[4],
                                'act_timestamp': f"{new_date} — {info[5][10::]}"
                            }
                            info_rows.append(new_row)

                        ui.table(columns=info_columns, rows=info_rows).classes("w-full text-bold")

                ui.button("Mark order as completed", on_click=lambda: update_track("Completed"), color="#00bf63").classes("w-50 h-22 text-white text-bold mb-10").style("border-radius: 25px; font-size: 20px;")
            
        dialog.open()

    # MAIN CONTENT AS A ROW
    @ui.refreshable
    def content_row():
        with ui.row().classes("w-full justify-center items-center gap-7"):
            data = request_orders()
            if not data:
                ui.label("No orders to be shown...").style(
                    "font-size: 30px; background-color: #eb1c24; border-radius: 30px; padding: 15px; color: white;"
                )
            else:
                for order in data:

                    # FIXING DATE YYYY-MM-DD -> DD/MM/YYYY
                    from datetime import datetime
                    input_date = order[3]
                    date_obj = datetime.strptime(input_date, "%Y-%m-%d")
                    output_date = date_obj.strftime("%d/%m/%Y")
                    order[3] = output_date

                    # VISUALY ORDER STATUS
                    if order[4] == "Not assigned":
                        card_status = "#ededed"
                    elif order[4] == "Completed":
                        card_status = "#a4e1a9"
                    else:
                        card_status = "#ffea95"
                    if date.fromisoformat(input_date) < date.today():
                        if order[4] == "Completed":
                            card_status = "#a4e1a9"
                        else:
                            card_status = "#f49ea1"

                    # ORDER CARDS
                    with ui.card().classes(f"w-100 text-bold hover:bg-sky-100 shadow hover:shadow-lg transition-all duration-300").style(
                        f"""background-color: {card_status};
                        border-radius: 20px;
                        border: 2px solid #eb1c24;
                        cursor: pointer;"""
                    ).on("click", lambda selected_order = order: order_info(selected_order)):
                        with ui.column().classes("w-full items-center"):
                            ui.label(order[1]).style("font-size: 20px;")
                            ui.label(order[2]).classes("text-lg")
                            ui.label(order[0]).classes("text-lg")
                        with ui.row().classes("w-full justify-between"):
                            ui.label(order[4]).classes("text-lg")
                            ui.label(order[3]).classes("text-lg")

    def filter_apply():
        main_fbtn.close()
        content_row.refresh()

    def reset_filter():
        filter_search.set_value("")
        filter_apply()

    ui.query(".nicegui-content").classes("p-0")

    # FULL PAGE IN A COLUMN
    with ui.column().classes("w-full items-center justify-center gap-0"):

        # CARD FOR THE HEADER
        with ui.card().props("flat").classes("w-full flex-row items-center justify-end gap-30 b-0").style("background-color: #eb1c24; border-radius: 0px;"):

            # MENU BUTTON
            with ui.button(icon="menu", color="white").classes("mr-auto").props("flat round dense").style("color: #eb1c24; font-size: 25px;"):
                with ui.menu() as menu:
                    with ui.menu_item(on_click=staff_dialog.open).classes("gap-2 items-center justify-center p-2 text-bold"):
                        ui.icon("person").classes("text-xl")
                        ui.label("Add staff")

            # HEADER TITLE
            ui.label("Yard Tracker").classes("text-white text-bold").style("font-size: 40px;")

            # HEADER LOGO
            ui.image("assets/hardwarengeneral_logo.jpg").classes("w-25 mr-30")

        # CARD FOR THE CONTENT AREA
        with ui.card().props("flat").classes("w-[95%]").style("border-radius: 0px;"):

            # ROW  FOR THE NAV BUTTONS
            with ui.row().classes("w-full justify-end items-center"):
                with ui.dropdown_button("Filter", icon="filter_list", color="#eb1c24").props("rounded").classes("w-70 text-white").style(
                    """font-size: 20px;"""
                ) as main_fbtn:
                    with ui.column().classes("w-full items-center justify-center gap-7 p-5"):
                        with ui.dropdown_button("Today", auto_close=True).props("rounded flat").classes("w-50 text-lg text-black").style("border: 2px solid #eb1c24") as filter_choice:
                            ui.item("Today", on_click=lambda selected_item: filter_choice.set_text("Today"))
                            ui.item("Tomorrow", on_click=lambda selected_item: filter_choice.set_text("Tomorrow"))
                            ui.item("Newest", on_click=lambda selected_item: filter_choice.set_text("Newest"))
                            ui.item("Oldest", on_click=lambda selected_item: filter_choice.set_text("Oldest"))

                        filter_search = ui.input("Search").props("outlined rounded").classes("h-15 w-full text-xl")

                        with ui.row():
                            ui.button("Apply", on_click=filter_apply, color="#eb1c24").props("rounded").classes("text-white").style("font-size: 15px;")
                            ui.button("Reset", on_click=reset_filter).props("rounded flat").classes("text-black").style("font-size: 15px; border: solid 2px black;")

                ui.button(icon="add_circle", color=None, on_click=add_order).props("flat round dense").style("color: #eb1c24; font-size: 30px;")

            # ROW FOR THE ORDERS
            content_row()

ui.run(
    title="Yard Tracker",
    favicon="assets/hardwarengeneral_logo.jpg"
)
