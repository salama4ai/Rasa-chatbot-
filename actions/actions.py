# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List, Optional
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, EventType
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict 
from rasa_sdk.forms import FormValidationAction
#import os
#import requests
#import json


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
    "usa": "330",
    "greece": "10.7",
    "sweden": "10.35",
    "australia": "25.7",
    "finland": "5.5",
    "japan": "126",
    "russia": "144",
    "india": "1380",   
    }

class ValidateUserQuestion(FormValidationAction):
#
    def name(self) -> Text:
        return "validate_user_question"
#
    def validate_country(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict
            ) -> Dict[Text, Any]:
        """ validate the 'country' value"""
        country = tracker.get_slot("country")
         
        # check if the country slot value is not null
        if not country:
            dispatcher.utter_message(response = "utter_ask_country")  
            return {"country": None}
         
        # check if the country slot value is in our database        
        elif country.lower() not in countries_pop.keys():
            dispatcher.utter_message(response = "utter_query_failure")
            return {"country": None}
             
        else: 
            return {"country", country}
#
    def validate_pop_cap(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict
            ) -> Dict[Text, Any]:
        """ validate the 'pop_cap' value"""
        pop_cap = tracker.get_slot("popcap")
         
        if not pop_cap:
            dispatcher.utter_message(response = "utter_ask_pop_cap")
            return {"pop_cap": None}
        else:
            return {"pop_cap": pop_cap}
                   
#
class ActionAnswer(Action):

    def name(self) -> Text:
        return "action_answer"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         
        country = tracker.get_slot("country")
        pop_cap_value = tracker.get_slot("pop_cap")
        if pop_cap_value==capital:
            dispatcher.utter_message(response = "utter_answer_cap", 
                                     country=f"{country}", 
                                     cap=f"{countries_cap[country.lower()]}")
        elif pop_cap_value==population:
            dispatcher.utter_message(response = "utter_answer_pop", 
                                     country=f"{country}",  
                                     pop=f"{countries_pop[country.lower()]}")            
        else :
            dispatcher.utter_message(response = "utter_answer_both", 
                                     country=f"{country}", 
                                     cap=f"{countries_cap[country.lower()]}", 
                                     pop=f"{countries_pop[country.lower()]}")            
        return


   
