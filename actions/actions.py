# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import ActionExecuted, UserUttered


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")
        data = {
            "intent": {
                "name": "bot_challenge",
                "confidence": 1.0,
            }
        }
        
        return [
            ActionExecuted("action_listen"),
            UserUttered(text="/bot_challenge", parse_data=data)
        ]

