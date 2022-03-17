import os
import configparser

# 获取配置文件的绝对路径
import sys

config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'config','config.ini')
# # Pyinstaller 之后需要根据执行路径去获取ini文件路径
# config_path = os.path.join(os.path.dirname(sys.argv[0]), "config", "config.ini")


def parse_config(section,config_path):
    """
    解析配置文件
    :param section:
    :param config_path:
    :return: configparser.SectionProxy
    """
    config = configparser.ConfigParser()   # 实例化
    config.read(config_path)
    if not config.has_section(section):
        # 如果没有这个section就抛出异常
        raise KeyError(f'This section "{section}" does not exist in the file')
    return config[section]

if __name__ == '__main__':
    # print(parse_config('tams',config_path),type(parse_config('tams',config_path)))
    # orgList = [1, 0, 3, 7, 7, 5]
    # # list()方法是把字符串str或元组转成数组
    # print(set(orgList))
    list = ['11+ANR','22+APP_CRASH']
    for one in list:
        print(one.split('+')[-1])