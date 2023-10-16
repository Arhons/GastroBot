from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.events import FollowupAction
from rasa_sdk.events import BotUttered
import sqlite3

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

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Здесь можно обработать запрос на заказ столика и выполнить необходимые действия
        dispatcher.utter_message(text="Столик успешно забронирован!")
        return []

class ActionOrderFood(Action):
    def name(self) -> Text:
        return "action_order_food"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Здесь можно обработать запрос на заказ еды с доставкой и выполнить необходимые действия
        dispatcher.utter_message(text="Ваш заказ принят! Ожидайте доставку.")
        return []

class ActionGetMenu(Action):
    def name(self) -> Text:
        return "action_get_menu"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Вот наше меню:")
        for dish_id, dish_info in menu.items():
            dish_text = f"{dish_id}. {dish_info['dish']} - {dish_info['price']} $"
            dispatcher.utter_message(text=dish_text)
        return []

class ActionGetSpecialOffers(Action):
    def name(self) -> Text:
        return "action_get_special_offers"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="У нас есть следующие специальные предложения:")
        for offer_id, offer_text in special_offers.items():
            offer_text = f"{offer_id}. {offer_text}"
            dispatcher.utter_message(text=offer_text)
        return []

class ActionGetOrderStatus(Action):
    def name(self) -> Text:
        return "action_get_order_status"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        order_id = tracker.get_slot('order_id')
        if order_id in order_status:
            status = order_status[order_id]['status']
            delivery_time = order_status[order_id]['delivery_time']
            message = f"Статус вашего заказа: {status}\nВремя доставки: {delivery_time}"
        else:
            message = "Заказ не найден"
        dispatcher.utter_message(text=message)
        return []