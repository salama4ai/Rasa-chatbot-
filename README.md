# salama4ai-chatbot
chatbot based on rasa framework as an assessment NLP task for Master-linux company jan-2022 done by Ahmed Salama

to clone the repository:
```bash
git clone https://github.com/salama4ai/salama4ai-chatbot.git
```
to install rasa
visit https://www.youtube.com/playlist?list=PL75e0qA87dlEWUA5ToqLLR026wIkk2evk```
install anaconda or miniconda
```
conda -V
```
to ensure that you installed anaconda successfully
then open anaconda prompt
```bash
conda update conda
```
then create new virtual environment
```bash
conda create -n yourenvname python=3.8 
```
you must install python3.8 or 3.7 ans rasa compatable with these two

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


