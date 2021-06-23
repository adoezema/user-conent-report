import json
from arcgis import GIS
from datetime import datetime

def get_folder_names(user):
    folder_names = [folder["title"] for folder in user.folders]
    folder_names.append(None)
    return folder_names

def get_user_content(user, folders):

    def convert_date(ts):
        return datetime.strftime(datetime.utcfromtimestamp(ts/1000), '%m/%d/%Y')

    result = []
    data = {folder: user.items(folder=folder, max_items=200) for folder in folders} 
    for folder, content in data.items():
        for item in content:
            if (item.type == 'Feature Service') and ('Hosted' in item.url):
                info = {'Title': item.title, 'ID': item.id, 'Created': convert_date(item.created), 
                'Modified': convert_date(item.modified), 'Item Page': item.homepage}
                result.append(info)
    return result


if __name__ == '__main__':
    gis = GIS(profile='adoezema_Portal')

    with open(f'.\data\c{datetime.strftime(datetime.now(),"%Y%m%d")}_Portal_Hosted_Services.json', 'w') as outfile:
        portal_findings = []
        for user in gis.users.search():
            if user.fullName not in ['Austin Doezema', 'David Andrus', 'Francesca Ortisi', 'Jamie Lau', 'Jeff Evans',
                                    'Jake Murawski', 'James Hainstock', 'Paul McCord', 'Michael Cousins']:
                user_content = {
                    'Name': user.fullName,
                    'Username': user.username,
                    'Hosted_Services': [],
                }

                folders = get_folder_names(user)
                hosted_services = get_user_content(user, folders)
                if hosted_services:
                    user_content['Hosted_Services'].append(hosted_services)
                portal_findings.append(user_content)
        json.dump(portal_findings, outfile)

