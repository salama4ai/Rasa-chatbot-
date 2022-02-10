# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List, Optional
from rasa_sdk import Action, Tracker#, FormValidationAction
from rasa_sdk.events import SlotSet, EventType
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict 
from rasa_sdk.forms import FormValidationAction
#import os
import requests
#import json
#import jwt


countries_cap = {
    "USA":"Washington, D.C.",
    "Greece": "Athens",
    "Sweden": "Stockholm",
    "Australia": "Canberra",
    "Finland": "Helsinki",
    "Japan": "Tokyo",
    "Russia": "Moscow",
    "India": "New Delhi"}

countries_pop = {
    "USA": "330",
    "Greece": "10.7",
    "Sweden": "10.35",
    "Australia": "25.7",
    "Finland": "5.5",
    "Japan": "126",
    "Russia": "144",
    "India": "1380"}

base_url = "https://qcooc59re3.execute-api.us-east-1.amazonaws.com/dev/get"
timeout = 35

class ValidateUserQuestion(FormValidationAction):

    def name(self) -> Text:
        return "validate_user_question"

    def validate_country(self, dispatcher: CollectingDispatcher, tracker: Tracker
                         , domain: DomainDict
                         #, country: Any                ###############
                         ) -> Dict[Text, Any]:
        """ validate the 'country' value"""
        
        country = tracker.get_slot("country")###############
        print("validation")
        # check if the country slot value is not null
        if not country:
            dispatcher.utter_message(response = "utter_ask_country")  
            return {"country": None}
         
        # check if the country slot value is in our database  in case the user give country
        else:
            try:
                get_countries = requests.get(f"{base_url}Countries", timeout=timeout)                                             
                # check if the status_code is ok, less than 400 
                if get_countries.ok:
                    print("connection is ok 200")
                    if country.title() not in get_countries.json()["body"]:
                        print("country not in the list")
                        dispatcher.utter_message(response = "utter_not_found")
                        return {"country": None}  
                    else:
                        print("country in the list")
                        return {"country", country.title()}  
                else:
                    print("connection is not ok >400")
                    dispatcher.utter_message(response = "utter_server_failure")
                    return {"country": None}                     
            except:
                print("connection is not ok >400")
                dispatcher.utter_message(response = "utter_server_failure")
                return {"country": None}            

    def validate_pop_cap(self, dispatcher: CollectingDispatcher, tracker: Tracker
                         , domain: DomainDict
                         , pop_cap: Any          ##################
                         ) -> Dict[Text, Any]:
        """ validate the 'pop_cap' value"""
        
        #pop_cap = tracker.get_slot("pop_cap")##########
        if not pop_cap:
            dispatcher.utter_message(response = "utter_ask_pop_cap")
            return {"pop_cap": None}
        else:
            return {"pop_cap": pop_cap.title()}
            
                   
class ActionAnswer(Action):

    def name(self) -> Text:
        return "action_answer"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker
            , domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         
        country = tracker.get_slot("country")
        pop_cap = tracker.get_slot("pop_cap")
        
        

        # the action when the country is selected and in case of the capital selection
        print("action_answer")
        # check if the status_code is ok, 
        if pop_cap=="Capital":                         
            try:                
                print("before capital")
                payload_cap = {}
                get_capital = requests.get(f"{base_url}Capital", 
                                           params=payload_cap, timeout=timeout)
                print("after capital")                
                if get_capital.ok:                    
                    dispatcher.utter_message(response = "utter_answer_cap", 
                                             country = f"{country}", 
                                             cap = get_capital.json()["body"]["capital"])
                else:
                    print("after capital")                    
                    dispatcher.utter_message(response = "utter_server_failure")
            except:
                dispatcher.utter_message(response = "utter_server_failure")
                
                
                        
        # the action when the country is selected and in case of the population selection
        elif pop_cap=="Population":
            try:
                payload_cap = {}                
                get_population = requests.get(f"{base_url}Population",
                                              params=payload_cap, timeout=timeout)                                              
                # check if the status_code is ok, 
                if get_population.ok:
                    dispatcher.utter_message(response = "utter_answer_cap", 
                                             country = f"{country}", 
                                             cap = get_population.json()["body"]["population"])
                else:
                    dispatcher.utter_message(response = "utter_server_failure")
            except:
                dispatcher.utter_message(response = "utter_server_failure")                       
        return