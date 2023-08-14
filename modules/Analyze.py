import os
import platform
import subprocess

def Analyze():
    system_info = ""

    # System information
    system_info += "System Information:\n"
    system_info += f"OS: {platform.system()} {platform.release()}\n"
    system_info += f"Architecture: {platform.machine()}\n"

    # CPU information
    cpu_info = subprocess.check_output(["lscpu"]).decode("utf-8")
    system_info += f"\nCPU Information:\n{cpu_info}\n"

    # Memory information
    mem_info = subprocess.check_output(["free", "-h"]).decode("utf-8")
    system_info += f"\nMemory Information:\n{mem_info}\n"

    # Disk information
    disk_info = subprocess.check_output(["df", "-h"]).decode("utf-8")
    system_info += f"\nDisk Information:\n{disk_info}\n"

    # Network information
    network_info = subprocess.check_output(["ip", "a"]).decode("utf-8")
    system_info += f"\nNetwork Information:\n{network_info}\n"

    return system_info

def save_to_file(content, file_path):
    with open(file_path, "w") as file:
        file.write(content)

if __name__ == "__main__":
    system_info = Analyze()
    output_file = "system_info.txt"
    save_to_file(system_info, output_file)
    print(f"System information saved to {output_file}")

