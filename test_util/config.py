import yaml
from pathlib import Path

# Specify the file to read to get the settings
JIRA_YML = Path(__file__).parents[1]/'local.yaml'


def read_yml_file(file):
    with file.open(mode='r') as file:
        return yaml.load(file, Loader=yaml.FullLoader)


class AppSettings:

    def __init__(self, config_yml):

        obj = read_yml_file(config_yml)
        env_settings = obj['settings']['env']
        # Environments
        self.username = env_settings['username']
        self.password = env_settings['password']
        self.webdriver_visible = env_settings['webdriver_visible']


TEST_ENV = AppSettings(config_yml=JIRA_YML)
