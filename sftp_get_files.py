import paramiko
from paramiko import sftp_client
import datetime
import credentials

# get timestamp for log
temp_timestamp = str(datetime.datetime.now())
print(2 * "\n")
print(temp_timestamp)


# setup connection


def grab_files(file_list):

    # Get files from RaspberryPi

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(
        hostname=credentials.pi_host,
        username=credentials.pi_user,
        password=credentials.pi_pass,
        port=22,
    )
    sftp_client = ssh.open_sftp()

    files = sftp_client.listdir()
    print(files)

    for file_name in file_list:
        sftp_client.get("/public/" + file_name, "incoming_files/" + file_name)
        print(f"Retrieved {file_name} from remote")

    sftp_client.close()
    ssh.close()


# grab_files(
#     [
#         "03_4_PS_Enroll.csv",
#         "03_0_Student_Identity.csv",
#         "03_5_PS_GradeProg.csv",
#         "03_6_PS_ADM.csv",
#         "03_7_PS_Att.csv",
#     ]
# )
