import threading
import time
import yt_dlp as yt_dl

operations = []
exit_thread = False
exited_thread = False


def shutdown():
    global exit_thread

    
    exit_thread = True


class HandlerOperation:
    def __init__(self):
        pass

    def handle_request(self):
        pass

class HandlerSingleDownload:
    def __init__(self, url:str, format:str, location:str) -> None:
        self.url = url
        self.format = format
        self.location = location
        print(f"Single download operation created: {self.url}")

    def handle_request(self):
        opts = {
            'noplaylist' : '',
            'format' : self.format,
            'outtmpl' : f"{self.location}/%(title)s.%(ext)s",
        }

        print(f"<Handler> Downloading {self.url} to {self.location}")
        with yt_dl.YoutubeDL(opts) as ydl:
            ydl.download([self.url])

def add_handler_operation(op: HandlerOperation) -> None:
    global operations


    operations.append(op)

def handler_target() -> None:
    global exited_thread, exit_thread
    global operations


    while True:
        if exit_thread:
            break

        if len(operations) != 0:
            next_op = operations.pop(0)
            next_op.handle_request()
        time.sleep(0.1)

    exited_thread = True
    print("<Handler> Exited cleanly.")

def start_handler(*args, **kwargs) -> None:
    handler_thread = threading.Thread(target=handler_target, args=args, kwargs=kwargs)
    handler_thread.start()
    return handler_thread