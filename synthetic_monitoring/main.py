# main.py
from monitoring.ping import run_monitoring

if __name__ == "__main__":
    config_path = "../config/monitor_config.yml"
    run_monitoring(config_path)
