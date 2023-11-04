import subprocess

def install_dependencies(requirements_file):
    try:
        subprocess.check_call(["pip", "install", "-r", requirements_file])
        return True
    except subprocess.CalledProcessError:
        return False

if __name__ == "__main__":
    requirements_file = "requirements.txt"
    
    if install_dependencies(requirements_file):
        print("Dependencies installed successfully.")
    else:
        print("Failed to install dependencies.")
