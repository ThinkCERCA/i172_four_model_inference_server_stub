from __future__ import annotations
import os
from configparser import RawConfigParser
from swa_lib import WORK_DIR
from swa_lib.log import log


class ModelConfig:
    def __init__(self, opt_dict: dict):
        self.name: str = opt_dict['name']
        self.full_name: str = opt_dict.get('full_name', self.name)
        self.path: str = opt_dict['path']
        self.type: str = opt_dict['type']
        self.default: bool = opt_dict.get('default', 'no')[0].lower() == 'y'
        self.results = opt_dict.get('results', 'SUCCESS|FAIL').split('|')
        self.seqn: int = int(opt_dict['seqn'])


class SWAConfigParser:
    def __init__(self, init: bool = True):
        """Initialize config object from config_file

        :param init: bool. False if empty object initialization.
        """
        # empty object initialization
        if not init:
            return
        error_msg = ''
        try:
            # parse config/config.ini
            error_msg = 'parsing config.ini'
            main_config_filename = os.path.join(WORK_DIR, 'configs', 'config.ini')
            config_parser = RawConfigParser(allow_no_value=True)
            config_parser.read(main_config_filename)
            self.all_cfg = self.convert_to_dict(config_parser)
            self.models = [ModelConfig(self.all_cfg[x]) for x in self.all_cfg if x.startswith('model_')]
            self.models.sort(key=lambda x: x.seqn)
        except Exception:
            log('error', 'Config initialization error at %s.' % error_msg)
            exit(-1)

    @staticmethod
    def convert_to_dict(cfg_parser: RawConfigParser):
        """
        Convert RawConfigParser to dict.
        Extract values in " and ' quotes.

        :param cfg_parser: RawConfigParser
        :return: dict
        """
        def parse_quotes(s_dict: dict):
            """Extract quoted dict values"""
            result_dict = dict()
            for k, v in s_dict.items():
                if v:
                    v = v.strip()
                if v:
                    for quote_char in ('"', "'"):
                        if (len(v) > 2) and (v[0] == v[-1] == quote_char):
                            v = v[1:-1]
                            break
                result_dict[k] = v
            return result_dict
        # convert RawConfigParser to dict {section: {key: value, ...}, ...}
        cfg_dict = {s: parse_quotes(dict(cfg_parser.items(s))) for s in cfg_parser.sections()}
        return cfg_dict

    def get_value(self, section: str, opt_name: str, default_value=None, opt_type: type = str):
        """
        Get config value.

        :param section: str
        :param opt_name: str
        :param default_value: various
        :param opt_type: object
        :return: various
        """
        value = self.all_cfg.get(section, dict()).get(opt_name)
        if value is None:
            return default_value
        return opt_type(value)

    def get_yes_no_value(self, section: str, opt_name: str, default_value: bool = False) -> bool:
        """
        Get "yes"/"no" config value as boolean.

        :param section: str
        :param opt_name: str
        :param default_value: bool
        :return: bool
        """
        opt_name = opt_name.lower()
        if opt_name in self.all_cfg.get(section, dict()):
            return str(self.all_cfg[section][opt_name])[0].lower() == 'y'
        return default_value


configuration = SWAConfigParser(init=False)
