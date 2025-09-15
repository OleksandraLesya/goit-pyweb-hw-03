# file_sorter.py

import argparse
import shutil
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from logger import logger  # Import shared logger


def copy_file(file_path: Path, output_base_dir: Path):
    """
    Copies file to a folder named after its extension in the target directory.
    """
    ext = file_path.suffix.lower()[1:] or "others"
    destination_folder = output_base_dir / ext
    destination_folder.mkdir(parents=True, exist_ok=True)
    destination_path = destination_folder / file_path.name

    try:
        shutil.copy2(file_path, destination_path)
        logger.info(f"Copied: {file_path} -> {destination_path}")
    except Exception as e:
        logger.error(f"Failed to copy {file_path}: {e}")


def main():
    """
    Main function to parse arguments and sort files using threads.
    """
    parser = argparse.ArgumentParser(description="Multithreaded file sorter by extension.")
    parser.add_argument("source_dir", type=Path, help="Path to the source directory.")
    parser.add_argument("-o", "--output_dir", type=Path, default=Path("dist"), help="Path to output directory (default: ./dist)")
    args = parser.parse_args()

    source_dir = args.source_dir
    output_dir = args.output_dir

    if not source_dir.exists() or not source_dir.is_dir():
        logger.error(f"Source directory does not exist or is not a directory: {source_dir}")
        return

    output_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"Sorting files from: {source_dir}")
    logger.info(f"Output directory: {output_dir}")

    files = [f for f in source_dir.rglob("*") if f.is_file()]

    with ThreadPoolExecutor(max_workers=10) as executor:
        for file_path in files:
            executor.submit(copy_file, file_path, output_dir)

    logger.info("Sorting complete.")


if __name__ == "__main__":
    main()
