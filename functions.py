import datetime
import subprocess
from PIL import Image


class DateNotFoundException(Exception):
    pass


def get_photo_date_taken_heic(filepath):
    """Gets the date taken for a photo through a shell."""
    cmd = "mdls '%s'" % filepath
    output = subprocess.check_output(cmd, shell=True)
    lines = output.decode("ascii").split("\n")
    for l in lines:
        if "kMDItemContentCreationDate" in l:
            datetime_str = l.split("= ")[1]
            datetime_datetime = datetime.datetime.strptime(
                datetime_str, "%Y-%m-%d %H:%M:%S +0000"
            )
            return datetime_datetime
    raise DateNotFoundException(f"No EXIF date taken found for file {filepath}")


def get_photo_date_taken_jpg(filepath):
    exif = Image.open(filepath)._getexif()
    if not exif:
        raise Exception(f"Image {filepath} does not have EXIF data.")
    return exif[36867]


def get_photo_date_taken(filepath):
    extension = filepath.split(".")[-1]
    dict_sub_functions = {
        "heic": get_photo_date_taken_heic,
        "jpg": get_photo_date_taken_jpg,
    }
    return dict_sub_functions[extension](filepath)
