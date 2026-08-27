import csv
from wsgiref.validate import validator

devices = []
def is_valid_ip(ip_str):
    ip_str=ip_str.strip()
    ip=ip_str.split('.')
    if len(ip)!=4:
        return False
    for i in ip:
        if i==" ":
            return False
        if not i.isdigit():
            return False
        num=int(i)
        if num<0 or num>255:
            return False
    return True
def is_valid_status(status):
    return status=="在线" or status=="离线"
def is_valid_name(name):
    return name.strip()!=""
def get_valid_input(prompt,validator,error_msg="输入无效请重新输入"):
    while True:
        user_input=input(prompt)
        if validator(user_input):
            return user_input
        print(error_msg)


def list_devices(devices):
    if len(devices)==0:
        print("当前未有设备，请添加")
        return
    print("当前设备清单：")
    for i,device in enumerate(devices,1):
            print(f"{i}. {device['name']:10} | {device['ip']:15} | {device['type']:8} | {device['status']}")
    return


def add_devices(devices):
    name=get_valid_input("请输入设备名称：",is_valid_name,"设备名不能为空，请重新输入")
    ip = get_valid_input("请输入设备ip地址：",is_valid_ip,"ip地址格式错误，正确格式如（192.168.1.1）")
    typ = get_valid_input("请输入设备类型：",is_valid_name,"设备类型不能为空，请重新输入")
    status = get_valid_input("请输入状态（在线/离线）：",is_valid_status,"状态只能输入“在线”或者“离线”")
    device = {"name":name,
              "ip":ip,
              "type":typ,
              "status":status
              }
    devices.append(device)
    print(f"设备{name}已添加")


def delete_device(devices):
    list_devices(devices)
    name=input("请输入要删除的设备名称")
    for device in devices:
        if name=="":
            print("删除的设备名不能为空，请重新输入")
            return
        if device["name"] == name:
            devices.remove(device)  # 删除字典
            print(f"设备 '{name}' 已删除")
            return
    print("未找到该设备")


def update_devices(devices):
    list_devices(devices)
    new_name=input("请输入要修改的设备名:")
    for device in devices:
        if new_name==device["name"]:
            new_ip=input("请输入要修改的新ip(直接回车不修改)：")
            if new_ip!="":
                while not is_valid_ip(new_ip):
                    print("IP 地址格式错误，正确格式如 192.168.1.1")
                    new_ip = input("请输入要修改的新ip(直接回车不修改)：")
                    if new_ip=="":
                        device["ip"]=new_ip
                if new_ip!="":
                    device["ip"]=new_ip
                new_type=input("请输入要修改的新类型：")
                if new_type=="":
                    device["type"] = new_type
                if new_type != "":
                    device["type"] = new_type
                new_status = input("请输入要修改的新状态：")
                while not is_valid_status(new_status):
                    if new_status!="":
                        print("状态只能输入：在线 或 离线")
                        new_status = input("请输入要修改的新状态：")
                    if new_status=="":
                        device["type"] = new_type
                if new_status!="":
                    device["status"] = new_status
            print("修改成功")
            return
    print("要修改的该设备不存在")



def save_to_file(devices,filename="devices.csv"):
    with open(filename,"w",newline="",encoding="utf-8") as f:
        fieldnames=["name","ip","type","status"]
        writer=csv.DictWriter(f,fieldnames=fieldnames)
        writer.writeheader()
        for device in devices:
            writer.writerow(device)
    print("设备清单已保存到文件")



def import_interfaces_from_config(config):
    devices=[]
    lines=config.split("\n")
    for line in lines:
        line=line.strip()
        if line.startswith("interface "):
            name=line.replace("interface ","")
            device={
                        "name":name,
                        "ip":"未分配",
                        "type":"接口",
                        "status":"在线"
                    }
            devices.append(device)
    return devices



def load_from_file(filename="devices.csv"):
    devices=[]
    try:
        with open(filename,"r",encoding="utf-8") as f:
            reader=csv.DictReader(f)
            for row in reader:
                devices.append(row)
    except FileNotFoundError:
        pass
    return devices



def main_menu():
    devices=load_from_file()

    while True:
        print("欢迎使用网络设备管理器")
        print('='*30)
        print(f"1.查看所有设备")
        print(f"2.添加设备")
        print(f"3.删除设备")
        print(f"4.修改设备")
        print(f"5.导入Cisco配置")
        print(f"6.退出")
        print('='*30)
        chioe=input("请选择操作（1-6）:")
        if chioe=="1":
            list_devices(devices)
        elif chioe == "2":
            add_devices(devices)
            save_to_file(devices)
        elif chioe == "3":
            delete_device(devices)
            save_to_file(devices)
        elif chioe == "4":
            update_devices(devices)
            save_to_file(devices)
        elif chioe=="5":
            print("请粘贴Cisco配置文件（输入空行结束）")
            config_lines=[]
            while True:
                line=input()
                if line=="":
                    break
                config_lines.append(line)
            config='\n'.join(config_lines)
            imported=import_interfaces_from_config(config)
            devices.extend(imported)
            save_to_file(devices)
            print(f"已导入{len(imported)}台设备")
            save_to_file(devices)
        elif chioe == "6":
            save_to_file(devices)
            print("再见!")
            break
        else:
            print("输入错误,请重新选择")

main_menu()






