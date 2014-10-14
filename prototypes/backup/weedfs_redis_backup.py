from JumpScale import j
import JumpScale.baselib.backup

j.application.start("jumpscale:btrfstest")

backup_client = j.clients.backup.get4BlobstorLedisWeedFS('test', 'test')
file_id = backup_client.uploadFile('/home/test/file.zip')
# will download this file, and write it to /opt/testdownload
backup_client.downloadFile(file_id, '/opt/testdownload')

dir_id = backup_client.uploadDir('/home/test/Downloads')
# will download dir files to /opt/test/
backup_client.downloadDir(dir_id, '/opt/test')

j.application.stop()