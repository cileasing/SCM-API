from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp

class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id

users = [
    User(1, 'testuser', 'testpassword')
]

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}

def authenticate(username, password):
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)

app=Flask(__name__)
app.config['SECRET_KEY'] = 'EeK@PWGjQcmk4L'
jwt = JWT(app, authenticate, identity)

#success response
_success = dict(status='success', data='...')

#error response
_error = dict(status='error', message='...', code='...')

@app.route('/')
def home():
    return ({})

@app.route('/protected')
@jwt_required()
def protected():
    return '%s' % current_identity

# create warehouse location
@app.route('/warehouses/<warehouseId>/locations', methods=['GET','POST'])
@jwt_required()
def warehouse_locations(warehouseId):
    if request.method == 'POST':
        req_data = request.get_json()
        print(req_data)
        data = [dict(warehouseId=3, name='Mechanical', availableToSell=True, createdAt='2020-18-12 12:00:00',
                     updatedAt='2020-18-12 12:00:00')]
        _success['data'] = data
        return (_success)

    # get warehouse locations
    data = [dict(warehouseId=3, name='Mechanical', availableToSell=True, createdAt='2020-18-12 12:00:00',
                 updatedAt='2020-18-12 12:00:00')]
    _success['data'] = data
    return (_success)

# update warehouse location
@app.route('/warehouses/<warehouseId>/locations/<locationId>', methods=['GET','PUT', 'DELETE'])
@jwt_required()
def warehouse_location(warehouseId, locationId):
    if request.method == 'PUT':
        req_data = request.get_json()
        print(req_data)
        data = [dict(warehouseId=3, name='Machine Tools', availableToSell=True, createdAt='2020-18-12 12:00:00',
                     updatedAt='2020-18-12 12:00:00')]
        _success['data'] = data
        return (_success)

    if request.method == 'DELETE':
        _success['data'] = "ok"
        return (_success)

    #
    data = [dict(warehouseId=3, name='Mechanical', availableToSell=True, createdAt='2020-18-12 12:00:00',
                 updatedAt='2020-18-12 12:00:00')]
    _success['data'] = data
    return (_success)

#status
@app.route('/statuses/<statusId>', methods=['GET'])
@jwt_required()
def statuses(statusId):
    data = [dict(id=3, code='picked', name='Picked')]
    _success['data'] = data
    return (_success)

#product stock
@app.route('/stocks/warehouses/<warehouseId>/products/<sku>', methods=['GET'])
@jwt_required()
def stock_products(warehouseId, sku):
    data = [dict(sku=3563, qty=4, locations=[
        dict(locationId=34, name='Mechanical', qty=2, availableToSell=True),
        dict(locationId=35, name='Tools', qty=2, availableToSell=True)
    ], createdAt='2020-18-12 12:00:00', updatedAt='2020-18-12 12:00:00')]
    _success['data'] = data
    return (_success)

# stocks
@app.route('/stocks', methods=['GET'])
@jwt_required()
def stocks():
    data = [dict(sku=3563, qty=4, locations=[
        dict(locationId=34, name='Mechanical', qty=2, availableToSell=True),
        dict(locationId=35, name='Tools', qty=2, availableToSell=True)
    ], createdAt='2020-18-12 12:00:00', updatedAt='2020-18-12 12:00:00')]
    _success['data'] = data
    return (_success)

# goods receipt
@app.route('/warehouses/<warehouseId>/goodsreceipt', methods=['POST'])
@jwt_required()
def goods_receipt(warehouseId):
    if request.method == 'POST':
        req_data = request.get_json()
        print(req_data)
        data = [dict(receiptNo='G674663774', poNumber='BT90998983', createdBy=45, remark='', warehouseId=warehouseId, status='received', items=[{"sku": 546, "price": 657.00, "qty": 5, "total": 7877.00, "locationId": 4564}], createdAt='2020-18-12 12:00:00',
                     updatedAt='2020-18-12 12:00:00')]
        _success['data'] = data
        return (_success)

# get goods receipt
@app.route('/goodsreceipt', methods=['GET'])
@jwt_required()
def gr():
    data = [dict(receiptNo='G674663774', poNumber='BT90998983', createdBy=45, putawayBy=4, remark='', warehouseId=3,
                 status='received',
                 items=[{"sku": 546, "price": 657.00, "qty": 5, "total": 7877.00, "locationId": 4564}],
                 createdAt='2020-18-12 12:00:00',
                 updatedAt='2020-18-12 12:00:00')]
    _success['data'] = data
    return (_success)

