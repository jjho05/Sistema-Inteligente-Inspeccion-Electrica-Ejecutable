"""
File cleanup utility for removing old generated documents.
"""

from pathlib import Path
from datetime import datetime, timedelta
import os


def cleanup_old_files(directory: str = "data/generated", days: int = 120):
    """
    Remove files older than specified days from directory.
    
    Args:
        directory: Directory to clean
        days: Files older than this many days will be deleted
    """
    dir_path = Path(directory)
    
    if not dir_path.exists():
        print(f"Directory {directory} does not exist, skipping cleanup")
        return
    
    cutoff_date = datetime.now() - timedelta(days=days)
    deleted_count = 0
    
    print(f"🧹 Cleaning up files older than {days} days from {directory}...")
    
    for file_path in dir_path.glob("*"):
        if file_path.is_file():
            # Get file modification time
            file_mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
            
            if file_mtime < cutoff_date:
                try:
                    file_path.unlink()
                    deleted_count += 1
                    print(f"  ✓ Deleted: {file_path.name} (age: {(datetime.now() - file_mtime).days} days)")
                except Exception as e:
                    print(f"  ✗ Error deleting {file_path.name}: {e}")
    
    if deleted_count > 0:
        print(f"✓ Cleanup complete: {deleted_count} file(s) deleted")
    else:
        print("✓ No old files to delete")
