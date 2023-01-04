# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionShowList(Action):

    def name(self) -> Text:
        return "action_show_list"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        list_uppercase = ['A', 'B', 'C']
        list_lowercase = ['a', 'b', 'c']

        upper_case_string = ""
        lower_case_string = ""

        for letter in list_uppercase:
            upper_case_string += letter + "\n"

        for letter in list_lowercase:
            lower_case_string += letter + "\n"

        dispatcher.utter_message(
            response="utter_list",
            upper_case_list=upper_case_string,
            lower_case_list=lower_case_string
        )

        return []
