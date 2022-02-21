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
import json
#from aws_requests_auth.boto_utils import BotoAWSRequestsAuth
#import jwt

endpoint = "https://qcooc59re3.execute-api.us-east-1.amazonaws.com/dev/get"
timeout = 55

#auth = BotoAWSRequestsAuth(aws_host="qcooc59re3.execute-api.us-east-1.amazonaws.com",
#                           aws_region="us-east-1", aws_service="execute-api")


     #any class name but it's good to be as the name of the action in camel
class ValidateCountryPopCapForm(FormValidationAction):
    
    
    def name(self) -> Text:
        return "validate_country_pop_cap_form"
              #"validate_<form_name>"

    async def required_slots(self, domain_slots, dispatcher, tracker, domain):
        print(f'>>> Domain slots:\n{domain_slots}\n========')
        return domain_slots
                        
    
    #def validate_<slot_name>
    def validate_country(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker,
                         domain: DomainDict) -> Dict[Text, Any]:
        """ validate the 'country' value"""
        
        print("validate_country", "\n slot_value = ", slot_value)
        # to notify me when this function is called

        # check if the country slot value is not null
        if slot_value is None:
            dispatcher.utter_message(response = "utter_ask_country")
            return {"country": None}              
        elif len(slot_value)>3:
            country = slot_value.title()
        else:
            country = slot_value.upper()
              
        print(f"country = {country}")
        
        # check if the country slot value is in our database  in case the user give country        
        try:
            res_country = requests.get(f"{endpoint}Countries", timeout=timeout)
            # check if the status_code is ok, less than 400 
            if res_country.ok==False:
                raise Exception
            elif country not in res_country.json()["body"]:
                dispatcher.utter_message(response = "utter_not_found", country=country)
                return {"country": None}  
            else:
                return {"country": country}
        except:
            dispatcher.utter_message(response = "utter_server_failure")
            return {"country": None}

    #def validate_<slot_name>
    def validate_pop_cap(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, 
                         domain: DomainDict) -> Dict[Text, Any]:
        """ validate the 'pop_cap' value"""
        
        print("validate_pop_cap")  # to notify me when this function is called
        try:
            pop_cap = slot_value.title()
            if pop_cap in ["Capital", "Population"]:
                return {"pop_cap": pop_cap}
            else:
                raise Exception()
        except:
            dispatcher.utter_message(response = "utter_ask_pop_cap",
                                     buttons=[{"title": "Capital", 
                                              "payload": '/inform{"pop_cap":"Capital"}'},     
                                              {"title": "Population",
                                              "payload": '/inform{"pop_cap":"Population"}'}])
            return {"pop_cap": None}          
    
    
class ActionAnswer(Action):
    

    def name(self) -> Text:
        return "action_answer"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, 
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        country = tracker.get_slot("country")
        pop_cap = tracker.get_slot("pop_cap")              
        payload = {"country": country}
        #headers = {'Content-Type': 'application/json'}          
        print(f"action_answer pop_cap = {pop_cap}, country = {country}")
        # the action when the country is selected and pop_cap=capital        
        if pop_cap=="Capital":
            try:
                res_cap = requests.post(f"{endpoint}Capital", 
                                        json=payload, 
                                        timeout=timeout
                                        #,headers=headers, 
                                        #auth=auth
                                        )
                # check if the status_code is ok, i.e less than 400 
                # or i can not checking this it will raise an error any way
                if not res_cap.ok:
                    raise Exception             # res_cap.raise_for_status()
                # getting the response of capital
                cap = res_cap.json()["body"]["capital"]
                dispatcher.utter_message(response = "utter_answer_cap", 
                                         country = country, cap = cap)
            except:
                dispatcher.utter_message(response = "utter_server_failure")
                
                                        
        # the action when the country is selected and pop_cap=population
        elif pop_cap=="Population":
            try:
                res_pop = requests.post(f"{endpoint}Population", 
                                        json=payload, 
                                        timeout=timeout
                                        #,headers=headers, 
                                        #auth=auth
                                        )
                # check if the status_code is ok, i.e less than 400 
                if not res_pop.ok:
                    raise Exception
                # getting the response of population
                pop = res_pop.json()["body"]["population"]
                dispatcher.utter_message(response = "utter_answer_pop", 
                                         country = country, pop = pop)
            except:
                dispatcher.utter_message(response = "utter_server_failure")         
        return