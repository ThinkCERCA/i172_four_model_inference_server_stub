## SGREL2WebAppML Version 1.02 (2022-09-29)
#### changes:  
```
1) config.ini [model_N] section changes:
  1.1) added "type": score_result or multi_scores
  1.2) added "results", e.g. CLAIM|NOCLAIM for score_result type models
  1.3) added "seqn" - place of model in the list
2) added models:
  2.1) model_3 - i172 Evidence XLNet
  2.2) model_4 - i172 Reasoning XLNet
3) replaced by new version: 
  model_2 - i172 BERT Multi
```

New / updated files (since 1.01):  
```
configs/config.ini
models/model_2/*
       model_3/*
       model_4/*
swa_lib/models/*
        configs.py
s2waml.py
```

-------------------------------------------
## SGREL2WebAppML Version 1.01 (2022-09-22)
#### Add Model 2 

New / updated files (since 1.0):  
```
configs/config.ini
models/model_2/*
swa_lib/models/*
        configs.py
```

---
## SGREL2WebAppML Version 1.0 (2022-09-12)
#### initial version
