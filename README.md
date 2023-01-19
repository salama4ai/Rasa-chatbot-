# salama4ai-chatbot
chatbot based on rasa framework as an assessment NLP task for Master-linux company jan-2022

## Objective:-
The goal is to create Rasa Chatbot that can provide answers for users questions about the Population and the capitel city of collecton of countries, where the chatbot use the restful API to get that information from third-party website

## initialization tips:-
to clone the repository:
```bash
git clone https://github.com/salama4ai/salama4ai-chatbot.git
```
to install rasa
visit https://www.youtube.com/playlist?list=PL75e0qA87dlEWUA5ToqLLR026wIkk2evk```
install anaconda or miniconda

to ensure that you installed anaconda successfully
```
conda -V
```
then open anaconda prompt, and update conda 
```bash
conda update conda
```
to create new virtual environment
```bash
conda create -n yourenvname python=3.8 
```
you must install python3.8 or 3.7 as rasa compatable with these two


create new folder and go to it and activate you environment
```bash
conda activate test_env
```
install rasa
```
pip install rasa
```
initialize you first project
```
rasa init 
```
if you need to train your bot after modifing files
```
rasa train
```
if you need to interact with your bot
```
rasa shell
```
or 
```
rasa interactive
```
if you use ```rasa interactive``` so you can train the bot by chatting and interacting with it 
if you write custom action so you need to open anaconda prompt and activate the bot and in the prompt run
```rasa run actions``` 
and leave it open in the background to be able to use the custom action with another prompt
you also can run shell in debug mode using ```rasa shell --debug```
and you can use ```rasa train --force``` to enforce retraining
if you make changes in action.py file you don't need to retrain again just rerun ```rasa run actions```

this project done by Ahmed Salama
email:salama4ai@gmail.com
linkedin:linkedin.com/in/salama4ai


