# SGREL2WebAppML

This webapp will fetch content and process it by certain model.

Model link: https://drive.google.com/drive/folders/1XelXeuxk3yqKF22bOAYPSUTURHhPHkwX

## Usage:

### Start WebApp:  
```
python3 s2waml.py
```
---
### Predict content:
```
POST /api/predict
with data: {'content': ..., 'model_name': ...}
```
Example result Model 1:
```
{"result":"CLAIM","score":0.9973957538604736}
```
Example result Model 2:
```
{"Claim":[1,0.9996739625930786],"Evidence":[0,0.06034946069121361],"Reasoning":[0,0.17518417537212372]}
```
---
### Predict list of contents:
```
POST /api/predict
with data: {'content_list': [...], 'model_name': ...}
```
Example result:
```
{"result_list":[{"result":"CLAIM","score":0.9973957538604736},{...}]}
```

---
### List model names:
```
GET /api/list_models
```
Example result:
```
{'default': 'model_1', 'models': [{'full_name': 'Some Model 1', 'name': 'model_1'}]}
```
---
### Test all models:
```
python3 try_all_models.py
```
---
## Install on Ubuntu 22.04:
Execute commands:
```
sudo apt update
sudo apt install python3-pip
sudo systemctl mask apt-daily.service
sudo systemctl disable apt-daily.timer
sudo systemctl disable unattended-upgrades
sudo systemctl disable --now apt-daily{,-upgrade}.{timer,service}
sudo shutdown -r now
sudo pip3 install sentencepiece torch flask flask_cors transformers requests
sudo nano /etc/systemd/system/sgrel2_ml_webapp.service
```
Write file contents:
```
[Unit]
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/ubuntu/SGREL2WebAppML/s2waml.py

[Install]
WantedBy=default.target
```
Execute commands:
```
sudo chmod 664 /etc/systemd/system/sgrel2_ml_webapp.service
sudo chmod 744 /home/ubuntu/SGREL2WebAppML/s2waml.py
sudo systemctl daemon-reload
sudo systemctl enable sgrel2_ml_webapp.service
sudo shutdown -r now
```

Set SGREL2 MySQL option `api_settings` -> 'ai_score_base_url' to new address
