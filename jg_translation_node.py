
import os
import json
import hashlib
import requests
import time

from .jg_config_manager import get_config_manager, get_translator, get_prompt_optimizer


class JiangePromptTranslationNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_text": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "placeholder": "输入要翻译或优化的提示词..."
                }),
                "operation": (["translate", "optimize", "both"], {
                    "default": "translate",
                    "tooltip": "翻译中文到英文 / 优化提示词 / 两者都做"
                })
            }
        }

    @classmethod
    def VALIDATE_INPUTS(cls, **kwargs):
        return True

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("output_text",)
    FUNCTION = "process"
    CATEGORY = "AI剑歌/🤖GPT-Image-2"
    DESCRIPTION = "翻译和优化提示词 @AI剑歌"
    
    def __init__(self):
        self.config_manager = get_config_manager()
    
    def process(self, input_text, operation):
        if not input_text:
            return ("",)
        
        result_text = input_text
        
        try:
            if operation in ["translate", "both"]:
                translator = get_translator()
                try:
                    result_text = translator.translate(result_text)
                    print(f"[JGTranslation] Translated: {result_text}")
                except Exception as e:
                    print(f"[JGTranslation] Translation warning: {e}")
                    # 如果翻译失败，不中断，继续用原文
            
            if operation in ["optimize", "both"]:
                optimizer = get_prompt_optimizer()
                try:
                    result_text = optimizer.optimize(result_text)
                    print(f"[JGTranslation] Optimized: {result_text}")
                except Exception as e:
                    print(f"[JGTranslation] Optimization warning: {e}")
            
        except Exception as e:
            print(f"[JGTranslation] Error: {e}")
            result_text = input_text
        
        return (result_text,)


class JiangeConfigNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "set_config": (["show_help"], {
                    "default": "show_help",
                    "tooltip": "查看配置说明"
                })
            },
            "optional": {
                "baidu_app_id": ("STRING", {
                    "default": "",
                    "placeholder": "百度翻译 APP_ID"
                }),
                "baidu_secret_key": ("STRING", {
                    "default": "",
                    "placeholder": "百度翻译 SECRET_KEY"
                }),
                "prompt_api_key": ("STRING", {
                    "default": "",
                    "placeholder": "提示词优化 API Key"
                })
            }
        }

    @classmethod
    def VALIDATE_INPUTS(cls, **kwargs):
        return True

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("config_status",)
    FUNCTION = "show_config"
    CATEGORY = "AI剑歌/🤖GPT-Image-2"
    DESCRIPTION = "配置管理 @AI剑歌"
    
    def __init__(self):
        self.config_manager = get_config_manager()
    
    def show_config(self, set_config, baidu_app_id="", baidu_secret_key="", prompt_api_key=""):
        status_lines = []
        status_lines.append("=== JG GPT Image 2 配置说明 ===")
        status_lines.append("")
        status_lines.append("1. 复制 conf/jg_config.example.json 为 conf/jg_config.json")
        status_lines.append("2. 在 conf/jg_config.json 中填入你的 API 密钥")
        status_lines.append("")
        status_lines.append("百度翻译 API 获取：https://fanyi-api.baidu.com/")
        status_lines.append("GPT API Key 获取：可使用柏拉图 API 等")
        status_lines.append("")
        status_lines.append("配置检查：")
        
        baidu_ok = self.config_manager.is_baidu_configured()
        status_lines.append(f"百度翻译：{'✅ 已配置' if baidu_ok else '❌ 未配置'}")
        
        prompt_ok = self.config_manager.is_prompt_optimize_configured()
        status_lines.append(f"提示词优化：{'✅ 已配置' if prompt_ok else '❌ 未配置'}")
        
        return ("\n".join(status_lines),)


NODE_CLASS_MAPPINGS = {
    "Jiange_Prompt_Translation": JiangePromptTranslationNode,
    "Jiange_Config": JiangeConfigNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Jiange_Prompt_Translation": "⚔️ 提示词翻译/优化",
    "Jiange_Config": "⚔️ 配置管理"
}
