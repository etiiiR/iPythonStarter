import os
import subprocess
import fnmatch
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import sys
# Check if Jupytext is installed; if not, install it
try:
    import jupytext
except ImportError:
    subprocess.run(['python', '-m', 'pip', 'install', 'jupytext'])

# Redirect stdout to a file
log_file_path = "watchdog_observer_log.txt"
log_file = open(log_file_path, "w")
sys.stdout = log_file



script_filename = os.path.basename(__file__)

# Define the directory to monitor
directory_to_watch = os.getcwd()

# Function to check if a file exists
def file_exists(file_path):
    print(print("Current Working Directory:", os.getcwd()))
    return os.path.isfile(file_path)

# Function to check if a .py file contains at least one line with #%% or # %%
def is_valid_py_file(py_file):
    with open(py_file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if '#%%' in line or '# %%' in line:
                return True
        return False

# Function to convert .ipynb to .py:percent
def convert_ipynb_to_py_percent(ipynb_file):
    subprocess.run(['python', '-m', 'jupytext', '--to', 'py:percent', ipynb_file])

# Function to convert .py:percent to .ipynb
def convert_py_percent_to_ipynb(py_percent_file):
    subprocess.run(['python', '-m', 'jupytext', '--to', 'notebook', py_percent_file])

# Create a custom event handler to trigger the conversion when a file is saved
class FileChangeHandler(FileSystemEventHandler):
    recently_modified = {}  # Dictionary to store recently modified files and their timestamps

    def on_modified(self, event):
        if not event.is_directory and event.src_path != script_filename:
            name, extension = os.path.splitext(event.src_path)
            if extension in {'.py', '.ipynb'} and not fnmatch.fnmatch(event.src_path, '.git*'):
                ipynb_file = name + '.ipynb'
                py_percent_file = name + '.py'

                # Check if the file was modified within the last 5 seconds
                current_time = time.time()
                last_modified_time = self.recently_modified.get(event.src_path, 0)
                if current_time - last_modified_time < 5:
                    return  # Skip processing if the file was recently modified

                self.recently_modified[event.src_path] = current_time  # Update the modification time

                if (
                    file_exists(ipynb_file) and file_exists(py_percent_file)
                    and event.src_path not in {ipynb_file, py_percent_file}
                ):
                    ipynb_mtime = os.path.getmtime(ipynb_file)
                    py_percent_mtime = os.path.getmtime(py_percent_file)

                    if ipynb_mtime > py_percent_mtime:
                        # .ipynb is newer, delete .py:percent and convert .ipynb to .py:percent
                        print('notebook newer')
                        os.remove(py_percent_file)
                        convert_ipynb_to_py_percent(ipynb_file)
                    elif ipynb_mtime < py_percent_mtime:
                        # .py:percent is newer, delete .ipynb and convert .py:percent to .ipynb
                        print('pyscript newer')
                        os.remove(ipynb_file)
                        convert_py_percent_to_ipynb(py_percent_file)
                else:
                    if file_exists(ipynb_file):
                        print('file exits not pyprecent')
                        # Only .ipynb exists, convert it to .py:percent
                        convert_ipynb_to_py_percent(ipynb_file)
                    elif file_exists(py_percent_file) and is_valid_py_file(py_percent_file):
                        # Only .py exists with at least one valid comment line, convert it to .ipynb
                        print('file not exits pynotebook')
                        convert_py_percent_to_ipynb(py_percent_file)

# Create a watchdog observer
event_handler = FileChangeHandler()
observer = Observer()
observer.schedule(event_handler, path=directory_to_watch, recursive=False)
observer.start()

try:
    while True:
        pass
except KeyboardInterrupt:
    observer.stop()
observer.join()


log_file.close()
sys.stdout = sys.__stdout__

# Print the contents of the log file
with open(log_file_path, "r") as log_file:
    print(log_file.read())