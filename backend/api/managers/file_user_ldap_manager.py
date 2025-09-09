import ctypes
import mimetypes
import base64
import magic
import glob
import os

from api.common.exception import LDAPExceptionFlaskError
from api.managers import ldap_manager as managers
from api.conf import settings


class ImageFileManager:
    @staticmethod
    def mimetypes(file_bytes):
        format_file = magic.from_buffer(file_bytes, mime=True)
        extension = mimetypes.guess_extension(format_file) if not format_file == 'image/webp' else '.webp'

        return format_file, extension

    def save_image(self, uid, file_bytes):
        file_b64 = file_bytes

        try:
            format_file, extension = self.mimetypes(file_b64)
        except ctypes.ArgumentError:
            raise LDAPExceptionFlaskError(result=400, message="file bytes mymetypes!")

        name = f"{uid}{extension}"
        path = os.path.join(settings.ABSPATH_UPLOAD_FOLDER, name)
        global_path = os.path.join(settings.GLOBAL_UPLOAD_FOLDER, name)
        self.remove_files(settings.ABSPATH_UPLOAD_FOLDER, f"{uid}.*")

        with open(path, 'wb') as f:
            f.write(file_b64)

        return global_path

    def remove_files(self, path_to_save=None, filename=None):
        path = glob.glob(os.path.join(settings.ABSPATH_UPLOAD_FOLDER, filename))

        if path_to_save in path:
            path.remove(path_to_save)

        for file in path:
            os.remove(file)


class FileUserRetrieveLDAPManager(managers.RetrieveLDAPManager):
    search_filter = "(objectClass=Person)"


class FileUserModifyLDAPManager(managers.ModifyLDAPManager):
    search_filter = "(objectClass=Person)"


