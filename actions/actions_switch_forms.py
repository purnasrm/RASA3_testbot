
# code in this file is based on https://github.com/RasaHQ/financial-demo/

from typing import Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from rasa_sdk.events import (
    SlotSet,
    EventType,
)

import logging

log = logging.getLogger(__name__)

NEXT_FORM_NAME = {
    "record_person": "person_form",
    "record_car": "car_form"
}

FORM_DESCRIPTION = {
    "person_form": "recording a person",
    "car_form": "recording a car",
}


class ActionSwitchFormsAsk(Action):
    """Asks to switch forms"""

    def name(self) -> Text:
        return "action_switch_forms_ask"

    async def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        """Executes the custom action"""
        active_form_name = tracker.active_form.get("name")
        intent_name = tracker.latest_message["intent"]["name"]
        next_form_name = NEXT_FORM_NAME.get(intent_name)

        if (
            active_form_name not in FORM_DESCRIPTION.keys()
            or next_form_name not in FORM_DESCRIPTION.keys()
        ):
            log.debug(
                f"Cannot create text for `active_form_name={active_form_name}` & "
                f"`next_form_name={next_form_name}`"
            )
            next_form_name = None
        else:
            text = (
                f"We haven't completed the {FORM_DESCRIPTION[active_form_name]} yet. "
                f"Are you sure you want to switch to {FORM_DESCRIPTION[next_form_name]}?"
            )
            buttons = [
                {"payload": "/affirm", "title": "Yes"},
                {"payload": "/deny", "title": "No"},
            ]
            dispatcher.utter_message(text=text, buttons=buttons)
        return [SlotSet("next_form_name", next_form_name)]


class ActionSwitchFormsDeny(Action):
    """Does not switch forms"""

    def name(self) -> Text:
        return "action_switch_forms_deny"

    async def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        """Executes the custom action"""
        active_form_name = tracker.active_form.get("name")

        if active_form_name not in FORM_DESCRIPTION.keys():
            log.debug(
                f"Cannot create text for `active_form_name={active_form_name}`."
            )
        else:
            text = f"Ok, let's continue with the {FORM_DESCRIPTION[active_form_name]}."
            dispatcher.utter_message(text=text)

        return [SlotSet("next_form_name", None)]


class ActionSwitchFormsAffirm(Action):
    """Switches forms"""

    def name(self) -> Text:
        return "action_switch_forms_affirm"

    async def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        """Executes the custom action"""
        active_form_name = tracker.active_form.get("name")
        next_form_name = tracker.get_slot("next_form_name")

        if (
            active_form_name not in FORM_DESCRIPTION.keys()
            or next_form_name not in FORM_DESCRIPTION.keys()
        ):
            log.debug(
                f"Cannot create text for `active_form_name={active_form_name}` & "
                f"`next_form_name={next_form_name}`"
            )
        else:
            text = (
                f"Great. Let's switch from the {FORM_DESCRIPTION[active_form_name]} "
                f"to {FORM_DESCRIPTION[next_form_name]}. "
                f"Once completed, you will have the option to switch back."
            )
            dispatcher.utter_message(text=text)

        return [
            SlotSet("previous_form_name", active_form_name),
            SlotSet("next_form_name", None),
        ]


class ActionSwitchBackAsk(Action):
    """Asks to switch back to previous form"""

    def name(self) -> Text:
        return "action_switch_back_ask"

    async def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        """Executes the custom action"""
        previous_form_name = tracker.get_slot("previous_form_name")

        if previous_form_name not in FORM_DESCRIPTION.keys():
            log.debug(
                f"Cannot create text for `previous_form_name={previous_form_name}`"
            )
            previous_form_name = None
        else:
            text = (
                f"Would you like to go back to the "
                f"{FORM_DESCRIPTION[previous_form_name]} now?."
            )
            buttons = [
                {"payload": "/affirm", "title": "Yes"},
                {"payload": "/deny", "title": "No"},
            ]
            dispatcher.utter_message(text=text, buttons=buttons)

        return [SlotSet("previous_form_name", None)]
