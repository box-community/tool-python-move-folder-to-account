# move-folder-to-account

## Install
```
pip install -r requirements.txt
```

## Description
move-folder-to-account finds a top level folder named "migration" which should contain folders with username's of users in your enterprise as the folder's name. Then it transfers the contents to each user by inviting them as a co-owner and then dropping itself from the folder making the intended user the owner of the contents.

The use case this script was for when our Research File System (RFS) was being shut down. All files from RFS were uploaded to a centralized Box account and this script was used on that account to send the users their files on Box.
## Configuration
move-folder-to-account uses JWT to authenticate to Box. For a primer on JWT, check out <a href="https://github.com/box-community/jwt-app-primer">this link</a>. Use the user_id field in config.py to specify where the migration files are hosted.

On the account that has the files to be transferred, make sure that the contents are in a file named "migration" and the sub-folders are named with the username's of the users to migrate to.
