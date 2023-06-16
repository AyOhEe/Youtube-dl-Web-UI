import webbrowser
import time

import server
import handler
from server import start_server
from handler import start_handler

PORT = 8000
ADDRESS = "127.0.0.128"

#IDEAS
# - pretty string decorator: used on __str__ to represent an object as a prettified json string,
#                            taking the names of each field to be stored as *args
# - download location changing via the settings module
# - actually using the logging module as i should be

#TODO
# - exception handling
# - checking to make sure an instance isn't already up, and if so, just opening the webpage.
#   could use a file in the working directory?
# - try/except in the handler thread so it doesn't die when a bad link is passed
# - file type selector

def main():
    import os
    os.system("")  # enables ansi escape characters in terminal
    print("\u001b[31mYoutube-dl\u001b[0m Web UI Console log - \u001b[32mDon't worry too much about this window!\u001b[0m")

    start_server(ADDRESS, PORT)
    start_handler()

    time.sleep(2)

    #TODO maybe have the auto open be a setting, and then have a settings.json which can be
    #     edited in the web ui?
    #PRERELEASE make sure this gets uncommented, this should be included in the build
    webbrowser.open(f"http://{ADDRESS}:{PORT}/web")

    #wait for exit input
    try:
        input("\t\u001b[33mPress enter to exit, when you're ready to quit the server.\u001b[0m\n\n\n")
    except KeyboardInterrupt:
        pass #we can silently ignore this, catching ctrl-c should start quitting anyway

    print("\n\nWaiting for threads to exit...")

    server.shutdown(ADDRESS, PORT)
    handler.shutdown()


if __name__ == "__main__":
    main()