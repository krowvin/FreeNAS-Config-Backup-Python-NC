[![FreeNAS Logo](https://forums.freenas.org/logo_flat_V2.png)](https://forums.freenas.org/index.php)

## [AHOY] There are many ways to backup your configuration files.  
* One method is to rely on the automatic backups of the programs themselves.  
* Another would be to copy them into another directory on your server.  
* You might even decide to email the file to yourself (Which I tried at first, until I ran into Google's email attachment limit)  
[Bidule0hm](https://forums.freenas.org/index.php?members/bidule0hm.31801/) does [email the FreeNAS backup](https://forums.freenas.org/index.php?threads/scripts-to-report-smart-zpool-and-ups-status-hdd-cpu-t%C2%B0-hdd-identification-and-backup-the-config.27365/) to himself (among other things), you should check that out as I skipped it in this program. 

## [Why?] What does it do?  
One of the best features, imo, of FreeNAS/BSD is that the jails are seperated. If one fails, you can delete it and create a new one.  
You even have the option to attach storage to these jails so that it persists through jail upgrades/deletions.  
While this script is intended for use with Sickrage, Headphones, Sabnzbd, Tautulli (Formerly PlexPY), and NGINX.  
You can upload just about any file with it.  
Just point to the path where that file exists. As far as I know there is no size limit. 

This Python script is designed to [zip](https://docs.python.org/2/library/zipfile.html) the database and configuration files from various share points, storage mounts, and other directories into one file. That file can then be uploaded to your personal [NextCloud](https://nextcloud.com/) server through the [Python WebDAV API](https://pypi.python.org/pypi/webdavclient/1.0.8) on a set schedule through Crontab. 

[Checkout FreeNAS for Yourself](http://www.freenas.org/)


## [Setup] Installation
1. Download from git and upload both BackupConfigs.py and webDavNC.py using SFTP to /mnt/volume/jail/mnt/scripts *(for example)* a jail directory on your FreeNAS box. 
2. Enter your FreeNAS jail, if you are logged in as root to the FreeNAS box you can type:  
```
jexec list  
jexec <jailID> csh
```  
3. Once you are in the Jail ensure you have python installed with  
```pkg install python```  
4. You will also need the webdav client, you can view the documentation [here](https://pypi.python.org/pypi/webdavclient/1.0.8)  
To install the package I was able to type:  
```easy_install webdavclient```  
Assuming you are the root user of the jail, you won't need sudo  
###If you decide to clone the directory  
4.1. Navigate to the directory where you uploaded your files, you might also be able to use:  
```
cd /mnt  
pkg install git  
git clone <repoURL>  
```  
4.2. Navigate into the Cloned Directory with ```cd <dirname>```  
5. Login to your FreeNAS GUI, click Jails>Storage and select the jail you are running this script in. Mount the storage points from the jails directory to directories in the current jail. i.e.
source: /mnt/volume1/jailname (I have one jail for multiple plugins)  
target: /sabnzbd/  
6. Open (nano BackupConfigs.py) and change the path values and WebDavURL seen below:  
```
backupFiles = [
{'status':True, 'name': "SabNZB_Config", 'path': \
"/sabnzbd/var/db/sabnzbd/sabnzbd.ini"},              #PATH VALUE -> "pathvalue"},
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

credentialsFile = 'loginCreds.txt'
WebDAVURL = "https://sub.domain.com/subdirectory/remote.php/webdav/"
```
Save the file by typing ctrl+x *>* y *>* enter  
7. If you want to use your LetsEncrypt server certs - open webDavNC.py and change:  
```
cert_path= "/etc/letsencrypt/live/sub.domain.com/fullchain.pem"
key_path = "/etc/letsencrypt/live/sub.domain.com-0001/privkey.pem"
```
If you do not have ssl setup, *you should*  
Change the options variable to:  
```
options = {
   'webdav_hostname': WebDAVURL,
   'webdav_login':    MY_ADDRESS,
   'webdav_password': PASSWORD
  }
```
Save the file by typing ctrl+x *>* y *>* enter  
8. Change the file permissions to:  
```
chmod 700 BackupConfigs.py  
chmod 700 webDavNC.py  
```

9. Almost there, try running the file with:
```
./BackupConfigs.py
```
You *should* see the console list which files are zipped, and the zip sizes. 

10. You will be asked to create a credentials file, while the file is *NOT* encrypted I did try to automatically make sure the file permissions are 400. You can confirm this in FreeNAS with the command ```ll```

11. Navigate to your Nextcloud Web Client and download the zip file.  
Make sure the configs are there, and that you can open them with a text editor. *(The .txt files, not the .db files)*

*Note: If you don't know the webdav url you can find it by logging in to your Nextcloud with a browser and clicking the settings icon at the bottom left*


## [Automation] Running as a Cron Task through the FreeNAS GUI
Now that you made sure the file can run at least once with no errors, as well as creating the configuration file, you should be able to create a cron job. 


To do this, open the FreeNAS GUI in your web browser. Login and click tasks < Cron Jobs < Add Cron Job
**PreNotes:** 
* Type ```jls``` to see the Jail Hostname
* change the command to suite your directory structure, don't forget the leading **.**
* Rotate your run times from other system tasks
* Uncheck Redirect Stdout after the first few runs, you can see the output in the console at the bottom of the screen (Enable the GUI console in the FreeNAS settings)
```
User: root
Command: jexec <Hostname> csh ./mnt/scripts/BackupConfigs.py
Short Description: Backup Configs
Minute: Each selected minute > 37
Hour: Each selected hour > 4
Day of month: Each selected day of month > 8, 21
Month: CHECKBOX ALL
Day of Week: CHECKBOX ALL
Redirect Stdout: Not Checked (Standard Output)
Redirect Stderr: Not Checked (Standard Error Output)
Enabled: Checkboxed
```

**Test your cron task:**
Click on the task *>* Click Run Now at the bottom of the screen

## [Recovery] How would I use these files? 
Lets say you make an edit to one of your configurations that breaks your sickrage instance, or maybe your history doesn't load for Tautulli's database. One option would be to copy the backup file and replace the current working database directly. 

That will work most of the time, however, if you delete your jail and forget to save your config/database. (Or any other number of unforseen incidents) You will now have the option to:
1. Download your BackupConfigs.zip file from NextCloud
2. Unzip the file
3. Rename the config/database file you want to replace to the same name as the file in the plugin and replace. 
###For example: 
Recovered zip file named **SabNZB_Config__sabnzbd.ini** and *rename it* to **sabnzbd.ini**, then copy to the server using SFTP and replace the file in /mnt/volume/jail_1/var/db/sabnzbd/sabnzbd.ini with this newly renamed file.

### Just *Happy* Little Features
* I started to write code to handle archival and mutiple copies of the backup zip file within nextcloud. Then it dawned on me that NextCloud has it's own version control of the files! *neato!*

* I included a cyclic redundancy check for the zip file, thanks to the Python WebDAV API - Meaning you won't upload a corrupted file

* This was my first github repo, I'm open to criticism and feedback. If something is confusing I can shorten or elaborate on it given your suggestion!
