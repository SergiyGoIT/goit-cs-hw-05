import argparse
import asyncio
import logging
from pathlib import Path
import aiofiles
import aiofiles.os
import shutil


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("file_sorter.log"), logging.StreamHandler()]
)


async def copy_file(file_path: Path, output_dir: Path):
    try:
        ext = file_path.suffix[1:] or "no_extension"
        target_folder = output_dir / ext
        await aiofiles.os.makedirs(target_folder, exist_ok=True)

        target_path = target_folder / file_path.name

        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, shutil.copy2, file_path, target_path)

        logging.info(f"Copied: {file_path} → {target_path}")
    except Exception as e:
        logging.error(f"Error copying {file_path}: {e}")


async def read_folder(source_dir: Path, output_dir: Path):
    tasks = []

    for path in source_dir.rglob("*"):
        if path.is_file():
            tasks.append(copy_file(path, output_dir))

    await asyncio.gather(*tasks)


def main():
    parser = argparse.ArgumentParser(description="Async file sorter")
    parser.add_argument("source", type=str, help="Source folder")
    parser.add_argument("output", type=str, help="Output folder")
    args = parser.parse_args()

    source_path = Path(args.source)
    output_path = Path(args.output)

    if not source_path.exists() or not source_path.is_dir():
        logging.error(f"Source path does not exist or is not a directory: {source_path}")
        return

    asyncio.run(read_folder(source_path, output_path))


if __name__ == "__main__":
    main()
