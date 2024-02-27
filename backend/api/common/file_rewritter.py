import os
import mimetypes
import magic
import base64
import glob

from backend.api.config import settings


def rewrite_file(user, fields):
    out_path = {}
    for field in fields:
        attr = getattr(user, field)

        if not attr:
            continue

        for index, file_base64 in enumerate(attr):

            file_base64_decode = base64.b64decode(file_base64)
            format_file = magic.from_buffer(file_base64_decode, mime=True)
            extension = mimetypes.guess_extension(format_file)
            name = f'{user.get_username()}_{field}_{index}{extension}'
            tmp_filename = f'{user.get_username()}_{field}_{index}.*'
            path_to_file = os.path.join(settings.ABSPATH_UPLOAD_FOLDER, name)
            global_path_to_file = os.path.join(settings.GLOBAL_UPLOAD_FOLDER, name)

            del_files(path_to_file, tmp_filename)

            if not out_path.get(field):
                out_path[field] = []
            out_path[field].append(global_path_to_file)

            if os.path.exists(path_to_file):

                with open(path_to_file, 'rb') as f:
                    file_data = f.read()
                if file_base64_decode == file_data:
                    continue

            with open(path_to_file, 'wb') as f:
                f.write(file_base64_decode)

    return out_path


def del_files(path_to_save, filename):
    path = glob.glob(os.path.join(settings.ABSPATH_UPLOAD_FOLDER, filename))

    if path_to_save in path:
        path.remove(path_to_save)

    for file in path:
        os.remove(file)
