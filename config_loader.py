import utils


class ConfigLoader:
    def __init__(self):
        self.rule_file_path = 'conf/rule.toml'
        self.rule = utils.toml_load(self.rule_file_path)


config_loader = ConfigLoader()


if __name__ == '__main__':
    print(config_loader.rule)
