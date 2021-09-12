!NOTE! all the code would be uploaded in next couple of days after properly commenting the code

# PythonEasyGoogleWrapper
self-made light wrapper for Google API using Python

main file: `google_wrapup.py`

### Parts included:
- logger (enhanced `print()` function storing messages in a file)
- general Google Service (service setup)

### Specific services (checked already done and working, unchecked planned to make)
- [x] Drive API
- [ ] Google Photos API
- [ ] Google Spreadsheet API
- [ ] Google Calendar API
- [ ] Google Mail API
- [ ] Google Translator API

## How to use

1. Create project in [Google Developer Console](https://console.cloud.google.com/) and download OAuth2 JSON
2. place the JSON file in the same folder as your main project
3. when ititialising service class, place the name of this JSON file into `client_secret_file` argument 
````
service = GeneralService(app_type, client_secret_file, API_name, API_version, scopes)
````
where:
- `app_type` is only a describer to properly name the log message (for example: log for `app_type = 'Client'` initialised at 1st January 2000, the name would be `logClient_2000-01-01.txt`)
- API name, version and scopes may be found in the time of setting up the project, scopes as list

The class includes `refresh()` function, which refreshes OAuth token (you have to call it separately, when `service.cred.expired` turns into `True`).
 
 connection for the API itself is hidden under `service.communicate` object, logging using `log_message()` under `service.log`.

### Specific case - Google Drive
`DriveService` has pre-filled API version (`v3`), name (`drive`) and it's scope (`https://apis.google.com/auth/drive/`). You have to fill only `app_type` and `client_secret_file`. The class includes basic commands for Drive operations, like `search_in_folder(id)`, which provides list of all files in folder of given ID, or `upload(what, where, to)`, where `what` is the name of the file itself, `where` is a path to the file and `to` is an ID of target folder, or `download(what_id, what_name, where)`, where `where` is path to the folder to store downloaded files. You can also use `delete(id)`, where `id` is ID of the deleted file.

All these functions are called directly from `service`.
