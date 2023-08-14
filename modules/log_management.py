import os
import subprocess

def log_management():
    try:
        print("Cleaning up logs in /var/log...")
        subprocess.run(["pkexec", "sh", "-c", "find /var/log -name '*.log' -exec rm -f {} +"])
        print("Log cleanup completed.")
    except subprocess.CalledProcessError as e:
        print(f"Error cleaning up logs: {e}")

if __name__ == "__main__":
    log_management()
