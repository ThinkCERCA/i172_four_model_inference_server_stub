from __future__ import annotations
from swa_lib.configs import SWAConfigParser
from swa_lib.log import log
from swa_lib.errors import Errors
from swa_lib.models.score_result import ModelScoreResult
from swa_lib.models.multi_scores import ModelMultiScores


class Models:
    model_type__class = {
        'score_result': ModelScoreResult,
        'multi_scores': ModelMultiScores
    }

    def __init__(self, configuration: SWAConfigParser | None = None):
        if not configuration:
            return
        self.c = configuration
        self.models: dict[str, ModelScoreResult | ModelMultiScores] = dict()
        self.default_model_name = ''
        self._init_all_models()

    def _init_all_models(self):
        log.info('Initializing models...')
        model_cfg_list = self.c.models
        if not model_cfg_list:
            log.error('No models found')
            exit(-1)
        for model_cfg in model_cfg_list:
            log.info(f"Initializing model: {model_cfg.full_name} / {model_cfg.name} / {model_cfg.type}")
            if not (model_class := self.model_type__class.get(model_cfg.type)):
                log.error(f'No model type found: ${model_cfg.type=}')
                exit(-1)
            self.models[model_cfg.name] = model_class(model_cfg)
            if model_cfg.default:
                self.default_model_name = model_cfg.name
        if not self.default_model_name:
            self.default_model_name = self.models[list(self.models.keys())[0]]

    def predict(self, opt_dict: dict) -> dict:
        model_name = opt_dict.get('model', self.default_model_name)
        if not (model_obj := self.models.get(model_name)):
            return Errors.WRONG_MODEL_NAME
        return model_obj.predict(opt_dict)


models = Models()
