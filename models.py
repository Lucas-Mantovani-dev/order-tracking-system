from pydantic import BaseModel

class NewOrder(BaseModel):
    order_number: int
    sales_rep: int
    cust_name: str
    suburb: str
    delivery_date: str

class NewStaff(BaseModel):
    fname: str
    lname: str
    department: str
    hash_pw: str

class UpdateTrack(BaseModel):
    order_number: int
    assign_to: str

class RequestInfo(BaseModel):
    order_number: int

class RequestOrders(BaseModel):
    filter_date: str
    filter_search: str

class LoginAccess(BaseModel):
    user_id: int
    user_pw: str