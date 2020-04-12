import os
import io
import pickle
from gzip import GzipFile
import builder
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseUpload


"""Google Drive Access"""

class GoogleDrive:
    def __init__(self, persist_dir, conf):
        print(conf)
        self._dir = persist_dir
        self._scopes = conf['scopes']
        self._tokenfile = conf['token_file']
        self._clientfile = conf['creds_file']
        self._query_fields = conf['query_fields']
        self._app_props = {
            'appName': conf['app_name']
        }
        builder.mkdirs(self._tokenfile)
        self._creds = self._load_creds()
        if not self._creds or not self._creds.valid:
            self._creds = self._authorize(self._creds)
        self._service = build('drive', 'v3', credentials=self._creds)
        self._mkdirs(dirs = self._dir.split('/'))

    def outdir(self):
        return self._dir

    def _load_creds(self):
        if not os.path.exists(self._tokenfile):
            return None
        else:
            with open(self._tokenfile, 'rb') as token:
                return pickle.load(token)
    
    def _authorize(self, creds):
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                self._clientfile, self._scopes)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(self._tokenfile, 'wb') as token:
            pickle.dump(creds, token)
        os.chmod(self._tokenfile, 0o600)

        return creds

    def _dir_exists(self, dirname):
        query = "name='{}' and mimeType='application/vnd.google-apps.folder'".format(dirname)
        response = self._service.files() \
            .list(q=query,
                  spaces='drive',
                  fields=self._query_fields) \
            .execute()
        
        found = None
        for item in response.get('files', []):
            app_props = item.get('appProperties', {})
            app_name = app_props.get('appName', None)
            if app_name and app_name==self._app_props['appName'] and not item.get('trashed'):
                found = item

        return found

    def _create_dir(self, dirname, parents=[]):
        file_metadata = {
            'name': dirname,
            'mimeType': 'application/vnd.google-apps.folder',
            'appProperties': self._app_props,
            'parents': parents
        }
        d = self._service.files() \
                .create(body=file_metadata,
                        fields='id, name, parents') \
                .execute()
        print('Created dir: {} (id={}, parents={})'.format(d.get('name', ''), d.get('id', ''), d.get('parents', [])))
        return d.get('id')

    def _mkdirs(self, dirs=[]):
        parents = []
        for d in dirs:
            if not self._dir_exists(d):
                id = self._create_dir(d, parents[-1:])
                parents.append(id)
        return parents

    def write(self, content, filename):
        parts = filename.split('/')
        dirs = parts[:-1]
        name = parts[-1]

        self._mkdirs(dirs)
        if dirs:
            found = self._dir_exists(dirs[-1])
            parents = [found.get('id')]

            mime_type = 'application/x-compressed'
            file_metadata = {
                'name': name + '.gz',
                'parents': parents,
                'mimeType': mime_type
                }
            content_bytes = io.BytesIO(''.encode('utf-8'))
            gzip_obj = GzipFile(filename=name, fileobj=content_bytes, mode='wb')
            gzip_obj.write(content.encode('utf-8'))
            gzip_obj.close()
            media = MediaIoBaseUpload(content_bytes, mimetype=mime_type)
            print("Writing to 'drive:" + filename + ".gz'")
            file = self._service.files() \
                .create(body=file_metadata,
                        media_body=media,
                        fields='id') \
                .execute()