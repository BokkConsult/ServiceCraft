import os
import subprocess

def create_systemd_service():
    # Prompt user for service name
    service_name = input("Enter the name of your service: ")

    # Prompt user for service description
    service_description = input("Enter the description of your service: ")

    # Prompt user for ExecStart command
    exec_start = input("Enter the ExecStart command (including the path to the executable): ")

    # Prompt user for RestartSec
    restart_sec = input("Enter the restart interval in seconds (RestartSec): ")

    # Prompt user for User
    user = input("Enter the user to run the service as: ")

    # Prompt user if the service should restart infinitely
    restart_infinity = input("Should the service restart infinitely if it fails? (yes/no): ").strip().lower()
    start_limit_interval = "StartLimitIntervalSec=0" if restart_infinity == "yes" else ""

    # Create the service file
    service_file_content = f"""[Unit]
Description={service_description}
After=network.target
{start_limit_interval}

[Service]
Type=simple
Restart=always
RestartSec={restart_sec}
User={user}
ExecStart={exec_start}

[Install]
WantedBy=multi-user.target
"""
    service_file_path = f"/etc/systemd/system/{service_name}.service"
    with open(service_file_path, "w") as f:
        f.write(service_file_content)

    # Reload systemd to read the new service file
    subprocess.run(["systemctl", "daemon-reload"])

    # Enable and start the service
    subprocess.run(["systemctl", "enable", service_name])
    subprocess.run(["systemctl", "start", service_name])

    # Colored output
    print("\033[92mService created and started successfully.\033[0m\n")
    print("\033[94mYou can manage your service using the following commands:\033[0m\n")
    print(f"\033[96m{'Description':<50}{'Command':<50}\033[0m")
    print(f"\033[92m{'Start the service':<50}{'sudo systemctl start ' + service_name:<50}\033[0m")
    print(f"\033[92m{'Stop the service':<50}{'sudo systemctl stop ' + service_name:<50}\033[0m")
    print(f"\033[92m{'Restart the service':<50}{'sudo systemctl restart ' + service_name:<50}\033[0m")
    print(f"\033[92m{'Enable the service at boot':<50}{'sudo systemctl enable ' + service_name:<50}\033[0m")
    print(f"\033[92m{'Disable the service at boot':<50}{'sudo systemctl disable ' + service_name:<50}\033[0m")

if __name__ == "__main__":
    create_systemd_service()
