# 第三部分：串口相关代码
# 这部分代码主要涉及串口设备的查找、配置以及数据发送操作。
# 首先通过serial.tools.list_ports.comports()获取所有串口设备实例，并根据获取到的设备列表情况进行输出：如果没有找到串口设备，则输出“无串口设备。”；如果找到串口设备，则依次输出每个设备对应的串口号和描述信息。
# 然后打开串口号为COM3的串口设备，并将波特率配置为115200，创建了一个serial.Serial对象ser。
# 最后进入一个无限循环，每隔 1 秒向串口发送一次数据。先发送字符串"1\r\n"，再发送字符串"2\r\n"，每次发送前将字符串编码为gbk格式。这里原本还有读取串口数据以及关闭串口的逻辑，但部分被注释掉了，目前主要功能是向串口发送特定数据。
import time
import serial
import serial.tools.list_ports

# 获取所有串口设备实例。
# 如果没找到串口设备，则输出：“无串口设备。”
# 如果找到串口设备，则依次输出每个设备对应的串口号和描述信息。
ports_list = list(serial.tools.list_ports.comports())
if len(ports_list) <= 0:
    print("无串口设备。")
else:
    print("可用的串口设备如下：")
    for comport in ports_list:
        print(list(comport)[0], list(comport)[1])


# 打开 COM3，将波特率配置为115200.
ser = serial.Serial(port="COM3", baudrate=115200)

# 串口发送 ABCDEFG，并输出发送的字节数。
while True:
    ser.write("1\r\n".encode("gbk"))
    time.sleep(1)
    ser.write("2\r\n".encode("gbk"))
    time.sleep(1)

# print("串口发出{}个字节。".format(write_len))
# com_input = ser.read(100)
# if com_input:  # 如果读取结果非空，则输出
#     print('接受字符:', com_input)

# ser.close()
