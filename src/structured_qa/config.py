from pydantic import BaseModel, DirectoryPath, FilePath


class Config(BaseModel):
    input_file: FilePath
    output_dir: DirectoryPath
