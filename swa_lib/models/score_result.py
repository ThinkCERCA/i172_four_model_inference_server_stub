from __future__ import annotations
import json
from functools import lru_cache
from swa_lib import WORK_DIR
from swa_lib.errors import Errors
from swa_lib.configs import ModelConfig
from transformers import XLNetTokenizer, XLNetForSequenceClassification
import torch
import torch.nn.functional as functional


class ModelScoreResult:
    def __init__(self, model_cfg: ModelConfig):
        self.model_cfg = model_cfg
        self.result_success, self.result_fail = self.model_cfg.results
        full_dir_path = WORK_DIR / 'models' / model_cfg.path
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.tokenizer = XLNetTokenizer.from_pretrained(full_dir_path)
        self.model = XLNetForSequenceClassification.from_pretrained(full_dir_path)
        self.model.to(self.device)
        self.model.eval()
        self._predict_one('Some sentence to test model and get results.')

    @lru_cache(maxsize=100)
    def _predict_one(self, content: str) -> (float, str):
        inputs = self.tokenizer(content, padding='max_length', truncation=True, return_tensors="pt")
        # move to gpu
        ids = inputs["input_ids"].to(self.device)
        idt = inputs["token_type_ids"].to(self.device)
        mask = inputs["attention_mask"].to(self.device)
        # forward pass
        outputs = self.model(ids, token_type_ids=idt, attention_mask=mask)
        logits = outputs[0]
        x = functional.softmax(logits, dim=-1)
        active_logits = logits.view(-1, self.model.num_labels)  # shape (batch_size * seq_len, num_labels)
        flattened_predictions = torch.argmax(active_logits, dim=1)
        score = float(x.cpu().detach().numpy()[0][1])
        label = self.result_success if (flattened_predictions.cpu().numpy()[0] == 1) else self.result_fail
        return score, label

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
            prob, label = self._predict_one(content)
            return {'result': label, 'score': prob}
        # content list
        result_list = []
        for content in content_list:
            if not content.strip():
                result_list.append(Errors.NO_CONTENT)
                continue
            prob, label = self._predict_one(content)
            result_list.append({'result': label, 'score': prob})
        return {'result_list': result_list}
