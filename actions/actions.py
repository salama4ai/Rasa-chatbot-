# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

 from typing import Any, Text, Dict, List
#
 from rasa_sdk import Action, Tracker
 from rasa_sdk.events import SlotSet
 from rasa_sdk.executor import CollectingDispatcher
 from rasa_sdk.types import DomainDict
#
#

countries_cap = {
    "usa":"Washington, D.C.",
    "greece": "Athens",
    "sweden": "Stockholm",
    "australia": "Canberra",
    "finland": "Helsinki",
    "japan": "Tokyo",
    "russia": "Moscow",
    "india": "New Delhi",   
    }

countries_pop = {
    "usa": 330,
    "greece": 10.7,
    "sweden": 10.35,
    "australia": 25.7,
    "finland": 5.5,
    "japan": 126,
    "russia": 144,
    "india": 1380,   
    }

 class ValidateUserQuestion(FormValidationAction):
#
     def name(self) -> Text:
         return "validate_user_question"
#
     def validate_pop_cap(
             self,
             slot_value: Any,
             dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: DomainDict
             ) -> Dict[Text, Any]:

         if slot_value.lower() not in countries_pop:
             dispatcher.utter_message(text=)
             return {"country": None}
             
         dispatcher.utter_message(text="Hello World!")
         state = next(tracker.get_latest_entity_values(country), None)

         return [SlotSet("country", state)]
