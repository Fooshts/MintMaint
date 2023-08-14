import subprocess

def disk_cleanup():
    try:
        print("Cleaning up temporary files...")
        # Use pkexec to run the entire cleanup process with elevated privileges
        subprocess.run(["pkexec", "sh", "-c", "rm -rf /tmp/* /var/tmp/*"], check=True)
        print("Temporary files cleanup completed.")
    except subprocess.CalledProcessError as e:
        print(f"Error cleaning up temporary files: {e}")

if __name__ == "__main__":
    disk_cleanup()
