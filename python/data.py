from datetime import datetime, timedelta

now = datetime.now()

# CellLocation: size - объём ячейки в см3
cells = [
    {"id": 1, "pickup_point_id": 1, "rack_number": 1, "shelf_number": 1,
        "cell_code": "A-1-1", "size": 1000, "is_occupied": True},
    {"id": 2, "pickup_point_id": 1, "rack_number": 1, "shelf_number": 2,
        "cell_code": "A-1-2", "size": 64000, "is_occupied": False},
    {"id": 3, "pickup_point_id": 1, "rack_number": 1, "shelf_number": 3,
        "cell_code": "A-1-3", "size": 8000, "is_occupied": False},
    {"id": 4, "pickup_point_id": 1, "rack_number": 2, "shelf_number": 1,
        "cell_code": "A-2-1", "size": 27000, "is_occupied": False},
    {"id": 5, "pickup_point_id": 1, "rack_number": 2, "shelf_number": 2,
        "cell_code": "A-2-2", "size": 8000, "is_occupied": True},
    {"id": 6, "pickup_point_id": 2, "rack_number": 1, "shelf_number": 1,
        "cell_code": "B-1-1", "size": 27000, "is_occupied": True},
]

# Product: dimensions - длина, ширина и высота в см
products = [
    {"id": 1, "title": "Наушники", "barcode": "4600000000011",
        "weight": 0.3, "dimensions": (20, 15, 10), "price": 3500},
    {"id": 2, "title": "Чайник", "barcode": "4600000000028",
        "weight": 1.2, "dimensions": (25, 25, 30), "price": 2400},
    {"id": 3, "title": "Книга", "barcode": "4600000000035",
        "weight": 0.5, "dimensions": (22, 15, 3), "price": 800},
]

# User: verification_code - код клиента для получения заказа
users = [
    {"id": 1, "role_id": 1, "full_name": "Иванов И.И.",
        "verification_code": "4821", "code_expires_at": now + timedelta(minutes=10)},
    {"id": 2, "role_id": 1, "full_name": "Петров П.П.",
        "verification_code": "1111", "code_expires_at": now - timedelta(minutes=10)},
    {"id": 3, "role_id": 2, "full_name": "Сидоров С.С.",
        "verification_code": None, "code_expires_at": None},
]

orders = [
    {"id": 1, "client_id": 1, "pickup_point_id": 1,
        "status": "Готов к выдаче", "total_price": 5900},
    {"id": 2, "client_id": 1, "pickup_point_id": 1,
        "status": "Готов к выдаче", "total_price": 800},
    {"id": 3, "client_id": 1, "pickup_point_id": 2,
        "status": "Готов к выдаче", "total_price": 2400},
]

order_items = [
    {"id": 1, "order_id": 1, "product_id": 1,
        "cell_id": 1, "quantity": 1, "price": 3500},
    {"id": 2, "order_id": 1, "product_id": 2,
        "cell_id": 5, "quantity": 1, "price": 2400},
    {"id": 3, "order_id": 2, "product_id": 3,
        "cell_id": 5, "quantity": 1, "price": 800},
    {"id": 4, "order_id": 3, "product_id": 2,
        "cell_id": 6, "quantity": 1, "price": 2400},
]

# Return: акты возврата, заполняются при работе алгоритма
returns = []

# ShipmentBox со статусом return - возвратная тара, destination_pp_id - её ПВЗ
shipment_boxes = [
    {"id": 1, "box_barcode": "RET-1", "origin_dc_id": None,
        "destination_pp_id": 1, "status": "return"},
]

shipment_box_items = [
    {"id": 1, "shipment_box_id": 1, "order_item_id": 1},
    {"id": 2, "shipment_box_id": 1, "order_item_id": 2},
]
