#!/usr/bin/python
# -*- coding: utf-8 -*-

import PySimpleGUI as sg
import yaml
import subprocess
import time
import threading

sg.theme("Default")


def save_config(filename, config_data):
    with open(filename, "w") as f:
        yaml.dump(config_data, f)


def load_config(filename):
    with open(filename, "r") as f:
        config_data = yaml.safe_load(f)
    return config_data


loaded_configs = []

layout = [
    [sg.Text("Target:")],
    [
        sg.Text("IP: "),
        sg.InputText(size=20, key="IP"),
        sg.Text("Port: "),
        sg.InputText(size=20, key="port"),
    ],
    [
        sg.Text("Attack"),
        sg.Text(" Enabled"),
        sg.Text("Keep-Alive"),
        sg.Text("Duration"),
        sg.Text("Message Count"),
        sg.Text("Processes"),
        sg.Text("Message Size"),
        sg.Text("Username"),
        sg.Text("Wordlist"),
    ],
    [
        sg.Text("SlowDoS"),
        sg.Checkbox("", key="slowdos_enabled"),
        sg.InputText(size=6, key="slowdos_keepalive"),
        sg.InputText(size=6, key="slowdos_duration"),
    ],
    [
        sg.Text("Malaria"),
        sg.Checkbox("", key="malaria_enabled"),
        sg.InputText(size=6, key="malaria_message_count"),
        sg.InputText(size=6, key="malaria_processes"),
        sg.InputText(size=6, key="malaria_message_size"),
    ],
    [
        sg.Text("Brute Force"),
        sg.Checkbox("", key="bruteforce_enabled"),
        sg.InputText(size=20, key="bruteforce_username"),
        sg.InputText(size=20, key="bruteforce_wordlist"),
    ],
    [sg.Text("Malformed"), sg.Checkbox("", key="malformed_enabled")],
    [
        sg.Combo(
            values=loaded_configs,
            size=(40, 1),
            key="loaded_configs_dropdown",
            readonly=True,
            enable_events=True,
        ),
        sg.Button("Load from Dropdown", key="LoadFromDropdown"),
    ],
    [
        sg.Button("Save"),
        sg.Button("RUN"),
        sg.Button("Load"),
        sg.Button("Exit", key="bExit"),
    ],
    [sg.Text(key="msg", size=(40, 1))],
]

window = sg.Window("MQTT Attack generator", layout)

def execute_attack(operation, window):
    mode = operation['mode']

    if mode == 'slowdos':
        sg.OneLineProgressMeter('Attack Progress', 1, 4, 'slowdos', 'Running SlowDoS attack...')
        # [SlowDoS attack code]
        sg.OneLineProgressMeter('Attack Progress', 2, 4, 'slowdos')

    elif mode == 'malaria':
        sg.OneLineProgressMeter('Attack Progress', 2, 4, 'malaria', 'Running Malaria attack...')
        # [Malaria attack code]
        sg.OneLineProgressMeter('Attack Progress', 3, 4, 'malaria')

    elif mode == 'bruteforce':
        sg.OneLineProgressMeter('Attack Progress', 3, 4, 'bruteforce', 'Running Brute Force attack...')
        # [Bruteforce attack code]
        sg.OneLineProgressMeter('Attack Progress', 4, 4, 'bruteforce')

    elif mode == 'malformed':
        sg.OneLineProgressMeter('Attack Progress', 4, 4, 'malformed', 'Running Malformed attack...')
        # [Malformed attack code]


