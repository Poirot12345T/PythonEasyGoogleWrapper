# PythonEasyGoogleWrapper
light wrapper for Google API using Python

This repository tries to make easier working with Google API as I found their own library for Python unusable without any further work, so this set of files tries to help with using this API

There are many apps connectted to Google account (like Google Drive, Google Photos, Google Docs, Spreadsheets, etc.) and sometimes it is easier to use API instead of the GUI Google developed (for example, when syncing many photos, uploading bigger amounts of data on Google Drive repeatedly, and so on).

To make orientation a little easier, each class (representing connection to API for each Google app) is placed in its own file, so you can import only the API handler you want.

### Parts included:
- logger (enhanced `print()` function storing messages in a file)
- general Google Service (service setup)

### Specific services (checked already done and working, unchecked planned to make)
- [x] Drive API
- [x] Google Photos API
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
- `app_type` is only a describer to properly name the log message (for example: log for `app_type = 'Client'` initialised at 1st May 2000, the name would be `logClient_2000-05-01.txt`)
- API name, version and scopes may be found in the time of setting up the project, scopes as list

The class includes `refresh()` function, which refreshes OAuth token (you have to call it separately, when `service.cred.expired` turns into `True`).
 
 connection for the API itself is hidden under `service.communicate` object, logging using `log_message()` under `service.log`.

### Specific case - Google Drive
`DriveService` has pre-filled API version (`v3`), name (`drive`) and it's scope (`https://apis.google.com/auth/drive/`). You have to fill only `app_type` and `client_secret_file`. 

The class includes basic commands for Drive operations, like `search_in_folder(id)`, which provides list of all files in folder of given ID, or `upload(what, where, to)`, where `what` is the name of the file itself, `where` is a path to the file and `to` is an ID of target folder, or `download(what_id, what_name, where)`, where `where` is path to the folder to store downloaded files. You can also use `delete(id)`, where `id` is ID of the deleted file.

### Specific case - Google Photos
`PhotoService` has prefilled API version(`v1`), name(`photoslibrary`) and it's scopes(`https://apis.google.com/auth/photoslibrary/`, `https://apis.google.com/auth/photoslibrary.sharing/`), again only `app_type` and `client_secret_file` needed to fill in.

Functions made:
- `get_user_albums()` returns all the juicy output of API about user albums, including their names, links, IDs, link & ID of cover photo in form of list of dicts.
- `get_album_info()` returns the same as `get_user_albums()`, but only for one album specified by it's ID as dict.
- `create_album()` creates album in Google Photos and returns the same info as `get_album_info()` for newly created album.
- `share_album()` shares the album, using two arguments as voluntary (collaboration and comments)
- `unshare_album()` unshares the album

All these functions in specific cases are called directly from `service`, for example `service.search_in_folder(id)`.
