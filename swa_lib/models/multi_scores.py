from __future__ import annotations
from functools import lru_cache
import json
from swa_lib import WORK_DIR
from swa_lib.errors import Errors
from swa_lib.configs import ModelConfig
from transformers import BertTokenizerFast, BertForSequenceClassification
import torch


class ModelMultiScores:
    def __init__(self, model_cfg: ModelConfig):
        self.model_cfg = model_cfg
        full_dir_path = WORK_DIR / 'models' / model_cfg.path
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.tokenizer = BertTokenizerFast.from_pretrained(full_dir_path)
        self.model = BertForSequenceClassification.from_pretrained(full_dir_path)
        self.model.to(self.device)
        self.model.eval()
        self._predict_one('Some sentence to test model and get results.')

    @lru_cache(maxsize=100)
    def _predict_one(self, content, threshold=.5):
        inputs = self.tokenizer(content,
                                padding='max_length',
                                truncation=True, return_tensors="pt")
        # move to gpu
        ids = inputs["input_ids"].to(self.device)
        idt = inputs["token_type_ids"].to(self.device)
        mask = inputs["attention_mask"].to(self.device)
        # forward pass
        outputs = self.model(ids, token_type_ids=idt, attention_mask=mask)
        logits = outputs[0]
        sigmoid = torch.nn.Sigmoid()
        probs = sigmoid(torch.Tensor(logits))
        flattened_predictions = probs.cpu().detach().numpy()[0]
        label = {'Claim': [], 'Evidence': [], 'Reasoning': []}
        if flattened_predictions[0] > threshold:
            label['Claim'] = [1, float(flattened_predictions[0])]
        elif flattened_predictions[0] <= threshold:
            label['Claim'] = [0, float(flattened_predictions[0])]
        if flattened_predictions[1] > threshold:
            label['Evidence'] = [1, float(flattened_predictions[1])]
        elif flattened_predictions[1] <= threshold:
            label['Evidence'] = [0, float(flattened_predictions[1])]
        if flattened_predictions[2] > threshold:
            label['Reasoning'] = [1, float(flattened_predictions[2])]
        elif flattened_predictions[2] <= threshold:
            label['Reasoning'] = [0, float(flattened_predictions[2])]
        return label

    def predict(self, opt_dict: dict) -> dict:
        content: str | None = opt_dict.get('content')
        try:
            content_list: list[str] | str = opt_dict.get('content_list', '[]')
            if type(content_list) == str:
                content_list = json.loads(content_list)
        except Exception:
            return Errors.NO_CONTENT
        if not (content or content_list):
            return Errors.NO_CONTENT
        if content:
            return self._predict_one(content)
        # content list
        result_list = []
        for content in content_list:
            if not content.strip():
                result_list.append(Errors.NO_CONTENT)
                continue
            result_list.append(self._predict_one(content))
        return {'result_list': result_list}
