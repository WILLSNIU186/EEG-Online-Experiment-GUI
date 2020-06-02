import numpy as np
import threading

class thread_test:
    def __init__(self):
        self.is_recording_running = False
        self.counter = 0

    def start_recording_data(self):
        self.is_recording_running = True
        self.thread = threading.Thread(target=self.record)
        self.thread.start()

    def stop_recording_data(self):
        self.is_recording_running = False

    def record(self):
        self.counter += 1
        print("I RUNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN")
        # while self.is_recording_running:
        #     pass
            # print("record run")

if __name__ == "__main__":
    t = thread_test()
    key = input()
    t.start_recording_data()

    input()
    t.stop_recording_data()

    input()
    t.start_recording_data()

    input()
    t.stop_recording_data()

    print(t.counter)