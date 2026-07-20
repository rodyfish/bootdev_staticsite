import os
import shutil

def move_files(source_dir: str, target_dir: str, working_dir:str="."):
    working_dir_abs = os.path.abspath(working_dir)
    source_dir_abs = os.path.normpath(os.path.join(working_dir_abs, source_dir))
    valid_source_dir = os.path.commonpath([working_dir_abs, source_dir_abs]) == working_dir_abs
    target_dir_abs = os.path.normpath(os.path.join(working_dir_abs, target_dir))
    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir_abs]) == working_dir_abs

    if not valid_source_dir:
        raise Exception (f'Error: Cannot use source "{source_dir}" as it is outside the permitted working directory')
    
    if not valid_target_dir:
        raise Exception (f'Error: Cannot use target "{target_dir}" as it is outside the permitted working directory')
    
    if not os.path.isdir(source_dir):
        raise Exception("Source directory is not a valid path")

    shutil.rmtree(target_dir_abs)
    os.mkdir(target_dir_abs)

    source_paths = os.listdir(source_dir_abs)
    for source_path in source_paths:
        source_path_abs = os.path.join(source_dir_abs, source_path)
        
        if os.path.isfile(source_path_abs):
            test = shutil.copy(source_path_abs, os.path.join(target_dir_abs, source_path))
        elif os.path.isdir(source_path_abs):
            new_dir = os.path.join(target_dir_abs, source_path)
            os.mkdir(new_dir)
            move_files(source_path_abs, new_dir, working_dir)
   

    pass


def read_file(file_path: str, working_dir: str=".") -> str:

    working_dir_abs = os.path.abspath(working_dir)
    file_path_abs = os.path.normpath(os.path.join(working_dir_abs, file_path))
    valid_source_dir = os.path.commonpath([working_dir_abs, file_path_abs]) == working_dir_abs

    if not valid_source_dir:
        raise Exception (f'Error: Cannot use source "{file_path}" as it is outside the permitted working directory')
    
    if not os.path.isfile(file_path):
        raise Exception(f"sSource directory is not a valid file {file_path}")

   

    file = open(file_path_abs, "r", encoding="utf-8")
    content = file.read()
    return content


def write_file(working_dir: str, file_path: str, content: str) -> str:
    output = ""
    try:
        working_dir_abs = os.path.abspath(working_dir)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        
        if not valid_target_file:
            raise Exception (f'Cannot write to "{file_path}" as it is outside the permitted working directory')
        if os.path.isdir(target_file):
            raise Exception(f'Cannot write to "{file_path}" as it is a directory') 
        test = target_file.rsplit("/", 1)[0]
        os.makedirs(test, exist_ok=True)

        file = open(target_file, "w", encoding="utf-8")
        file.write(content)
        file.close()
        output = f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        output = f"Error: {e}"

    return output

def get_files_info(working_directory: str, directory: str = ".") -> list[str]:
    
    info: list[str] = []
    
    decorated_dir = "'"+directory+"'"
    if directory == ".":
        decorated_dir = "current"

    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

    if not valid_target_dir:
        raise Exception (f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
    if not os.path.isdir(target_dir):
        raise Exception(f'Error: "{directory}" is not a directory') 
    
    file_names = os.listdir(target_dir)
    records: list[str] = []

    for file_name in file_names:
        file_dir = os.path.join(target_dir, file_name)
        info.append(file_dir)
        
    
    return info
    


    

