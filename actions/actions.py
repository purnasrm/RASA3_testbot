from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

import logging

log = logging.getLogger(__name__)


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")

        return []


class ActionRecordCar(Action):

    def name(self) -> Text:
        return "action_record_car"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        brand = tracker.get_slot("brand")
        log.info(f'brand: {brand}')
        model = tracker.get_slot("model")
        log.info(f'model: {model}')
        dispatcher.utter_message(text="Car recorded!")

        return [
            SlotSet("brand", None),
            SlotSet("model", None)
        ]


class ActionRecordPerson(Action):

    def name(self) -> Text:
        return "action_record_person"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        name = tracker.get_slot("name")
        log.info(f'name: {name}')
        age = tracker.get_slot("age")
        log.info(f'age: {age}')
        dispatcher.utter_message(text="Person recorded!")

        return [
            SlotSet("name", None),
            SlotSet("age", None)
        ]
