#!/usr/local/bin/python
# Configuration Backups
from sys      import exit
from zipfile  import ZipFile
from os.path  import basename
from os       import stat

try: import webDavNC as WDNC
except: print("Failed to import webDavNC.py - \
        please add the file to this directory")
        
#################################
##   Enable/Disable Backups    ##
#################################

#Create jail storage shares:
# source: /mnt/volume1/jailname (I have one jail for multiple plugins)
# target: /sabnzbd/

backupFiles = [
{'status':True, 'name': "SabNZB_Config", 'path': \
"/sabnzbd/var/db/sabnzbd/sabnzbd.ini"},
{'status':True, 'name': "Sickrage_DB", 'path': \
"/sabnzbd/var/db/sickrage/sickbeard.db"},
{'status':True, 'name': "Sickrage_Config", 'path': \
"/sabnzbd/var/db/sickrage/config.ini"},
{'status':True,  'name': "Couchpotato_Config", 'path': \
"/sabnzbd/var/db/couchpotato/settings.conf"},
{'status':True,  'name': "Transmission_Config", 'path': \
"/sabnzbd/var/db/transmission/settings.json"},
{'status':True,  'name': "Headphones_Config", 'path': \
"/sabnzbd/var/db/headphones/config.ini"},
{'status':True,  'name': "Headphones_DB", 'path': \
"/sabnzbd/var/db/headphones/headphones.db"},
{'status':True,  'name': "Tautulli_DB", 'path': \
"/usr/local/share/Tautulli/tautulli.db"},
{'status':True,  'name': "Tautulli_Config", 'path': \
"/usr/local/share/Tautulli/config.ini"},
{'status':True,  'name': "Nginx_Config", 'path': \
"/nextcloud/usr/local/etc/nginx/nginx.conf"},
{'status':True,  'name': "SSL_common_Config", 'path': \
"/nextcloud/usr/local/etc/nginx/ssl_common.conf"}
]


zipFilePath = "/tmp/BackupConfigs.zip"
remotePath = '/BackupConfigs.zip'

''' Login Credentials Format of File
PaSsW0Rd123
LoGiN
'''

#This directory could have a different name depending on if you git clone
#If you download the files individ., just be sure to mkdir /mnt/scripts
credentialsFile = '/mnt/scripts/loginCreds.txt'
WebDAVURL = "https://sub.domain.com/subdir/remote.php/webdav/"

    
def detFileSize(file): 
    bits = stat(file).st_size
    for x in ['bits', 'KB', 'MB', 'GB', 'TB']:
        if bits < 1000.0:
            return "%3.1f %s" % (bits, x)
        bits /= 1000.0

def zipFiles(zipPath):
    print("Zipping Files:")
    with ZipFile(zipPath, 'w') as fileObject:
        for file in backupFiles:
            if file['status']:
                try: 
                    fileName = basename(file['path'])
                    fileObject.write(
                     file['path'], 
                     file['name']+'__'+str(fileName)
                    )
                    print("Zipped: %s"%file['path'])
                    print("Size: %s"%detFileSize(file['path']))
                except Exception as err: 
                    print(err)
                    print("[ERROR] FAILED TO ARCHIVE: %s"%file['name'])
        #Perform cyclic redundancy check and test file headers of zip
        zipStatus = fileObject.testzip()
    if zipStatus == None:
        print("Successfully Zipped Archive!")
    else:
        print("Failed to zip files: %s"%zipStatus)
        print("Exiting to Prevent Corruption of Possible Good File")
        exit()


def main(): 
    zipFiles(zipFilePath)
    print("Total Zip Size: %s"%detFileSize(zipFilePath))
    
    login = WDNC.Login()
    clientAPI = login.fetchCredentials(WebDAVURL,credentialsFile)
    
    webTask = WDNC.Synchronous()
    webTask.uploadFile(clientAPI, remotePath, zipFilePath)

if __name__ == "__main__": 
    main() 
    



