import requests
import heapq
import json
from typing import List
from pydantic import BaseModel, validator


class Device(BaseModel):
    name: str
    type: str
    score: float
    benchmarks: int

    @validator('score', pre=True, always=True)
    def format_float(cls, value):
        return round(value, 2)

class DeviceList(BaseModel):
    devicesCount: int
    devices: List[Device]


class DeviceTypes(BaseModel):
    types: List[str]


url = "https://opendata.blender.org/benchmarks/query/?group_by=device_name&group_by=compute_type&response_type=datatables"


def format_devices(devices):
    formated_devices = []
    for device in devices:
        formated_devices.append(
            Device(
                name=device[0],
                type=device[1],
                score=device[2],
                benchmarks=device[3],
            )
        )
    return formated_devices


def filter_devices_types(devices):
    filtered_types = []
    for device in devices:
        if device[1] not in filtered_types:
            filtered_types.append(device[1])
    return filtered_types


def filter_gpus(devices):
    gpus = []
    for device in devices:
        if device[1] != "CPU":
            gpus.append(
                Device(
                    name=device[0],
                    type=device[1],
                    score=device[2],
                    benchmarks=device[3],
                )
            )
    return gpus


def filter_cpus(devices):
    cpus = []
    for device in devices:
        if device[1] == "CPU":
            cpus.append(
                Device(
                    name=device[0],
                    type=device[1],
                    score=device[2],
                    benchmarks=device[3],
                )
            )
    return cpus


def filter_top_devices(devices):
    filtered_objects = format_devices(devices)
    return heapq.nlargest(10, filtered_objects, key=lambda obj: obj.score)


def get_all_devices() -> DeviceList:
    response = requests.get(url)
    formated_devices = format_devices(json.loads(response.text)["rows"])
    return DeviceList(
        devicesCount=len(formated_devices),
        devices=formated_devices,
    )


def get_gpus_devices() -> DeviceList:
    response = requests.get(url)
    gpus_list = filter_gpus(json.loads(response.text)["rows"])
    return DeviceList(
        devicesCount=len(gpus_list),
        devices=gpus_list,
    )


def get_cpus_devices() -> DeviceList:
    response = requests.get(url)
    cpus_list = filter_cpus(json.loads(response.text)["rows"])
    return DeviceList(
        devicesCount=len(cpus_list),
        devices=cpus_list,
    )


def get_top_all_devices() -> DeviceList:
    response = requests.get(url)
    topList = filter_top_devices(json.loads(response.text)["rows"])
    return DeviceList(devicesCount=10, devices=topList)


def get_device_types() -> DeviceTypes:
    response = requests.get(url)
    deviceTypes = filter_devices_types(json.loads(response.text)["rows"])
    return DeviceTypes(types=deviceTypes)
