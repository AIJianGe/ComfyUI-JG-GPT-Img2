
import os
import json
import hashlib
import requests

CONFIG_FILE_NAME = "jg_config.json"
EXAMPLE_CONFIG_NAME = "jg_config.example.json"


class JGConfigManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if hasattr(self, '_initialized'):
            return
        self._initialized = True
        self.config = {}
        self.plugin_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_dir = os.path.join(self.plugin_dir, "conf")
        self.config_file = os.path.join(self.config_dir, CONFIG_FILE_NAME)
        self.load_config()
    
    def load_config(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
                print(f"[JGConfig] Loaded config from {self.config_file}")
            except Exception as e:
                print(f"[JGConfig] Error loading config: {e}")
                self.config = {}
        else:
            print(f"[JGConfig] Config file not found: {self.config_file}")
            self.config = {}
    
    def save_config(self):
        try:
            # 确保配置目录存在
            if not os.path.exists(self.config_dir):
                os.makedirs(self.config_dir)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
            print(f"[JGConfig] Saved config to {self.config_file}")
        except Exception as e:
            print(f"[JGConfig] Error saving config: {e}")
    
    def get(self, key_path, default=None):
        keys = key_path.split('.')
        value = self.config
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        return value
    
    def set(self, key_path, value):
        keys = key_path.split('.')
        config = self.config
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        config[keys[-1]] = value
        self.save_config()
    
    def get_baidu_config(self):
        return {
            'app_id': self.get('baidu_translate.APP_ID', ''),
            'secret_key': self.get('baidu_translate.SECRET_KEY', ''),
            'timeout': self.get('baidu_translate.timeout', 10)
        }
    
    def get_prompt_optimize_config(self):
        return {
            'api_key': self.get('prompt_optimize.api_key', ''),
            'base_url': self.get('prompt_optimize.base_url', 'https://api.bltcy.ai'),
            'model': self.get('prompt_optimize.model', 'gpt-4o-mini'),
            'timeout': self.get('prompt_optimize.timeout', 30)
        }
    
    def is_baidu_configured(self):
        config = self.get_baidu_config()
        return bool(config['app_id'] and config['secret_key'])
    
    def is_prompt_optimize_configured(self):
        config = self.get_prompt_optimize_config()
        return bool(config['api_key'])


class BaiduTranslator:
    def __init__(self):
        self.config_manager = JGConfigManager()
    
    def translate(self, text, from_lang='auto', to_lang='en'):
        config = self.config_manager.get_baidu_config()
        
        if not config['app_id'] or not config['secret_key']:
            raise ValueError("百度翻译API未配置，请先在 conf/jg_config.json 中配置 APP_ID 和 SECRET_KEY")
        
        url = "https://fanyi-api.baidu.com/api/trans/vip/translate"
        salt = str(int(time.time()))
        sign_str = config['app_id'] + text + salt + config['secret_key']
        sign = hashlib.md5(sign_str.encode('utf-8')).hexdigest()
        
        data = {
            'q': text,
            'from': from_lang,
            'to': to_lang,
            'appid': config['app_id'],
            'salt': salt,
            'sign': sign
        }
        
        try:
            response = requests.post(url, data=data, timeout=config['timeout'])
            response.raise_for_status()
            result = response.json()
            
            if result.get('error_code'):
                raise Exception(f"百度翻译API错误: {result.get('error_msg', '未知错误')}")
            
            translations = result.get('trans_result', [])
            if translations:
                return translations[0].get('dst', text)
            return text
        except Exception as e:
            print(f"[JGTranslator] Translation error: {e}")
            raise


class PromptOptimizer:
    def __init__(self):
        self.config_manager = JGConfigManager()
    
    def optimize(self, prompt):
        config = self.config_manager.get_prompt_optimize_config()
        
        if not config['api_key']:
            raise ValueError("提示词优化API未配置，请先在 conf/jg_config.json 中配置 api_key")
        
        system_prompt = """你是一个专业的图像生成提示词优化专家。你的任务是把用户输入的中文提示词优化为高质量的英文提示词，适合GPT图像生成模型使用。

要求：
1. 将中文翻译成自然、专业的英文
2. 优化提示词结构，使其更符合图像生成模型的要求
3. 添加合适的风格、质量、细节等关键词
4. 保持原意不变，但提升提示词的质量

请直接返回优化后的英文提示词，不要包含其他额外内容。"""
        
        url = f"{config['base_url']}/v1/chat/completions"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {config['api_key']}"
        }
        data = {
            'model': config['model'],
            'messages': [
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': prompt}
            ],
            'temperature': 0.7
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=config['timeout'])
            response.raise_for_status()
            result = response.json()
            
            if 'choices' in result and len(result['choices']) > 0:
                return result['choices'][0]['message']['content'].strip()
            return prompt
        except Exception as e:
            print(f"[JGPromptOptimize] Error: {e}")
            raise


import time


def get_config_manager():
    return JGConfigManager()


def get_translator():
    return BaiduTranslator()


def get_prompt_optimizer():
    return PromptOptimizer()
