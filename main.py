# -- Imports
import os
import pandas as pd
from functions import get_photo_date_taken
import shutil
import os
from pathlib import Path

# -- Constants
RELEVANT_EXTENSIONS = ["heic", "jpg"]
DIRECTORY_PHOTOS = "D:/iCloud/Photos/Shared"

# -- 1. Get files and filter for relevant extensions
path_files = Path(DIRECTORY_PHOTOS)

list_relevant_files = []
for ext in RELEVANT_EXTENSIONS:
    paths = [*path_files.glob(f"**/*.{ext}")]
    list_relevant_files.extend(paths)

# -- 2. Loop, store data
list_data = []
for f in list_relevant_files:
    dt_photo = get_photo_date_taken(f)
    list_out = [f, dt_photo]
    list_data.append(list_out)

# -- 3. To DataFrame, enrich with relevant information
df_photos = pd.DataFrame(list_data, columns=["source_file", "dt_photo_taken"])
df_photos["target_dir"] = df_photos["dt_photo_taken"].apply(
    lambda dt: dt.strftime("%Y_%b")
)
df_photos["destination_file"] = df_photos["target_dir"] + "/" + df_photos["source_file"]

# -- 4. Move file to new location
for dir in df_photos["target_dir"].unique():
    if dir not in list_files:
        os.mkdir(dir)

for src, dest in zip(df_photos["source_file"], df_photos["destination_file"]):
    shutil.move(src, dest)