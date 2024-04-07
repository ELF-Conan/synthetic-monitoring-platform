import pingparsing
from prometheus_client import Gauge, start_http_server
import time
import yaml

# Define the Prometheus metric
ping_latency_gauge = Gauge('ping_latency', 'Ping response time in milliseconds', ['target'])
ping_loss_gauge = Gauge('ping_packet_loss', 'Ping packet loss rate', ['target'])

def load_config(config_path):
    try:   
       with open(config_path, "r") as file:
           data = yaml.safe_load(file)
           print(yaml.dump(data, sort_keys=False))
           return data
    except FileNotFoundError:
        print(f"Error: The file '{config_path}' was not found.")
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")   

def ping_hosts(host, duration):
    """Ping host list, update the metric"""
    ping_parser = pingparsing.PingParsing()
    transmitter = pingparsing.PingTransmitter()

    transmitter.destination = host
    transmitter.count = duration  # default: send 4 ping packet
    result = transmitter.ping()
    parsed_result = ping_parser.parse(result).as_dict()
    # update Prometheus metric
    latency = parsed_result['rtt_avg']
    packet_loss = parsed_result['packet_loss_rate']
    ping_latency_gauge.labels(target=host).set(latency)
    ping_loss_gauge.labels(target=host).set(packet_loss)
    print(f"Pinged {host}: Avg latency={latency} ms, Packet Loss={packet_loss}%")

#if __name__ == "__main__":
    #config = load_config("../../config/monitor_config.yml")
def run_monitoring(config_path):
    config = load_config(config_path)
    http_port = config.get("http_port", 8000)
    ping_interval = config.get("ping_interval", 60)
    ping_targets = config.get("ping_targets", []) 

    # Start the HTTP server for Prometheus fetching
    start_http_server(http_port)

    while True:
        for target_info in ping_targets:
            host = target_info['host']
            duration = target_info.get('duration', 4)
            ping_hosts(host, duration)
        time.sleep(ping_interval)
