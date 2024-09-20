from pathlib import Path


class Directory:
    def __init__(self):
        self.base_dir = Path(__file__).resolve().parent.parent

        self.json_dir = self.base_dir / "json"
        self.images_dir = self.base_dir / "images"

    def create_folders(self) -> None:
        folders = [
            self.json_dir,
            self.images_dir,
        ]
        for fol in folders:
            try:
                fol.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                print(f"Failed to create directory {fol}: {e}")


directory = Directory()
directory.create_folders()