while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == "bExit":
        break

    if event == "Save":
        config_data = {"scriptConfigurations": []}

        if values["slowdos_enabled"]:
            slowdos_data = {
                "mode": "slowdos",
                "slow_dos_path": "/home/jishnusen/Desktop/mqtt/MQTT_SlowITe/MQTT_attack_slowITe/MQTT_SlowDoS.py",
                "address": values["IP"],
                "port": int(values["port"]),
                "keep_alive": int(values["slowdos_keepalive"]),
                "time": int(values["slowdos_duration"]),
            }
            config_data["scriptConfigurations"].append(slowdos_data)

        if values["malaria_enabled"]:
            malaria_data = {
                "mode": "malaria",
                "malaria_path": "",
                "address": values["IP"],
                "port": int(values["port"]),
                "message_count": int(values["malaria_message_count"]),
                "processes": int(values["malaria_processes"]),
                "message_size": int(values["malaria_message_size"]),
            }
            config_data["scriptConfigurations"].append(malaria_data)

        if values["bruteforce_enabled"]:
            bruteforce_data = {
                "mode": "bruteforce",
                "mqttsa_path": "/home/jishnusen/Desktop/mqtt/mqttsa/mqttsa.py",
                "address": values["IP"],
                "port": int(values["port"]),
                "username": values["bruteforce_username"],
                "wordlist": values["bruteforce_wordlist"],
            }
            config_data["scriptConfigurations"].append(bruteforce_data)

        if values["malformed_enabled"]:
            malformed_data = {
                "mode": "malformed",
                "mqttsa_path": "/home/jishnusen/Desktop/mqtt/mqttsa/mqttsa.py",
                "address": values["IP"],
                "port": int(values["port"]),
            }
            config_data["scriptConfigurations"].append(malformed_data)

        filename = sg.popup_get_file(
            "Save Config As",
            save_as=True,
            no_window=True,
            default_extension="yaml",
            file_types=(("YAML Files", "*.yaml"),),
        )
        if filename:
            save_config(filename, config_data)
            window["msg"].update("Configuration saved.")
    elif event == "Load" or event == "LoadFromDropdown":

        if event == "Load":
            filename = sg.popup_get_file(
                "Load Config From",
                no_window=True,
                default_extension="yaml",
                file_types=(("YAML Files", "*.yaml"),),
            )
            if filename and filename not in loaded_configs:
                loaded_configs.append(filename)

                window["loaded_configs_dropdown"].update(values=loaded_configs)
        else:
            filename = values["loaded_configs_dropdown"]

        if filename:
            config_data = load_config(filename)

            # Reset checkboxes and input boxes

            for key in [
                "slowdos_enabled",
                "malaria_enabled",
                "bruteforce_enabled",
                "malformed_enabled",
            ]:
                window[key].update(value=False)
            for key in [
                "slowdos_keepalive",
                "slowdos_duration",
                "malaria_message_count",
                "malaria_processes",
                "malaria_message_size",
                "bruteforce_username",
                "bruteforce_wordlist",
            ]:
                window[key].update(value="")

            # Populate checkboxes and input boxes based on the loaded configuration

            for operation in config_data["scriptConfigurations"]:
                mode = operation["mode"]
                if mode == "slowdos":
                    window["slowdos_enabled"].update(True)

                    window["slowdos_keepalive"].update(
                        str(operation.get("keep_alive", ""))
                    )

                    window["slowdos_duration"].update(str(operation.get("time", "")))
                elif mode == "malaria":
                    window["malaria_enabled"].update(True)

                    window["malaria_message_count"].update(
                        str(operation.get("message_count", ""))
                    )

                    window["malaria_processes"].update(
                        str(operation.get("processes", ""))
                    )

                    window["malaria_message_size"].update(
                        str(operation.get("message_size", ""))
                    )
                elif mode == "bruteforce":
                    window["bruteforce_enabled"].update(True)

                    window["bruteforce_username"].update(operation.get("username", ""))

                    window["bruteforce_wordlist"].update(operation.get("wordlist", ""))
                elif mode == "malformed":
                    window["malformed_enabled"].update(True)

            window["msg"].update("Configuration loaded.")
    elif event == "RUN":
        if filename:
            config_data = load_config(filename)
            for operation in config_data['scriptConfigurations']:
            	threading.Thread(target=execute_attack, args=(operation, window)).start()


window.close()

