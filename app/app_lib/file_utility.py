import os
import uuid
import logging
import aiofiles
import aiofiles.os as aioos

from fastapi import UploadFile, File
from typing import List


# Setting Logger
LOGGER = logging.getLogger(__name__)


class FileUtility():
    def __init__(self, file_path):
        """ ex file_path: images/ """
        self.file_path = file_path

        if not os.path.exists(self.file_path):
            os.makedirs(self.file_path)

    def _generate_hex_uuid(self) -> str:
        """ Create unique uuid for using """
        return uuid.uuid4().hex

    async def save_file(self, file_name: str, in_file: UploadFile = File(...)):
        """ Async saving file in to images folder """
        LOGGER.info(f"Saved image name: {file_name}")

        save_file_path = f"{self.file_path}{file_name}"

        async with aiofiles.open(save_file_path, 'wb') as out_file:
            content = await in_file.read()  # async read
            await out_file.write(content)  # async write

        return file_name

    async def save_files(self, in_files: List[UploadFile] = File(...), use_hex: bool = True):
        """ Async saving file in to images folder """
        LOGGER.info(f"Save image in {self.file_path}")

        res_data = []
        for file in in_files:
            if use_hex:
                # Split input filename and extention and generate new unique file name with uuid
                new_uuid = self._generate_hex_uuid()
                _, ext = os.path.splitext(file.filename)
                new_filename = new_uuid + ext
            else:
                new_filename = file.filename
            _ = await self.save_file(new_filename, file)
            res_data.append(new_filename)

        return res_data

    async def delete_file(self, file_name: str):
        """ Async delete file from images folder """
        LOGGER.info(f"Delete image name list: {file_name}")

        delete_file_path = f"{self.file_path}{file_name}"

        if os.path.exists(delete_file_path):
            # File exist and delete
            await aioos.remove(delete_file_path)
        else:
            LOGGER.warning(f"Skip delete, file is not exist, full file path: {delete_file_path}")
            pass

        return

    async def delete_files(self, file_name_list: list):
        """ Async delete file list """
        for file_name in file_name_list:
            await self.delete_file(file_name)

        return