# get goods receipt details
@app.route('/goodsreceipt/<receiptNo>', methods=['GET'])
@jwt_required()
def goodsreceipt(receiptNo):
    data = [dict(receiptNo=receiptNo, poNumber='BT90998983', createdBy=45, putawayBy=4, remark='', warehouseId=3,
                 status='received',
                 items=[{"sku": 546, "price": 657.00, "qty": 5, "total": 7877.00, "locationId": 4564}],
                 createdAt='2020-18-12 12:00:00',
                 updatedAt='2020-18-12 12:00:00')]
    _success['data'] = data
    return (_success)


# put away GRN items
@app.route('/warehouses/<warehouseId>/goodsreceipt/<receiptNo>/putaway', methods=['PUT'])
@jwt_required()
def put_away(warehouseId, receiptNo):
    if request.method == 'PUT':
        data = [dict(receiptNo=receiptNo, poNumber='BT90998983', createdBy=45, putawayBy=4, remark='', warehouseId=3,
                     status='received',
                     items=[{"sku": 546, "price": 657.00, "qty": 5, "total": 7877.00, "locationId": 4564}],
                     createdAt='2020-18-12 12:00:00',
                     updatedAt='2020-18-12 12:00:00')]
        _success['data'] = data
        _success['status'] = 'success'
        return (_success)

# create stock count
@app.route('/warehouses/<warehouseId>/stockcounts', methods=['POST'])
@jwt_required()
def create_stock_counts(warehouseId):
    if request.method == 'POST':
        data = [dict(sku=546,
                     qty=5,
                     warehouseId=4563,
                     locationId=3456,
                     userId=34,
                     remark='if any',
                     createdAt='2020-18-12 12:00:00',
                     updatedAt='2020-18-12 12:00:00')]
        _success['data'] = data
        _success['status'] = 'success'
        return (_success)

# get stock counts
@app.route('/stockcounts', methods=['GET'])
@jwt_required()
def stock_counts():
    data = [dict(sku=546,
                 qty=5,
                 warehouseId=4563,
                 locationId=3456,
                 userId=34,
                 remark='if any',
                 createdAt='2020-18-12 12:00:00',
                 updatedAt='2020-18-12 12:00:00')]
    _success['data'] = data
    _success['status'] = 'success'
    return (_success)

'''
    Fill these in and add authentication!
'''
# create/update goods released
@app.route('/warehouses/<warehouseId>/goodsreleased', methods=['POST', 'PUT'])
def goods_released(warehouseId):
    if request.method == 'POST':
        data = dict(ticketNo='PT8499584',
                     requestNumber='BT90998983',
                     createdBy=45,
                     remark='',
                     warehouseId=3,
                     status='received',
                     items=[dict(sku=546, qty=5, locationId=4564)],
                     createdAt='2020-18-12 12:00:00',
                     updatedAt='2020-18-12 12:00:00')
        _success['data'] = data
        _success['status'] = 'success'
        return (_success)

    if request.method == 'PUT':
        data = dict(ticketNo='PT8499584',
                     requestNumber='BT90998983',
                     createdBy=45,
                     remark='',
                     warehouseId=3,
                     status='received',
                     items=[dict(sku=546, qty=5, locationId=4564)],
                     createdAt='2020-18-12 12:00:00',
                     updatedAt='2020-18-12 12:00:00')
        _success['data'] = data
        _success['status'] = 'success'
        return (_success)

# get goods released details
@app.route('/goodsreleased/<id>', methods=['GET'])
def get_gr_details(id):
    data = dict(ticketNo='PT8499584',
                 requestNumber='BT90998983',
                 createdBy=45,
                 remark='',
                 warehouseId=3,
                 status='received',
                 items=[dict(sku=546, qty=5, locationId=4564)],
                 createdAt='2020-18-12 12:00:00',
                 updatedAt='2020-18-12 12:00:00')
    _success['data'] = data
    _success['status'] = 'success'
    return (_success)

# get good released list
@app.route('/goodsreleased', methods=['GET'])
def get_gr_list():
    data = [dict(ticketNo='PT8499584',
                 requestNumber='BT90998983',
                 createdBy=45,
                 remark='',
                 warehouseId=3,
                 status='received',
                 items=[dict(sku=546, qty=5, locationId=4564)],
                 createdAt='2020-18-12 12:00:00',
                 updatedAt='2020-18-12 12:00:00')]
    _success['data'] = data
    _success['pagination'] = dict(offset=0, limit=20, total=100)
    _success['status'] = 'success'
    return (_success)

