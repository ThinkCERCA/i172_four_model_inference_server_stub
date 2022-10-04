"""
This script will iterate all models on SGREL2WebAppML
  and check content on each model
"""
import requests

base_url = 'http://localhost:8008'

content = "I believe that the Everglades biggest threat was draining the swamp because snakes offer a threat to "\
          "animals not the area which the animals live in and if we were worried about the animals then why "\
          "don't they move to a different swamp why concern our selves with our problems not the animals."

for model_dict in requests.get(f'{base_url}/api/list_models').json()['models']:
    print(f"Checking model: {model_dict['full_name']} ...")
    x = requests.post(f'{base_url}/api/predict', json={'content': content, 'model': model_dict['name']})
    print(f"Result: {x.text}")
