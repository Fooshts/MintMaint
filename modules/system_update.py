import subprocess

def system_update():
    try:
        print("Updating system packages...")
        subprocess.run(["pkexec", "sh", "-c", "apt update && apt upgrade -y && apt autoremove -y"], check=True)
        print("System update completed.")
        return "System update completed successfully."
    except subprocess.CalledProcessError as e:
        return f"Error updating system: {e}"

if __name__ == "__main__":
    result = system_update()
    print(result)
