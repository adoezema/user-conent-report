import json
from arcgis import GIS

def get_folder_names(user):
    folder_names = [folder["title"] for folder in user.folders]
    folder_names.append(None)
    return folder_names

def get_user_content(user, folders):
    result = []
    data = {folder: user.items(folder=folder, max_items=200) for folder in folders} 
    for folder, content in data.items():
        for item in content:
            if (item.type == 'Feature Service') and ('Hosted' in item.url):
                info = {'Title': item.title, 'ID': item.id, 
                        'Item Page': f'https://gisportal.ohm-advisors.com/portal/home/item.html?id={item.id}'}
                result.append(info)
    return result


if __name__ == '__main__':
    gis = GIS(profile='adoezema_Portal')

    for user in gis.users.search():
        if user.fullName not in ['Austin Doezema', 'David Andrus', 'Francesca Ortisi', 'Jamie Lau', 'Jeff Evans',
                                'Jake Murawski', 'James Hainstock', 'Paul McCord', 'Michael Cousins']:
            print(f'{user.fullName}: {user.username}')
            folders = get_folder_names(user)
            hosted_services = get_user_content(user, folders)
            if hosted_services:
                print(json.dumps(hosted_services, indent=4))

