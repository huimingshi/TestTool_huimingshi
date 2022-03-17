from Lib.get_tams_response import Get_Tams_Data

EXCEPTIONS_DEMAND_DICT = {
                            'version_213':
                                {'White_list':[],'Black_list':['others']},
                            'version_225':
                                {'White_list':[],'Black_list':['com.google.','others','org.codeaurora.bluetooth.batestapp','com.qualcomm.qti.PresenceApp','com.kiloo.subwaysurf.bd','com.tencent.mm','com.qualcomm.qti.sva']}
                        }

def get_summary_data(task_id):
    summary_data = Get_Tams_Data(task_id).get_summary()
    return summary_data

def get_devices_list(task_id):
    """
    获取单个任务下的device_id列表
    ['BH9500G8JG', 'BH95003LJH', 'BH95002WJH', 'BH9500S7JG', 'BH9500YMJG']
    :param task_id:
    :return: device_id所组成的列表
    """
    summary_data = get_summary_data(task_id)
    devices_list = []
    for one in summary_data['config']['dut_list']:
        devices_list.append(one['DUT'])
    return devices_list

def single_task_devices_data(task_id):
    """
    获取单个任务下所有设备的test_time，pass_case，total_case，testcase_count，pass_rate
    {
        'BH9500G8JG': {
            'test_time': 4.85,      # 执行时长：            4.85h
            'pass_case': 143,       # 测试通过的case数：     143
            'total_case': 161,      # 测试的case总数：      161
            'testcase_count': 18,   # 测试的case个数：      18
            'pass_rate': '88.82%'    # 测试的case通过率：     89%
        },
        'BH95003LJH': {
            'test_time': 5.03,
            'pass_case': 131,
            'total_case': 161,
            'testcase_count': 18,
            'pass_rate': '81.37%'
        },...
    }
    :param task_id:
    :return:返回字典格式，每个键值对都对应device_id和设备的test_time，total_case，pass_rate
    """
    summary_data = get_summary_data(task_id)
    devices_list = get_devices_list(task_id)
    single_task_devices_data_dict = {}
    for device in devices_list:
        device_dict = summary_data['summary'][device]
        test_time = round(float(int(device_dict['test_time']) / 3600), 2)
        pass_case = device_dict['pass']
        total_case = device_dict['total']
        testcase_count = device_dict['testcase_count']
        pass_rate = str(round(float(device_dict['pass_rate'])*100,4)) + '%'
        single_task_devices_data_dict[device] = {'test_time':test_time,'pass_case':pass_case,'total_case':total_case,'testcase_count':testcase_count,'pass_rate':pass_rate}
    return single_task_devices_data_dict

def single_task_devices_total_run_time(task_id):
    """
    获取单个任务下设备总体的运行时长
    :param task_id:
    :return:
    """
    summary_data = get_summary_data(task_id)
    single_task_devices_total_run_time_int = round(float(int(summary_data['summary']['total']['test_time']) / 3600), 2)
    return single_task_devices_total_run_time_int

def single_task_devices_exceptions_summary(task_id,which_version):
    """
    获取单个任务下所有的设备的log_path，package_name
    {
        'BH9500S7JG': {
            'log_path': ['/group1/default/20220113/14/57/3/logcat_20220113145655'],
            'package_name': ['com.sonymobile.launcher+ANR'],
            'filename': ['logcat_20220113145655']
        },
        'BH9500YMJG': {
            'log_path': ['/group1/default/20220113/14/58/3/logcat_20220113145751', '/group1/default/20220113/15/36/3/logcat_20220113153535', '/group1/default/20220113/15/57/3/logcat_20220113155642'],
            'package_name': ['com.sonymobile.launcher+ANR', 'com.sonymobile.launcher+ANR', 'com.sonymobile.launcher+ANR'],
            'filename': ['logcat_20220113145751', 'logcat_20220113153535', 'logcat_20220113155642']
        },...
    }
    :param task_id:
    :param which_version:设备的版本（目前是213和225版本）
    :return:返回字典格式，每个键值对都对应device_id和设备的log_path，exception_type，package_name
    """
    single_task_devices_exceptions_dict = {}
    for device_id in get_devices_list(task_id):
        single_device_exceptions_list = Get_Tams_Data(task_id).get_singel_device_exceptions(device_id)
        log_path_list = []
        filename_list = []
        package_name_list = []
        for single_device_single_exception in single_device_exceptions_list:
            tag_1 = False
            tag_2 = True
            if EXCEPTIONS_DEMAND_DICT[which_version]['White_list'] != []:
                for exception in EXCEPTIONS_DEMAND_DICT[which_version]['White_list']:
                    if exception in single_device_single_exception['package_name']:
                        tag_1 = True
                        break
            elif EXCEPTIONS_DEMAND_DICT[which_version]['White_list'] == []:
                if single_device_single_exception['package_name']:
                    tag_1 = True
            if EXCEPTIONS_DEMAND_DICT[which_version]['Black_list'] != []:
                for exception in EXCEPTIONS_DEMAND_DICT[which_version]['Black_list']:
                    if exception in single_device_single_exception['package_name']:
                        tag_2 = False
                        break
            elif EXCEPTIONS_DEMAND_DICT[which_version]['Black_list'] == []:
                if not single_device_single_exception['package_name']:
                    tag_2 = False
            if tag_1 and tag_2:
                if single_device_single_exception.get("log"):
                    log_index_id = list(single_device_single_exception['log'].keys())[0]
                    log_path_list.append(single_device_single_exception['log'][log_index_id]['path'])
                    filename_list.append(single_device_single_exception['log'][log_index_id]['filename'])
                else:
                    log_path_list.append("")
                    filename_list.append("")
                package_name_list.append(single_device_single_exception['package_name'].strip() + '+' + single_device_single_exception['type'])
        single_task_devices_exceptions_dict[device_id] = {'log_path': log_path_list,
                                                          'package_name': package_name_list,
                                                          'filename': filename_list}
    return single_task_devices_exceptions_dict

if __name__ == '__main__':
    # task_id = '101318'
    task_id = '101744'
    which_version = 'version_213'
    # print(single_task_devices_total_run_time(task_id))
    # print(single_task_devices_exceptions_summary(task_id,witch_version))
    # print(single_task_devices_data(task_id))
    # print(single_task_devices_total_run_time(task_id))
    # print(single_task_devices_data(task_id))
    # print(str(round(float(0.9429)*100,4)) + '%')
    # print(round(float(0.9429),4)*100)
    # print(single_task_devices_total_run_time(task_id))
    # print(single_task_devices_exceptions_summary(task_id, which_version))
    # print(get_devices_list(task_id))
    print(single_task_devices_total_run_time(task_id))