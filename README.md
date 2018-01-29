# move-folder-to-account

##Install
```
pip install -r requirements.txt
```

##Description
move-folder-to-account finds a top level folder named "migration" which should contain folders with username's of users in your enterprise as the folder's name. Then it transfers the contents to each user by inviting them as a co-owner and then dropping itself from the folder making the intended user the owner of the contents.

The use case this script was for when our Research File System (RFS) was being shut down. All files from RFS were uploaded to a centralized Box account and this script was used on that account to send the users their files on Box.
##Configuration
move-folder-to-account uses [`config.py`](config.py) as a configuration file. This configuration specifies the Box app's [JWT credentials](https://github.com/box-community/jwt-app-primer) as well as the runtime arguments.

* `user_id` specifies the user whose folders are to be renamed. 
* `base_folder_id` specifies the folder which holds all of the folders with usernames to migrate to. For example, if all of the folders are in a folder called "migration", you would find the id of the folder in the url of the page used to access the folder, and use that value as the `base_folder_id`. If the folders with usernames are at the top level of your account, use the value '0'.