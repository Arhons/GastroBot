from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.events import FollowupAction
from rasa_sdk.events import BotUttered
import sqlite3
from datetime import datetime


# Фиктивные данные для меню
menu = {
    '1': {
        'dish': 'Пицца Маргарита',
        'price': 10.99
    },
    '2': {
        'dish': 'Спагетти Болоньезе',
        'price': 8.99
    },
    '3': {
        'dish': 'Салат Цезарь',
        'price': 5.99
    }
}

# Фиктивные данные о специальных предложениях
special_offers = {
    '1': 'Бесплатная доставка при заказе от $20',
    '2': '10% скидка на все пиццы в понедельник'
}

# Фиктивные данные о статусе заказа
order_status = {
    '1': {
        'status': 'В обработке',
        'delivery_time': '30 минут'
    },
    '2': {
        'status': 'Доставлен',
        'delivery_time': '45 минут'
    }
}


class ActionBookTable(Action):
    def name(self) -> Text:
        return "action_book_table"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Здесь можно обработать запрос на заказ столика и выполнить необходимые действия
        dispatcher.utter_message(text="Столик успешно забронирован!")
        return []


class ActionOrderFood(Action):
    def name(self) -> Text:
        return "action_order_food"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        numbers_list = tracker.get_slot('numbers_list')
        try:
            numbers_list = tuple(map(int, numbers_list))
        except:
            dispatcher.utter_message(text="Ошибка. Попробуйте спросить ещё раз")
        else:
            dispatcher.utter_message(text="Ваш заказ принят! Позиции по заказу:")
            with sqlite3.connect('example.db') as conn:
                cursor = conn.cursor()
                # Сохраняем заказ в таблицу orders
                order = [(datetime.now(), 60, 'В обработке', '1111')]
                cursor.executemany('INSERT INTO orders (order_date, delivery_time_min, \
                                   status, client_phone) VALUES (?,?,?,?)', order)
                # Получаем наименования и цены по позициям
                res = cursor.execute(f"SELECT * FROM menu WHERE id IN {numbers_list};").fetchall()
                conn.commit()
            price = 0
            for row in res:
                text = f"{row[0]}. {row[1]} \t {row[2]} $"
                price += int(row[2])
                dispatcher.utter_message(text=text)
            dispatcher.utter_message(text=f"Общая сумма заказа: {price} $")
            dispatcher.utter_message(text="Спасибо за заказ! Ожидайте доставку.")
        return []


class ActionGetMenu(Action):
    def name(self) -> Text:
        return "action_get_menu"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Вот наше меню:")
        with sqlite3.connect('example.db') as conn:
            cursor = conn.cursor()
            res = cursor.execute("SELECT * FROM menu;")
            for row in res.fetchall():
                text = f"{row[0]}. {row[1]} \t {row[2]} $"
                dispatcher.utter_message(text=text)
        # for dish_id, dish_info in menu.items():
        #     dish_text = f"{dish_id}. {dish_info['dish']} - {dish_info['price']} $"
        #     dispatcher.utter_message(text=dish_text)
        return []


class ActionGetSpecialOffers(Action):
    def name(self) -> Text:
        return "action_get_special_offers"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="У нас есть следующие специальные предложения:")
        with sqlite3.connect('example.db') as conn:
            cursor = conn.cursor()
            res = cursor.execute("SELECT * FROM special_offers;")
            for row in res.fetchall():
                text = f"{row[0]}. {row[1]}"
                dispatcher.utter_message(text=text)
        return []


class ActionGetOrderStatus(Action):
    def name(self) -> Text:
        return "action_get_order_status"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        with sqlite3.connect('example.db') as conn:
            cursor = conn.cursor()
            orders = cursor.execute("SELECT * FROM orders WHERE id=(SELECT max(id) FROM orders);") \
                .fetchall()
        if orders:
            order_date = orders[0][1]
            delivery_time_min = orders[0][2]
            status = orders[0][3]
            message = f"Статус вашего заказа: {status} \nВремя доставки: {delivery_time_min} мин."
            message += f"\nДата и время заказа: {order_date.split('.')[0]}"
        else:
            message = "Заказ не найден"
        dispatcher.utter_message(text=message)
        return []
