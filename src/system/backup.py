import os
import tarfile
from datetime import datetime
from pathlib import Path

def create_backup():
    """Create a timestamped .tar.gz of configs, models, runtime, and logs; clears the active log afterwards."""
    base_dir = Path(os.getcwd())
    backup_dir = base_dir / "backups"
    backup_dir.mkdir(exist_ok=True)

    # Use UTC for consistent timing
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    backup_path = backup_dir / f"backup_{timestamp}.tar.gz"

    # 1. Create the compressed backup
    with tarfile.open(backup_path, "w:gz") as tar:
        # Added "logs" to the folders being backed up
        for folder_name in ["configs", "models", "runtime", "logs"]:
            folder_path = base_dir / folder_name
            if folder_path.exists():
                # The arcname=folder_name keeps the folder structure clean inside the zip
                tar.add(str(folder_path), arcname=folder_name, recursive=True)
    
    # 2. Clear the active log file to save disk space
    # This happens ONLY after the backup above is safely created
    log_file = base_dir / "logs/bot.log"
    if log_file.exists():
        with open(log_file, "w") as f:
            f.truncate(0)
            
    return backup_path
