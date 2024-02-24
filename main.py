import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QToolBar
from PyQt6.QtWebEngineWidgets import QWebEngineView
import PyQt6.QtWidgets 
#from PyQt6.QtWebKitWidgets import QWebPage
from PyQt6.QtCore import QUrl, QTimer
import subprocess
import urllib.request

# Define variables to hold references to the subprocesses
python_script_process1 = None

# Define global variables to hold button states
analysis_app_running = False

def run_python_script1():
    global python_script_process1, analysis_app_running
    command_python1 = [
        "/home/trader/Documents/breeze_venv/bin/python",
        "./app.py"
    ]
    python_script_process1 = subprocess.Popen(command_python1)
    analysis_app_running = True

def stop_python_script1():
    global python_script_process1, analysis_app_running
    if python_script_process1:
        python_script_process1.terminate()
        python_script_process1 = None
        analysis_app_running = False

def set_button_style(run_script1_button, background_color=None):
    style = "min-height: 2px; padding: 1px 2px; font-size: 10px;"
    if background_color:
        style += f"background-color: {background_color};"
    run_script1_button.setStyleSheet(style)

def check_url_status(run_script1_button):
    global analysis_app_running
    try:
        urllib.request.urlopen("http://127.0.0.1:8050/").getcode()
        set_button_style(run_script1_button, background_color="#00a06d")
    except urllib.error.URLError:
        set_button_style(run_script1_button)



def main():
    app = QApplication(sys.argv)
    window = QMainWindow()
    central_widget = QWidget()
    layout = QVBoxLayout()
    browser = QWebEngineView()

    browser.setUrl(QUrl("http://127.0.0.1:8050/"))  # Load your URL here

    # Set the zoom level (adjust the value as needed)
    zoom_level = 0.75  # Example: 1.5 for 150% zoom
    browser.setZoomFactor(zoom_level)

    layout.addWidget(browser)
    central_widget.setLayout(layout)
    window.setCentralWidget(central_widget)

    window.setWindowTitle("My Hedge Fund")

    # Create a toolbar (top bar)
    toolbar = QToolBar()
    window.addToolBar(toolbar)


    run_script1_button = QPushButton("Run Analysis App", window)
    run_script1_button.clicked.connect(run_python_script1)
    run_script1_button.setStyleSheet("min-height: 2px; padding: 1px 2px; font-size: 10px;")
    stop_script1_button = QPushButton("Stop Analysis App", window)
    stop_script1_button.clicked.connect(stop_python_script1)
    stop_script1_button.setStyleSheet("min-height: 2px; padding: 1px 2px; font-size: 10px;")

    # Add custom buttons to the toolbar
    toolbar.addWidget(run_script1_button)
    toolbar.addWidget(stop_script1_button)

    # Initialize the QTimer for URL status check
    url_check_timer = QTimer()
    url_check_timer.timeout.connect(lambda: check_url_status(run_script1_button))
    url_check_timer.start(5000)  # Check every 15 seconds

    window.showMaximized()
    app.exec()

if __name__ == "__main__":
    main()
