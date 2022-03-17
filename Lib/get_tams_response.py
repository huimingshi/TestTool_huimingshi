import sys

import requests
import json

HOST = 'http://tams.thundersoft.com/'


class Get_Tams_Data(object):
    def __init__(self,task_id):
        self.task_id = task_id
        self.devices_list = []

    def get_summary(self):
        """
        获取总体数据接口的返回体
        :return:
        """
        url = HOST + f'api/result/get/{self.task_id}'
        response = requests.get(url)
        res_dict = json.loads(response.text)
        if res_dict['code'] != 200:
            print('获取任务总体数据的接口报错')
        return res_dict

    def get_singel_device_exceptions(self,device_id):
        """
        # 获取单个设备下的log_path，exception_type，package_name
        获取单台设备下获取异常的接口的返回体
        :param device_id:
        :return:
        """
        url = HOST + f'api/result/get_exception/{self.task_id}/{device_id}?page=1&limit=10000'
        response = requests.get(url)
        res_dict = json.loads(response.text)
        if res_dict['code'] != 200 and res_dict['code'] != 404:
            print(f'{self.task_id}下{device_id}获取单台设备的异常总数据的接口报错')
            sys.exit(1)
        elif res_dict['code'] == 404:
            single_device_exceptions_list = [{"log":
                                                  {"456e3ec09d2e4f2cae651abe76d656b3":
                                                       {"md5": "",
                                                        "path": "",
                                                        "size": "",
                                                        "filename": "",
                                                        "hex_code": ""}},
                                              "type": "",
                                              "uuid": "",
                                              "index": 0,
                                              "details": "",
                                              "case_name": "",
                                              "device_id": f"{device_id}",
                                              "happen_time": "",
                                              "package_name": ""}]
            return single_device_exceptions_list
        else:
            single_device_exceptions_list = res_dict['exceptions']
            return single_device_exceptions_list

if __name__ == '__main__':
    task_id = '101318'
    print(Get_Tams_Data(task_id).get_singel_device_exceptions())