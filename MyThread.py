import threading

class MyThread(threading.Thread):
    def __init__(self, target, args):
        threading.Thread.__init__(self)
        self.stop_flag = threading.Event()  # Tạo một cờ để đánh dấu việc dừng thread
        self.target = target
        self.args = args

    def run(self):
        self.target(scheduler=self.args, stop_flag=self.stop_flag)  # Truyền cờ dừng vào hàm target

    def stop(self):
        self.stop_flag.set()  # Đặt cờ dừng để kết thúc vòng lặp của thread