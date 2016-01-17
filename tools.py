# -*- encoding:"utf-8"-*-
# coding=utf-8



def getSensorList(filename):
    """
    返回有序的传感器列表
    :param filename:
    :return:
    """
    sensor_list = []
    with open(filename, 'r') as fr:
        for line in fr:
            row = line.split()
            sensor_id = row[2]
            if sensor_id not in sensor_list:
                sensor_list.append(sensor_id)
    return sorted(sensor_list)
