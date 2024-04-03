import shutil
from pathlib import Path

import aiofiles
from fastapi import UploadFile

from nordic_realm.utils import generate_id


class DiskFileUpload:

    def __init__(self, file: UploadFile, auto_delete: bool = True):
        self.file = file
        self.disk_file: Path | None = None
        self.upload_id = generate_id(32)
        self.auto_delete = auto_delete

    def _create_tmp_rootpath(self):
        Path(f"/tmp/fastapi_uploads/{self.upload_id}").mkdir(parents=True, exist_ok=True)

    async def to_disk(self) -> "DiskFileUpload":
        self._create_tmp_rootpath()
        self.disk_file = Path(f"/tmp/fastapi_uploads/{self.upload_id}/{self.file.filename}")

        async with aiofiles.open(self.disk_file, 'wb') as out_file:
            while content := await self.file.read(50*1024*1024):  # async read chunk
                await out_file.write(content)  # async write chunk

        await self.file.close()

        return self

    def __del__(self):
        if self.auto_delete:
            shutil.rmtree(f"/tmp/fastapi_uploads/{self.upload_id}")
