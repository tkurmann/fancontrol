from subprocess import Popen, PIPE
import csv
import io
import re
import time
import os

gpu_fan_mapping  = {0: {0,1,2,3,4,5}, 1: {0,1,2,3,4,5}, 2: {0,1,2,3,4,5}, 3: {0,1,2,3,4,5}}


os.environ["NVSMI_SHOW_ALL_DEVICES"]="1"

def control_loop():
    while 1:
        process = Popen(["nvidia-smi", "dmon", "-c", "1"], stdout=PIPE)
        (output, err) = process.communicate()
        exit_code = process.wait()
        output = output.decode("utf-8")
        output = re.sub(' +',' ',output)
        reader=csv.reader(io.StringIO(output),delimiter=' ')
        row_count = 0
        gpu_temps = [None] * 8 # TBD: remove hard coded size

        for row in reader:
            row_count = row_count + 1
            if(row_count > 2):
                gpu_temps[int(row[1])] = int(row[3])


        #print(gpu_temps)
        for fan in gpu_fan_mapping:
            gpus = gpu_fan_mapping[fan]

            max_temp = 0
            for gpu in gpus:
                if(gpu_temps[gpu] > max_temp):
                    max_temp = gpu_temps[gpu]

            percentage = 25
            if(max_temp > 70):
               percentage = 45
            if(max_temp > 75):
               percentage = 55
            if(max_temp > 80):
               percentage = 75
            if(max_temp > 85):
               percentage = 90
            if(max_temp > 90):
               percentage = 100


            percentage = min(percentage, 100)
            percentage = max(percentage, 25)
            percHex = "0x%0.2X" % int(percentage)
            fanHex = "0x%0.2X" % int(fan)
            process = Popen(["ipmitool", "raw", "0x30", "0x70", "0x66", "0x01",fanHex, percHex ], stdout=PIPE)


        time.sleep(20)


def main(argv=None):  # pylint: disable=unused-argument
    control_loop()

if __name__ == "__main__":
    main()
