import os
import requests

class HKBU_ChatGPT():
    def __init__(self):
        self.config = {
            'BASICURL': os.environ.get('BASICURL'),
            'MODELNAME': os.environ.get('MODELNAME'),
            'APIVERSION': os.environ.get('APIVERSION'),
            'ACCESS_TOKEN_GPT': os.environ.get('ACCESS_TOKEN_GPT')
        }
        if None in self.config.values():
            raise ValueError("Environment variables are not properly set.")

    def submit(self, message):
        conversation = [{"role": "user", "content": message}]
        url = self.config['BASICURL'] + "/deployments/" + self.config['MODELNAME'] + "/chat/completions/?api-version=" + self.config['APIVERSION']
        headers = {'Content-Type': 'application/json', 'api-key': self.config['ACCESS_TOKEN_GPT']}
        payload = {'messages': conversation}
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data['choices'][0]['message']['content']
        else:
            return 'Error:', response