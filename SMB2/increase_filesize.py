#!/usr/bin/env python
import sys
import string

from smb2pack import config
from smb2pack import smb2
from smb2pack import constants


if __name__ == "__main__": 
        
        const = constants.smb2Constants()
        
        smb2client = smb2.SMB(config.remoteIP,config.smbport)
        
        smb2client.login(config.username, config.password)
        
        ntstatus,sid,tid = smb2client.tree_connect("\\\\"+config.remoteIP+"\\"+config.share)
        ################## 1st rename ################
        ntstatus,fileId, filesize = smb2client.create(tid,"test1.txt","oplock=0","accessmask=65664",\
                           "fileattr=0","sharemode=7","disposition=1", "createoptions=2097216"\
                           ,"DHNQ","MXAC","QFID")
        if ntstatus != 0:
        	  print "file open failed"
        	  exit()
        
        ntstatus = smb2client.set_info(tid, fileId,"infotype="+str(const.SMB2_0_INFO_FILE),\
                   "fileinfoclass="+str(const.FileEndOfFileInformation))
        if ntstatus == 0:
        	  print "file delete successful"
        else:
           print "file delete failed"
        ntstatus = smb2client.close(tid ,fileId)
        
        ntstatus = smb2client.tree_disconnect(tid)
        
        ntstatus = smb2client.logoff()


