import streamlit.web.bootstrap
import os
import sys

# Add the src directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if __name__ == "__main__":
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, "asa24_analyzer.py")
    
    sys.argv = [
        "streamlit",
        "run",
        filename,
        "--server.address=0.0.0.0",
        "--server.port=53189",
        "--server.headless=true",
        "--browser.serverAddress=localhost",
        "--server.enableCORS=false",
        "--server.enableXsrfProtection=false"
    ]
    
    streamlit.web.bootstrap.run()