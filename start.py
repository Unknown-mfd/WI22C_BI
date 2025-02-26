import subprocess
import sys
import os
import threading

# Funktion zur Überprüfung und Installation von Requirements
def install_requirements():
    if os.path.exists("requirements.txt"):
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    else:
        print("requirements.txt nicht gefunden!")

def run_streamlit():
    subprocess.run([sys.executable, "-m", "streamlit", "run", "dashboard.py"], check=True)

def run_additional_scripts():
    scripts = ["Scrapper/amazon.py", "Scrapper/google-trends.py", "Scrapper/idealo.py"]
    threads = []
    for script in scripts:
        thread = threading.Thread(target=subprocess.run, args=([sys.executable, script],), kwargs={"check": True}, daemon=True)
        thread.start()
        threads.append(thread)

if __name__ == "__main__":
    # Überprüfen und Installieren der Requirements
    install_requirements()
    
    # Starten von Streamlit in einem separaten Thread
    streamlit_thread = threading.Thread(target=run_streamlit, daemon=True)
    streamlit_thread.start()

    # Starten von zusätzlichen Skripten in separaten Threads
    run_additional_scripts()

