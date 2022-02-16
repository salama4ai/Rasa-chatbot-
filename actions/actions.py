# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List, Optional
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.events import SlotSet, EventType
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict 
import requests
#import jwt


countries_cap = {
    "Aa": "ccaappiittaall",
    "USA":"Washington, D.C.",
    "Greece": "Athens",
    "Sweden": "Stockholm",
    "Australia": "Canberra",
    "Finland": "Helsinki",
    "Japan": "Tokyo",
    "Russia": "Moscow",
    "India": "New Delhi"}

countries_pop = {
    "Aa": "1198798798790",
    "USA": "330",
    "Greece": "10.7",
    "Sweden": "10.35",
    "Australia": "25.7",
    "Finland": "5.5",
    "Japan": "126",
    "Russia": "144",
    "India": "1380"}

base_url = "https://qcooc59re3.execute-api.us-east-1.amazonaws.com/dev/get"
timeout = 55

class ValidateUserQuestion(FormValidationAction):
    
    
    def name(self) -> Text:
        return "validate_user_question"

    def validate_country(self, dispatcher: CollectingDispatcher, tracker: Tracker,
                         domain: DomainDict, slot_value: Any) -> List[Dict[Text, Any]]:
        """ validate the 'country' value"""
        
        print("validate_country")
        # check if the country slot value is not null
        if not slot_value:
            print("slot_value_country is None")            
            dispatcher.utter_message(response = "utter_ask_country")
            return {"country": None}              
            
        # check if the country slot value is in our database  in case the user give country
        country = slot_value.title()         
        try:
            get_countries = requests.get(f"{base_url}Countries", timeout=timeout)                                             
            # check if the status_code is ok, less than 400 
            if not get_countries.ok:
                print("connection is not ok")                            
                raise Exception
            elif country not in get_countries.json()["body"]:
                print("country not found")                            
                dispatcher.utter_message(response = "utter_not_found", country=country)
                return {"country": None}  
            else:
                print("country slot is ok")                            
                return {"country", country}                      
        except:
            dispatcher.utter_message(response = "utter_server_failure")
            return {"country": None}            


    def validate_pop_cap(self, dispatcher: CollectingDispatcher, tracker: Tracker, 
                         domain: DomainDict, slot_value: Any) -> List[Dict[Text, Any]]:
        """ validate the 'pop_cap' value"""
        
        print("validate_pop_cap")            
        try:            
            pop_cap = slot_value.title()    
            if (pop_cap in ["Capital", "Population"]):
                print("pop_cap is correct")                            
                return {"pop_cap": pop_cap} 
            else:
                raise Exception()
        except:  
            print("pop_cap exception")                                                 
            dispatcher.utter_message(response = "utter_ask_pop_cap",
                                     buttons=[{"title": "Capital", 
                                              "payload": '/inform{{"pop_cap":"Capital"}}'},     
                                              {"title": "Population",
                                              "payload": '/inform{{"pop_cap":"Population"}}'}])
            return {"pop_cap": None}            



class ActionAnswerTemporarly(Action):
    """this function is temporal function untill i find the correct link to the get_capital and get_population"""

    
    def name(self) -> Text:
        return "temporarly_action_answer"
    

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, 
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # i couldn't make the validation functions work by any means, so i call them explicitly
        # till i fix them issue
        ValidateUserQuestion.validate_country(self, dispatcher, tracker, domain, tracker.get_slot("country"))        
        ValidateUserQuestion.validate_pop_cap(self, dispatcher, tracker, domain, tracker.get_slot("pop_cap"))

        country = tracker.get_slot("country").title()
        pop_cap = tracker.get_slot("pop_cap").title()        
        print("temporarly_action_answer", country, pop_cap)

        # the action when the country is selected and pop_cap=Capital
        if pop_cap=="Capital":  
            print(f"country is {country}, pop_cap is {pop_cap}")                                             
            dispatcher.utter_message(response = "utter_answer_cap", 
                                     country = country, 
                                     cap = countries_cap[country])
                                        
        # the action when the country is selected and pop_cap=Population
        elif pop_cap=="Population":
            print(f"country is {country}, pop_cap is {pop_cap}")                                             
            dispatcher.utter_message(response = "utter_answer_pop", 
                                     country = country, 
                                     pop = countries_pop[country])                      
      
        return[]
    
    
class ActionAnswer(Action):

    def name(self) -> Text:
        return "action_answer"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, 
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         
        country = tracker.get_slot("country")
        pop_cap = tracker.get_slot("pop_cap")                       

        # the action when the country is selected and pop_cap=capital
        print("action_answer")
        if pop_cap=="Capital": 
            payload_cap = {}                         
            try:                
                get_capital = requests.get(f"{base_url}Capital", 
                                           timeout=timeout, params=payload_cap)
                # check if the status_code is ok, i.e less than 400 
                if not get_capital.ok:
                    raise Exception
                cap = get_capital.json()["body"]["capital"]
                dispatcher.utter_message(response = "utter_answer_cap", 
                                         country = country, cap = cap)
            except:
                dispatcher.utter_message(response = "utter_server_failure")
                
                                        
        # the action when the country is selected and pop_cap=population
        elif pop_cap=="Population":
            payload_pop = {}
            try:
                get_population = requests.get(f"{base_url}Population", 
                                              timeout=timeout, params=payload_pop)                                              
                # check if the status_code is ok, i.e less than 400 
                if not get_population.ok:
                    raise Exception
                pop = get_population.json()["body"]["population"]
                dispatcher.utter_message(response = "utter_answer_pop", 
                                         country = country, pop = pop)
            except:
                dispatcher.utter_message(response = "utter_server_failure")                       
        return    