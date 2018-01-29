from __future__ import print_function, unicode_literals

import pprint
from datetime import datetime

from boxsdk import Client, JWTAuth
from boxsdk.exception import BoxAPIException
from boxsdk.object.collaboration import CollaborationRole
from boxsdk.util.translator import Translator

import config

oauth = JWTAuth(
    client_id=config.client_id,
    client_secret=config.client_secret,
    enterprise_id=config.enterprise_id,
    jwt_key_id=config.jwt_key_id,
    rsa_private_key_file_sys_path=config.rsa_private_key_file_sys_path
)


# Create an authenticated client that can interact with the Box Content API
client = Client(oauth)

userId = config.user_id

owner = client.user(user_id=userId)

oauth.authenticate_app_user(owner)

failed_users = []  # here is our list of users whose auto-accept were likely off


def run_collab(box_client):
    global migration_folder, collaboration

    migration_folder = client.folder(folder_id=config.base_folder_id).get()

    users = migration_folder.get_items(limit=1000, offset=0)  # get the items from inside
    for user in users:  # go through the folders in migration
        new_name = config.new_folder_prefix + user.name
        collab_folder = user.rename(new_name)  # rename the folder
        f.write('\nFolder {0} renamed'.format(collab_folder.get()['name']))
        print('\nFolder {0} renamed'.format(collab_folder.get()['name']))

        box_users = box_client.users(filter_term=user.name + "@")
        if len(box_users) == 0:
            f.write('\nNo Box users found for ' + user.name)
            print('No Box users found for ' + user.name)
            continue
        if len(box_users) > 1:
            f.write('\nMultiple Box users found for ' + user.name)
            print('Multiple Box users found for ' + user.name)
            continue

        first_user = box_users[0]
        f.write('\nCreating a collaboration with ' + user.name + ' (login: ' + first_user.login + ')...')
        print('Creating a collaboration with ' + user.name + ' (login: ' + first_user.login + ')...')

        try:
            collaboration = collab_folder.add_collaborator(first_user.login, CollaborationRole.CO_OWNER)  # add a
            # collaborator using the folder name
        except BoxAPIException as box:
            if box.status == 204:  # success
                f.write('\nCreated a collaboration with ' + user.name + '\n')
                print('Created a collaboration with ' + user.name)
                pass
            elif box.status == 400:  # auto-accept is off
                failed_users.append(user.name)
                f.write('\nFAILED to create the collaboration with ' + user.name + ': ' + box.message + '\n')
                print('FAILED to create the collaboration with ' + user.name + ': ' + box.message)
                collab_folder.rename(user.name)
                continue
                pass
            elif box.status == 409:  # auto-accept is off
                failed_users.append(user.name)
                f.write('\nFAILED to create the collaboration with ' + user.name + ': ' + box.message + '\n')
                print('FAILED to create the collaboration with ' + user.name + ': ' + box.message)
                collab_folder.rename(user.name)
                continue
                pass
            else:
                raise

        try:
            collaboration.update_info(role=CollaborationRole.OWNER)  # make the collaborator the owner
        except BoxAPIException as box:
            if box.status == 204:  # success
                f.write('\nModified the collaboration to OWNER\n')
                print('Modified the collaboration to OWNER')
                pass
            elif box.status == 400:  # auto-accept collaboration is likely off
                failed_users.append(user.name)
                f.write('\nFAILED to modify the collaboration to OWNER for ' + user.name + ': ' + box.message + '\n')
                print('FAILED to modify the collaboration to OWNER for ' + user.name + ': ' + box.message)
                collab_folder.rename(user.name)
                pass
            else:
                raise

        json_response = box_client.make_request(  # get the collaboration id
            'GET',
            box_client.get_url('folders', collab_folder.id, 'collaborations'),
        ).json()

        id_num = [Translator().translate(item['type'])(None, item['id'], item) for item in
                  json_response['entries']]  # translate the id for the machine
        collab = id_num[0]  # grab the ID

        try:
            json_send = box_client.make_request(  # delete the collab_id
                'DELETE',
                box_client.get_url('collaborations', collab.id),
            )
            pprint.pprint(json_send)
        except BoxAPIException as box:
            if box.status == 204:  # success
                pass
            else:
                raise
        print("\n")


time = (datetime.now().strftime("_%m-%d-%Y"))
filename = "RFSMigration" + time + ".txt"
f = open(filename, "w+")
f = open(filename, "a+")
run_collab(client)
f.write("\n\nFailed users were:")
print("Failed users were:")
f.write("\n")
print("\n")
for f_user in failed_users:  # print failed users
    f.write(f_user + "\n")
    print(f_user + "\n")
f.close()
