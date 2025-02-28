import subprocess
import sys
import os

def install_requirements():
    """Install the required modules from requirements.txt."""
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], capture_output=True, text=True)
        if result.returncode != 0:
            print(result.stderr)
            sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error installing requirements: {e}")
        sys.exit(1)

def start_frontend():
    """Start the frontend web server."""
    try:
        subprocess.Popen(["python", "-m", "http.server", "8000", "--directory", "Online-Store/frontend"])
        print("Frontend started at http://localhost:8000")
    except Exception as e:
        print(f"Error starting frontend: {e}")

def start_dashboard():
    """Start the Streamlit dashboard."""
    try:
        subprocess.Popen(["python", "-m", "streamlit", "run", "Dashboard/app.py"])
        print("Dashboard started at http://localhost:8501")
    except Exception as e:
        print(f"Error starting dashboard: {e}")

def run_pipelines():
    """Run the data pipelines."""
    pipelines = ["Piplines/newsorg.py", "Piplines/idealo.py", "Piplines/google-trends.py", "Piplines/amazon.py"]
    for pipeline in pipelines:
        if os.path.exists(pipeline):
            try:
                subprocess.Popen(["python", pipeline])
                print(f"Pipeline {pipeline} started.")
            except Exception as e:
                print(f"Error running pipeline {pipeline}: {e}")
        else:
            print(f"Pipeline {pipeline} not found.")

if __name__ == "__main__":
    install_requirements()
    start_frontend()
    start_dashboard()
    
