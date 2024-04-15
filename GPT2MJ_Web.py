from openai import OpenAI
import requests
import sys
import os
import time
import json

client = OpenAI(
    api_key="sk-OHic8IBf9orqjXxzrGm14f2jaOGEYfN2K0TUlq4jw10vABtC",
    base_url="https://api.chatanywhere.tech/v1"
)

XAPIKEY = "605d1a71632970eb5f3d145c7b53a0d710cf7acfd10210bf37c10305197cf84f"

headers = {
    "X-API-KEY": XAPIKEY
}

Data = {
        "code": 200,
        "origin_prompt": "prompt",
        "new_prompt": "",
        "img1": "",
        "img2": "",
        "img3": "",
        "img4": "",
        "err_info": ""
    }

def chat(messages: list):
    completion = client.chat.completions.create(model="gpt-4", messages=messages)
    return completion.choices[0].message.content


def imagine(prompt):
    data = {
        "prompt": prompt,
        "aspect_ratio": "4:3",
        "process_mode": "fast",
        "webhook_endpoint": "",
        "webhook_secret": ""
    }
    endpoint = "https://api.midjourneyapi.xyz/mj/v2/imagine"
    response = requests.post(endpoint, headers=headers, json=data)
    Data["code"] = response.status_code
    Data["err_info"] = str(response.json())
    if response.status_code == 200 and (str(response.json()).find("success") != -1 or str(response.json()).find("finished") != -1):
        pos = str(response.json()).index("task_id") + 11
        endpos = str(response.json()).index("', 'success'")
        return str(response.json())[pos: endpos]
    else:
        return ""


def upscale(taskId, index):
    data = {
        "origin_task_id": taskId,
        "index": str(index),
        "webhook_endpoint": "",
        "webhook_secret": ""
    }
    endpoint = "https://api.midjourneyapi.xyz/mj/v2/upscale"
    cnt = 0
    while cnt < 20:
        if cnt == 0 and index == 1:
            time.sleep(30)
        else:
            time.sleep(5)
        cnt += 1
        response = requests.post(endpoint, headers=headers, json=data)
        Data["code"] = response.status_code
        Data["err_info"] = str(response.json())
        if response.status_code == 200 and (str(response.json()).find("success") != -1 or str(response.json()).find("finished") != -1):
            print(response.status_code)
            print(response.json())
            pos = str(response.json()).index("task_id") + 11
            endpos = str(response.json()).index("', 'success'")
            return str(response.json())[pos: endpos]
    return ""


def fetch(taskId):
    data = {
        "task_id": taskId
    }
    endpoint = "https://api.midjourneyapi.xyz/mj/v2/fetch"
    cnt = 0
    while cnt < 20:
        if cnt == 0:
            time.sleep(30)
        else:
            time.sleep(5)
        cnt += 1
        response = requests.post(endpoint, json=data)
        Data["code"] = response.status_code
        Data["err_info"] = str(response.json())
        if response.status_code == 200 and (str(response.json()).find("success") != -1 or str(response.json()).find("finished") != -1):
            pos = str(response.json()).index("https://img.midjourneyapi.xyz/mj/")
            endpos = str(response.json()).index("', 'image_urls'")
            print(str(response.json())[pos: endpos])
            return str(response.json())[pos: endpos]
    return ""


def work(prompt):
    messages = [{'role': 'user', 'content': 'I want to generate an image in MidJourney using the following paragraph as a description, please give the prompt in English that applies to MidJourney:' + prompt}, ]
    reply = chat(messages)
    if reply[0] == '\"' and reply[len(reply) - 1] == '\"':
        reply = reply[1:-1]
    Data["new_prompt"] = reply
    taskId = imagine(reply)
    if (Data["code"] != 200):
        return Data

    i = 1
    while i <= 4:
        Data["img" + str(i)] = fetch(upscale(taskId, i))
        if (Data["code"] != 200):
            break
        i += 1

    return Data


def run(prompt):
    while prompt[len(prompt) - 1] == '\n':
        prompt = prompt[0:-1]

    return work(prompt)
