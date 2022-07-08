import paramiko

ssh_client =paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname='23.254.176.188',username='root',password='f0z1E5Im5s%tg(*765!$@')
ftp_client=ssh.open_sftp()
ftp_client.put('/Users/artemiikhristich/PycharmProjects/ObjectDetection2/main.py','icast-rest')
ftp_client.close()