import json
import settings


class ConfigManager:

    @staticmethod
    def set_config(data: dict):
        with open(settings.CONFIG_PATH, 'w') as file:
            json.dump(data, file)
    
    @staticmethod
    def get_config() -> dict:
        with open(settings.CONFIG_PATH, 'r') as file:
            return json.load(file)