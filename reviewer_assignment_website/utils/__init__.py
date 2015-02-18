"""Functions that are used by many apps"""

import uuid


def get_file_path(filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return filename