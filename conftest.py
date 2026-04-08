import os
import pytest
import threading
import http.server
import functools
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Try to find the active graphical display when running outside a desktop session
def _find_display():
    import subprocess, glob
    # Prefer Wayland
    for path in glob.glob("/run/user/*/wayland-*"):
        uid = path.split("/")[3]
        os.environ.setdefault("XDG_RUNTIME_DIR", f"/run/user/{uid}")
        return None  # WAYLAND_DISPLAY not needed when path is set via XDG_RUNTIME_DIR
    # Fall back to X11
    for path in glob.glob("/tmp/.X11-unix/X*"):
        return ":" + path.replace("/tmp/.X11-unix/X", "")
    return None

if not os.environ.get("DISPLAY") and not os.environ.get("WAYLAND_DISPLAY"):
    display = _find_display()
    if display:
        os.environ["DISPLAY"] = display

PORT = 8765
SERVER_DIR = "."


@pytest.fixture(scope="session")
def local_server():
    """Start a local HTTP server for the duration of the test session."""
    handler = functools.partial(
        http.server.SimpleHTTPRequestHandler,
        directory=SERVER_DIR
    )
    server = http.server.HTTPServer(("localhost", PORT), handler)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    yield f"http://localhost:{PORT}"
    server.shutdown()


@pytest.fixture(scope="session")
def driver():
    """Provide a headless Chrome WebDriver for the test session."""
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280,800")

    service = Service(ChromeDriverManager().install())
    drv = webdriver.Chrome(service=service, options=options)
    drv.implicitly_wait(5)
    yield drv
    drv.quit()
