import subprocess
import sys
import boto3
import datetime

s3 = boto3.client('s3')

def main(argv):
    cmd =  determine_command(int(argv[0]))
    log_file_name = datetime.datetime.now(datetime.timezone.utc).strftime("%m/%d/%Y, %H:%M:%S")+ "_logfile"
    kickoff_subprocess(cmd, log_file_name)
    upload_output_to_S3(log_file_name)



# instead of allowing free-form input
# we instead have them enter a number
# which corresponds to a command that is pre-written
# you also could present a menu that allows them to select the command
# but either way we are avoiding allowing free-form entry
def determine_command(user_input):
    if(user_input == 1):
        return ['echo', "command1"]
    if(user_input == 2):
        return ['echo', "command2"]
    if(user_input == 3):
        return ['echo', "command3"]
    else:
        return ['echo', "default"]


def kickoff_subprocess(cmd, log_file_name):
    process = subprocess.call(cmd, shell=False)
    timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%m/%d/%Y, %H:%M:%S")
    output = timestamp + " Command: "+ cmd[0] + " | Return Code: " + str(process) + "\n"
    with  open(log_file_name, "a+") as f:
        f.write(output)

def upload_output_to_S3(log_file_name):
    with open(log_file_name, "rb") as f:
        s3.upload_fileobj(f, "petr-j-testing", log_file_name)

if __name__ == "__main__":
   main(sys.argv[1:])
