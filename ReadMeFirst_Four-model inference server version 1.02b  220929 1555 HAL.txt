
Four-model inference server version 1.02b  220929 1555.txt

Curl examples of getting inference from each of 4 models embedded in a single flask ML inference server on EC2 using docker and ubuntu, pytorch, flask and the rest...  config file for model definition / descriptions right now; planning to add a mysql table ...  configurable port (set to 8008) with multiple error conditions and additional api functions (e.g. a) list models and b) give a LIST of inferences from a single model on many sentences.


Model2 is multi-classification BERT: (cer aka claim, evidence and reasoning)

harryAtMac@MacMiniM1 model % curl -X POST http://localhost:8008/api/predict -H "Content-Type:application/json" -d "{\"model\":\"model_2\", \"content\":\"Habitat distruction is the greater threat as once all the animals die it won't matter about the Pythons.\"}"

{"Claim":[1,0.8956063985824585],"Evidence":[0,0.00364016299135983],"Reasoning":[1,0.9839255809783936]}

Model1 is binary classification XLNet for CLaim / No Claim

harryAtMac@MacMiniM1 model % curl -X POST http://localhost:8008/api/predict -H "Content-Type:application/json" -d "{\"model\":\"model_1\", \"content\":\"Habitat distruction is the greater threat as once all the animals die it won't matter about the Pythons.\"}"

{"result":"CLAIM","score":0.9922879934310913}

Model3 is binary classification XLNet for Evidence / No Evidence

harryAtMac@MacMiniM1 model % curl -X POST http://localhost:8008/api/predict -H "Content-Type:application/json" -d "{\"model\":\"model_3\", \"content\":\"Habitat distruction is the greater threat as once all the animals die it won't matter about the Pythons.\"}"

{"result":"NOEVIDENCE","score":0.0012019198620691895}


Model4 is binary classification XLNet for Reasoning / No Reasoning

harryAtMac@MacMiniM1 model % curl -X POST http://localhost:8008/api/predict -H "Content-Type:application/json" -d "{\"model\":\"model_4\", \"content\":\"Habitat distruction is the greater threat as once all the animals die it won't matter about the Pythons.\"}"

{"result":"REASONING","score":0.8939672708511353}
harryAtMac@MacMiniM1 model % 


Additional notes:

class Errors:
    UNDEFINED_ERROR = {'error_code': -1, 'error_msg': 'Undefined Error'}
    NO_CONTENT = {'error_code': -2, 'error_msg': 'No content'}
    WRONG_MODEL_NAME = {'error_code': -3, 'error_msg': 'Wrong model name'}
    ONLY_POST_REQUESTS_ALLOWED = {'error_code': -4, 'error_msg': 'Only POST requests allowed'}

Configs:

[server]
port = 8008

also nodel names:

[model_1]
name = model_1
full_name = i172 XLNet CNC
path = model_1
type = score_result
results = CLAIM|NOCLAIM
default = yes
seqn = 1

[model_2]
name = model_2
full_name = i172 BERT Multi
path = model_2
type = multi_scores
seqn = 4

[model_3]
name = model_3
full_name = i172 Evidence XLNet
path = model_3
type = score_result
results = EVIDENCE|NOEVIDENCE
seqn = 2

[model_4]
name = model_4
full_name = i172 Reasoning XLNet
path = model_4
type = score_result
results = REASONING|NOREASONING
seqn = 3


Debug output example:

INFO 2022-09-29 16:17:55,464 Initializing models...

INFO 2022-09-29 16:17:55,464 Initializing model: i172 XLNet CNC / model_1 / score_result

INFO 2022-09-29 16:17:56,650 Initializing model: i172 Evidence XLNet / model_3 / score_result

INFO 2022-09-29 16:17:57,621 Initializing model: i172 Reasoning XLNet / model_4 / score_result

INFO 2022-09-29 16:17:58,609 Initializing model: i172 BERT Multi / model_2 / multi_scores

DEBUG 2022-09-29 16:21:11,831 Options:
{'model': 'model_2', 'content': "Habitat distruction is the greater threat as once all the animals die it won't matter about the Pythons."}
Result:
{'Claim': [1, 0.8956063985824585], 'Evidence': [0, 0.00364016299135983], 'Reasoning': [1, 0.9839255809783936]}

DEBUG 2022-09-29 16:22:17,930 Options:
{'model': 'model_1', 'content': "Habitat distruction is the greater threat as once all the animals die it won't matter about the Pythons."}
Result:
{'result': 'CLAIM', 'score': 0.9922879934310913}



