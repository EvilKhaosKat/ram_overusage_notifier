import psutil
import time
import os
#import sys

class Main:
    DEFAULT_ICON = '/usr/share/icons/gnome/32x32/status/software-update-urgent.png'
    DEFAULT_EXPIRE_TIME = 7000
    DEFAULT_PROCESS_MEMORY_LIMIT_MB = 2048
    DEFAULT_SLEEP_PERIOD_SEC = 5
    EXCLUDED_PROCESS_NAMES = []

    @staticmethod
    def get_process_used_memory_mb(process):
        resident_memory_size = process.memory_info()[0]
        return resident_memory_size / (1024 * 1024)

    @staticmethod
    def send_notify(message):
        os.system("notify-send --urgency=critical -i {icon} -t {expire_time} 'ram overusage notify' '{message}'"
                  .format(icon=Main.DEFAULT_ICON, expire_time=Main.DEFAULT_EXPIRE_TIME, message=message))

    @staticmethod
    def check_ram_overusage():
        previous_max = None

        while True:
            processes = psutil.get_process_list()
            processes = list(filter(lambda process: process.name() not in Main.EXCLUDED_PROCESS_NAMES, processes))

            if len(processes) > 0:
                max_memory_used_process = max(processes, key=Main.get_process_used_memory_mb)

                used_memory_mb = Main.get_process_used_memory_mb(max_memory_used_process)
                if used_memory_mb > Main.DEFAULT_PROCESS_MEMORY_LIMIT_MB:
                    if not previous_max or previous_max.pid != max_memory_used_process.pid:
                        Main.send_notify("Process {process_name} uses {used_memory:.2f} mb of RAM"
                                         .format(process_name=max_memory_used_process.name(), used_memory=used_memory_mb))

                    previous_max = max_memory_used_process

            time.sleep(Main.DEFAULT_SLEEP_PERIOD_SEC)


Main().check_ram_overusage()