from fastapi import FastAPI, HTTPException
import services, models

app = FastAPI()

@app.post("/request_orders")
def request_orders(request: models.RequestOrders):
    orders = services.request_dborders(request)
    return orders

@app.post("/add_order")
def add_order(request: models.NewOrder):
    services.new_order_val(request)
    status = services.add_new_order(request)
    if status["status_code"] == 200:
        services.record_log(request.order_number, "created", request.sales_rep)
        services.create_track(request.order_number)
        return status
    else:
        raise HTTPException (
            status_code=400,
            detail="Something went wrong!"
        )

@app.post("/new_staff")
def new_staff(request: models.NewStaff):
    services.new_staff_val(request)
    services.adding_new_staff(request)
    return {
        "detail": "Staff SUCCESSFULLY added!"
    }

@app.get("/yard_staff")
def yard_staff():
    y_staff = services.request_yard_staff()
    return y_staff

@app.post("/update_track")
def update_track(request: models.UpdateTrack):
    services.update_track(request)
    services.record_log(request.order_number, "assign", 1, request.assign_to)

@app.post("/order_info")
def order_info(request: models.RequestInfo):
    data = services.order_info(request.order_number)
    return data