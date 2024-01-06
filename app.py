import requests
import subprocess
import json

# List of dictionaries with download links, file names, and setup flag
with open('output.json', 'r') as file:
    file_data = json.load(file)

def download_file(url, file_name):
    with requests.get(url, stream=True) as r:
        with open(file_name, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

def install_application(installer_path):
    subprocess.run(installer_path, shell=True)

# Download and optionally install applications from the download list
for app in file_data:
    download_file(app['url'], app['file_name'])
    if app['setup']:
        answer = input(f"Do you want to install {app['file_name']}? (yes/no): ").lower()
        if answer == 'yes':
            install_application(app['file_name'])
    else:
        print(f"{app['file_name']} downloaded but not set for installation.")
