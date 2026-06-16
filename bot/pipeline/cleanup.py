import shutil
import os


def cleanup_workspace(workspace: str):
    """Apaga workspace temporário."""
    if workspace and os.path.exists(workspace):
        shutil.rmtree(workspace)


def cleanup_file(file_path: str):
    """Apaga arquivo único."""
    if file_path and os.path.exists(file_path):
        os.remove(file_path)