# create waybill
@app.route('/warehouses/<warehouseId>/waybills', methods=['POST'])
def create_waybill(warehouseId):
    if request.method == 'POST':
        data = dict(userId=45,
                    ticketNumber='PT8499584',
                    requestNumber='BT90998983',
                    receiverName='John Doe',
                    receiverSignature='<Base64>',
                    warehouseId=3,
                    items=[dict(sku=546, qty=5)],
                    createdAt='2020-18-12 12:00:00',
                    updatedAt='2020-18-12 12:00:00')
        _success['data'] = data
        _success['status'] = 'success'
        return (_success)

# update waybill
@app.route('/warehouses/<warehouseId>/waybills/<id>', methods=['PUT'])
def update_waybill(warehouseId, id):
    if request.method == 'PUT':
        data = dict(userId=45,
                    ticketNumber='PT8499584',
                    requestNumber='BT90998983',
                    receiverName='John Doe',
                    receiverSignature='<Base64>',
                    warehouseId=3,
                    items=[dict(sku=546, qty=5)],
                    createdAt='2020-18-12 12:00:00',
                    updatedAt='2020-18-12 12:00:00')
        _success['data'] = data
        _success['status'] = 'success'
        return (_success)

# get waybill details
@app.route('/waybills/<id>', methods=['PUT'])
def get_waybill(id):
    if request.method == 'PUT':
        data = dict(userId=45,
                    ticketNumber='PT8499584',
                    requestNumber='BT90998983',
                    receiverName='John Doe',
                    receiverSignature='<Base64>',
                    warehouseId=3,
                    items=[dict(sku=546, qty=5)],
                    createdAt='2020-18-12 12:00:00',
                    updatedAt='2020-18-12 12:00:00')
        _success['data'] = data
        _success['status'] = 'success'
        return (_success)

# get waybills
@app.route('/waybills', methods=['GET'])
def get_waybills():
    data = dict(userId=45,
                ticketNumber='PT8499584',
                requestNumber='BT90998983',
                receiverName='John Doe',
                receiverSignature='<Base64>',
                warehouseId=3,
                items=[dict(sku=546, qty=5)],
                createdAt='2020-18-12 12:00:00',
                updatedAt='2020-18-12 12:00:00')
    _success['data'] = data
    _success['_pagination'] = dict(offset=0, limit=20, total=100)
    _success['status'] = 'success'
    return (_success)

# create stock transfer
@app.route('/stocktransfers', methods=['POST'])
def create_stock_transfer():
    if request.method == 'POST':
        data = dict(userId=45,
                    requestNumber='BT90998983',
                    fromWarehouseId=3,
                    fromLocationId=35,
                    type='intra',
                    assignToId=46,
                    items=[dict(sku=546, qty=5, toWarehouseId=4, toLocationId=35)],
                    createdAt='2020-18-12 12:00:00',
                    updatedAt='2020-18-12 12:00:00')
        _success['data'] = data
        _success['status'] = 'success'
        return (_success)

# update/get stock transfer details
@app.route('/stocktransfers/<id>', methods=['PUT', 'GET'])
def stock_transfers():
    if request.method == 'PUT':
        data = dict(userId=45,
                    requestNumber='BT90998983',
                    fromWarehouseId=3,
                    fromLocationId=35,
                    type='intra',
                    assignToId=46,
                    items=[dict(sku=546, qty=5, toWarehouseId=4, toLocationId=35)],
                    createdAt='2020-18-12 12:00:00',
                    updatedAt='2020-18-12 12:00:00')
        _success['data'] = data
        _success['status'] = 'success'
        return (_success)

    data = dict(userId=45,
                requestNumber='BT90998983',
                fromWarehouseId=3,
                fromLocationId=35,
                type='intra',
                assignToId=46,
                items=[dict(sku=546, qty=5, toWarehouseId=4, toLocationId=35)],
                createdAt='2020-18-12 12:00:00',
                updatedAt='2020-18-12 12:00:00')
    _success['data'] = data
    _success['status'] = 'success'
    return (_success)

# get stock transfers
@app.route('/stocktransfers', methods=['GET'])
def get_stock_transfers():
    data = [dict(userId=45,
                requestNumber='BT90998983',
                fromWarehouseId=3,
                fromLocationId=35,
                type='intra',
                assignToId=46,
                items=[dict(sku=546, qty=5, toWarehouseId=4, toLocationId=35)],
                createdAt='2020-18-12 12:00:00',
                updatedAt='2020-18-12 12:00:00')]
    _success['data'] = data
    _success['_pagination'] = dict(offset=0, limit=20, total=100)
    _success['status'] = 'success'
    return (_success)

