import asyncio
import aiofiles
import os
from pathlib import Path

async def read_file(file_path: str) -> dict:
    """
    Reads a file asynchronously and returns its content as a dictionary.
    
    Args:
        file_path (str): The path to the file to be read.

    Returns:
    dictronary with given keys:
    - path: File path in string format.
    - name: File name in string format.
    - content: File content in string format.
    """
    if file_path:
        file_path = file_path.strip()
    try:
        async with aiofiles.open(file=file_path, mode="r") as f:
            content = await f.read()
            file_name = os.path.basename(file_path)
            return {"path": file_path, "name": file_name, "content": content}
    except FileNotFoundError:
        return {"error": "FileNotFoundError", "path": file_path}
    except PermissionError:
        return {"error": "NotEnoughPermissions", "path": file_path}
    

async def write_file(file_path: str, content: str, mode: str = "overwrite") -> dict:
    """
    Write a file asynchronously and returns response status as a dictionary.
    
    Args:
        file_path (str): The path to the file to be write.
        content (str): The string that file will contain.
        mode (str): 
        - "overwrite" (changes file content if exists if not create new with this content)
        - "append" (append file content if exists if not create new with this content)
        - "fail_if_exists" (if file exists cancel operation if not create new with this content)
    Returns:
    dictronary with given keys:
    - status: Action status in string format.
    - path: File path in string format.

    Permissions:
    Needed
    """
    
    if mode == "fail_if_exists":
        option = "x"
    elif mode == "overwrite":
        option = "w"
    else:
        option = "a"


    try:
        async with aiofiles.open(file = file_path, mode = option) as f:
            await f.write(content)
            if option == "w" or option == "x":
                return {"status": "File written!", "path": file_path}
            if option == "a":
                return {"status": "Appended content to file!", "path": file_path}
    except FileExistsError:
        return {"status": "File already exists!", "path": file_path}