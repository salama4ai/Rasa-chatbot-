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


class ValidateUserQuestion(FormValidationAction):
    
    
    def name(self) -> Text:
        return "validate_user_question"

    def validate_country(self, dispatcher: CollectingDispatcher, tracker: Tracker,
                         domain: DomainDict, slot_value: Any) -> List[Dict[Text, Any]]:
        """ validate the 'country' value"""
        
        print("validate_country")  # to notify me when this function is called
        # check if the country slot value is not null
        if not slot_value:
            dispatcher.utter_message(response = "utter_ask_country")
            return {"country": None}              
            
        # check if the country slot value is in our database  in case the user give country
        country = slot_value.title()         
        try:
            res_country = requests.get(f"{endpoint}Countries", timeout=timeout)
            # check if the status_code is ok, less than 400 
            if not res_country.ok:
                raise Exception
            elif country not in res_country.json()["body"]:
                dispatcher.utter_message(response = "utter_not_found", country=country)
                return {"country": None}  
            else:
                return {"country", country}
        except:
            dispatcher.utter_message(response = "utter_server_failure")
            return {"country": None}


    def validate_pop_cap(self, dispatcher: CollectingDispatcher, tracker: Tracker, 
                         domain: DomainDict, slot_value: Any) -> List[Dict[Text, Any]]:
        """ validate the 'pop_cap' value"""
        
        print("validate_pop_cap")  # to notify me when this function is called
        try:
            pop_cap = slot_value.title()
            if (pop_cap in ["Capital", "Population"]):
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




        print("program now in ActionAnswer.run()")
        # i couldn't make the validation functions work by any means, so i call
        # them explicitly till i could fix them issue        
        ###############################################################
        # to be deleted after i could fix the validation method issue        
        ValidateUserQuestion.validate_pop_cap(self, dispatcher, tracker, domain, tracker.get_slot("pop_cap"))
        country = ValidateUserQuestion.validate_country(self, dispatcher, tracker, domain, tracker.get_slot("country"))
        if not country:
            return
        ################################################################





        country = tracker.get_slot("country")
        pop_cap = tracker.get_slot("pop_cap")              
        payload = {"country": country}
        #headers = {'Content-Type': 'application/json'}          
        
        # the action when the country is selected and pop_cap=capital        
        if pop_cap=="Capital":
            try:
                res_cap = requests.post(f"{endpoint}Capital", 
                                        json=payload, 
                                        timeout=timeout,
                                        #headers=headers, 
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
                                        timeout=timeout,
                                        #headers=headers, 
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