import os
import time
import subprocess
import schedule

HOME = os.getenv("HOME")


def job():
    try:
        with open(f"{HOME}/.config/qtile/test.txt", "w") as f:
            proc = subprocess.run(
                "ping -c 1 fleetapi-sg.cartrack.com",
                shell=True,
                check=True,
                stdout=subprocess.DEVNULL,
            )
            if proc.returncode == 0:
                f.write("1")
            else:
                f.write("0")
    except Exception as ex:
        print(f"failed: {ex}")
        with open(f"{HOME}/.config/qtile/test.txt", "w") as f:
            f.write("0")


schedule.every(1).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
