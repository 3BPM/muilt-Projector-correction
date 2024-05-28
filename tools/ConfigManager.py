import json
import os

class ConfigManager:
    def __init__(self, filename='config.json'):
        self.filename = filename

    def add_config(self, projector_id, cam_size, sizewh, capture_dir):
        config = {
            'cam_size': cam_size,
            'pro_size': sizewh,
            'capture_dir': capture_dir,
        }

        # 如果配置文件存在，读取现有内容
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                configs = json.load(f)
        else:
            configs = {}

        # 添加新的配置
        configs[projector_id] = config

        # 写回配置文件
        with open(self.filename, 'w') as f:
            json.dump(configs, f, indent=4)

    def clear_configs(self):
        # 将空字典写入配置文件
        with open(self.filename, 'w') as f:
            json.dump({}, f, indent=4)

    def load_configs(self):
        # 检查配置文件是否存在
        if not os.path.exists(self.filename):
            return {}

        # 读取并解析配置文件
        with open(self.filename, 'r') as f:
            configs = json.load(f)

        return configs

    def get_config(self, projector_id):
        configs = self.load_configs()
        return configs.get(projector_id)

    def delete_config(self, projector_id):
        configs = self.load_configs()
        if projector_id in configs:
            del configs[projector_id]
            with open(self.filename, 'w') as f:
                json.dump(configs, f, indent=4)


# 示例用法
if __name__ == "__main__":

    c = ConfigManager()
    # 添加配置
    c.add_config('projector_1', 'cam_size_1', screen, 'capture_dir_1')
    c.add_config('projector_2', 'cam_size_2', screen, 'capture_dir_2')

    # 加载所有配置
    configs = c.load_configs()
    print("Loaded configs:", configs)

    # 获取特定配置
    config = c.get_config('projector_1')
    print("Config for projector_1:", config)

    # 删除特定配置
    c.delete_config('projector_1')
    print("Configs after deleting projector_1:", c.load_configs())

    # 清空所有配置
    c.clear_configs()
    print("Configs after clearing:", c.load_configs())
