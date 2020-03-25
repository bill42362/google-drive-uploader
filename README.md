# google-drive-uploader
Enable upload files to google drive.

# Setup API client secrets
* Setup a **CLI cert** from [here](https://console.developers.google.com/flows/enableapi?apiid=drive). 
* Or follow this [medium](https://medium.com/@newlife617/%E7%A8%8B%E5%BC%8F-python-google-drive-api-eebeb58876ef).
* Save your cert file as `client_secrets.json`.

# Usage
```
$ pip3 install --upgrade pydrive
$ python3 main.py [file1] [file2] [...]
```
