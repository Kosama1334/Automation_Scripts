# import required libraries

import psutil
import time
import re
import argparse
from datetime import datetime

#function to get the metrics of the server/system
def get_system_metrics():
  return {
    "CPU": psutil.cpu_percent(interval=1),
    "MEM": psutil.virtual_memory().percent,
    "DISK_USAGE": psutil.disk_usage('/').percent
  }

#function to scan the log file and look for lines with certain error keywords
def get_logs(log_fie, searchwords):
  try:
    with open(log_file, "r") as f:
      for line in f:
        for p in searchwords:
          if re.search(p, line, re.IGNORECASE):
            print(f"Found a line with '{p}': {line.strip()}")
            with open("output_logs.txt", "a") as k:
              k.write({line.strip()}, "\n")
            return True
  except FileNotFoundError:
    print(f"Log file '{log_file}' NOT FOUND")
  return False

#write the metrics in an output file
def write_to_file(msg):
  with open("output_metrics.txt", "a") as f:
    f.write(msg + "\n")


def get_metrics_logs(args):
  searchwords = args.searchwords.split(",")
  log_file = args.logfile

  while True:
    metrics = get_system_metrics()
    timestamp = datetime.now().strftime("%H:%M:%S %d-%m-%Y")

    msg = (
      f"{timestamp} | CPU: {metrics['CPU']}% | RAM: {metrics['MEM']}% | Disk_Usage: {metrics['DISK_USAGE']}%"
    )
    print(msg)

    if args.save:
      write_to_file(msg)

    get_logs(log_file, searchwords)
    time.sleep(args.interval)



# Main execution
if __name__ == "__main__":
  parser = argparse.ArgumentParser(description= "Getting metrics and requested lines from the log file")

  parser.add_argument("--logfile", default="sample.log", help="Log file to scan")
  parser.add_argument("--searchwords", default="ERROR, TimeOut, WARNING", help="keywords to look for in the log file")
  parser.add_argument("--interval", type=int, default=2, help="time interval to scan metrics")
  parser.add_argument("--save", action="store_true", help="Save metrics to an output file")

  args = parser.parse_args()
  get_metrics_logs(args)




