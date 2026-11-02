from datetime import datetime, timedelta

import data

RETURN_PERIOD_DAYS = 14
ALLOWED_REASONS = {"Брак", "Не подошёл размер", "Не соответствует описанию"}
RETURN_BOX_CAPACITY = 3


def find_best_cell(pickup_point_id, dimensions):
    """Алгоритм адресного хранения (Best-Fit)"""
    # Проверка наличия свободных ячеек в ПВЗ
    free_cells = []
    for cell in data.cells:
        if cell["pickup_point_id"] == pickup_point_id and not cell["is_occupied"]:
            free_cells.append(cell)

    if not free_cells:
        print("Нет подходящих ячеек")
        return None

    # Фильтрация ячеек по объёму
    length, width, height = dimensions
    volume = length * width * height
    suitable_cells = []
    for cell in free_cells:
        if cell["size"] >= volume:
            suitable_cells.append(cell)

    if not suitable_cells:
        print("Нет подходящих ячеек")
        return None

    # Сортировка ячеек по возрастанию (Best-Fit)
    suitable_cells.sort(key=lambda cell: cell["size"])

    best_cell = suitable_cells[0]
    print(f"Ячейка: {best_cell['cell_code']}, стеллаж {best_cell['rack_number']}, "
          f"полка {best_cell['shelf_number']}, объём {best_cell['size']} см³")
    return best_cell


def check_delivery(expected, scanned, defective):
    """Алгоритм сверки поставки. Принимает множества штрихкодов"""
    documents = []

    # Формирование множества недостач
    shortage = expected - scanned
    if shortage:
        documents.append(
            {"type": "Акт о недостающих товарах", "items": shortage})

    # Формирование множества излишков
    extra = scanned - expected
    if extra:
        documents.append(
            {"type": "Акт о поставке лишних товаров", "items": extra})

    if defective:
        documents.append({"type": "Акт дефектовки", "items": defective})

    # Акт приёмки содержит только корректные товары
    accepted = (expected & scanned) - defective
    documents.append({"type": "Акт приёмки", "items": accepted})

    for document in documents:
        print(f"{document['type']}: {sorted(document['items'])}")
    return documents


def issue_order(client_code, pickup_point_id):
    """Алгоритм верификации и выдачи заказа клиенту"""
    # Сверка кода клиента
    client = None
    for user in data.users:
        if user["verification_code"] == client_code and user["code_expires_at"] > datetime.now():
            client = user
            break

    if client is None:
        print("Ошибка верификации клиента")
        return None

    # Получение информации о заказах клиента в данном ПВЗ
    order_ids = []
    for order in data.orders:
        if order["client_id"] == client["id"] and order["pickup_point_id"] == pickup_point_id:
            order_ids.append(order["id"])

    # Составление списка товаров и их ячеек
    products_by_id = {product["id"]: product for product in data.products}
    cells_by_id = {cell["id"]: cell for cell in data.cells}
    result = []
    for item in data.order_items:
        if item["order_id"] in order_ids:
            result.append({
                "order_id": item["order_id"],
                "title": products_by_id[item["product_id"]]["title"],
                "cell_code": cells_by_id[item["cell_id"]]["cell_code"],
            })

    print(f"Клиент: {client['full_name']}")
    for row in result:
        print(
            f"Заказ {row['order_id']}: {row['title']} - ячейка {row['cell_code']}")
    return result


def process_return(item, pickup_point_id):
    """Алгоритм обработки возврата"""
    # Проверка срока и причины возврата
    deadline = item["issued_at"] + timedelta(days=RETURN_PERIOD_DAYS)
    if datetime.now() > deadline or item["reason_type"] not in ALLOWED_REASONS:
        print("Возврат невозможен")
        return None

    # Создание акта возврата
    return_act = {
        "id": len(data.returns) + 1,
        "order_item_id": item["order_item_id"],
        "client_id": item["client_id"],
        "operator_id": item["operator_id"],
        "reason_type": item["reason_type"],
        "comment": item["comment"],
        "created_at": datetime.now(),
        "status": "Создан",
    }
    data.returns.append(return_act)

    # Поиск свободной тары для возвратов
    free_box = None
    for box in data.shipment_boxes:
        if box["status"] == "return" and box["destination_pp_id"] == pickup_point_id:
            items_count = 0
            for box_item in data.shipment_box_items:
                if box_item["shipment_box_id"] == box["id"]:
                    items_count += 1
            if items_count < RETURN_BOX_CAPACITY:
                free_box = box
                break

    # Создание новой возвратной тары
    if free_box is None:
        box_id = len(data.shipment_boxes) + 1
        free_box = {
            "id": box_id,
            "box_barcode": f"RET-{box_id}",
            "origin_dc_id": None,
            "destination_pp_id": pickup_point_id,
            "status": "return",
        }
        data.shipment_boxes.append(free_box)

    # Привязка товара к таре
    data.shipment_box_items.append({
        "id": len(data.shipment_box_items) + 1,
        "shipment_box_id": free_box["id"],
        "order_item_id": item["order_item_id"],
    })

    print(f"Упакуйте товар и поместите его в тару {free_box['box_barcode']}")
    return return_act
