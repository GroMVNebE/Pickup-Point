from datetime import datetime, timedelta

from algorithms import check_delivery, find_best_cell, issue_order, process_return


def make_return(order_item_id, reason_type, days_ago):
    return {
        "order_item_id": order_item_id,
        "client_id": 1,
        "operator_id": 3,
        "reason_type": reason_type,
        "comment": "",
        "issued_at": datetime.now() - timedelta(days=days_ago),
    }


# Тесты адресного хранения
find_best_cell(2, (10, 10, 10))
find_best_cell(1, (100, 100, 100))
find_best_cell(1, (25, 25, 25))

# Тесты сверки поставки
check_delivery({"111", "222"}, {"111", "222"}, set())
check_delivery({"111", "222", "333"}, {"111", "333", "444"}, {"333"})

# Тесты выдачи заказов
issue_order("0000", 1)
issue_order("1111", 1)
issue_order("4821", 1)

# Тесты возвратов
process_return(make_return(3, "Брак", 30), 1)
process_return(make_return(3, "Передумал", 1), 1)
process_return(make_return(3, "Брак", 1), 1)
process_return(make_return(4, "Брак", 1), 1)
