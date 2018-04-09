#!/usr/local/bin/python
#WebDAV client 
#Python -> Nextcloud
#https://github.com/CloudPolis/webdav-client-python

import webdav.client as wc
from sys import exit, version_info
from os  import chmod

class Login():
    def changePermissions(self, filePath):
        print("Setting Credential File Permissions to 400")
        if version_info[0] < 3:
            chmod(filePath,0400)
        else:
            chmod(filePath,0o400)

    def retryLogin(self, credentialsFile, WebDAVURL):
        
        connected = False
        failedCount = 1
        while not connected:
            try:
                print("We can create the credentials file in Plain Text:")
                print("Press Ctrl + C to Exit/Cancel")
                MY_ADDRESS = raw_input("Enter your NextCloud Login    : ")
                PASSWORD   = raw_input("Enter your NextCloud Password : ")
                with open(credentialsFile,'w') as credentials:
                    credentials.write(PASSWORD+'\n')
                    credentials.write(MY_ADDRESS)
                self.changePermissions(credentialsFile)
                options = {
                 'webdav_hostname': WebDAVURL,
                 'webdav_login':    MY_ADDRESS,
                 'webdav_password': PASSWORD
                }
                client = wc.Client(options)
                print("Saved Credentials to: %s"%credentialsFile)
                connected = True
                return client
                
            except Exception as err:
                connected = False
                if failedCount > 3:
                    print("Exceeded '3' Failed Login Attempts:\n%s"%err)
                    exit()
                elif str(err).find('global name') != -1:
                    print("Missing Library: %s"%err)
                    exit()
                else:
                    print("Invalid Credentials: %s"%err)
                    print("Try again, or Ctrl + C to Exit:")
                    failedCount += 1          
        
    def fetchCredentials(self, WebDAVURL,credentialsFile):
        try:
            with open(credentialsFile) as credentials:
                data = credentials.readlines()
                PASSWORD = data[0].strip('\n')
                MY_ADDRESS = data[1].strip('\n')
            print("\nNC Login Credentials Obtained")
            print("--------------------------")
            print("LOGIN:    %s"%MY_ADDRESS)
            print("PASSWORD: %s\n"%(PASSWORD))
            self.changePermissions(credentialsFile)
            options = {
             'webdav_hostname': WebDAVURL,
             'webdav_login':    MY_ADDRESS,
             'webdav_password': PASSWORD
            }
            client = wc.Client(options)
            return client
        except Exception as err:
            if str(err).find('connection') != -1:
                print("Connection Error:\n\t%s"%err)
                exit()
            if str(err).find('global name') != -1:
                        print("Missing Library: %s"%err)
                        exit()
            print("Invalid Credentials: %s"%err)
            client = self.retryLogin(credentialsFile, WebDAVURL)
            return client

class Synchronous(): 

    def checkFile(self, client, remotePath):
        return client.check(remotePath)

        
    def uploadFile(self, client, remotePath, localPath):
        print("Uploading:\n %s \n\tto \n%s\n"%(localPath, remotePath))
        print("\nThis Could Take a Minute\n")
        try: 
            client.upload_sync(remotePath, localPath)
            print("Upload Successful!")
        except Exception as err:
            print(err)
            print("Failed to upload %s"%localPath)
            print("Check Your Credentials File")

