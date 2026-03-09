import os
import shutil

SRC_DIR = r"D:\Working\Working Directory\Ai Project\Odint V1\Odint\odint-site\public"
DEST_DIR = r"D:\Working\Working Directory\Ai Project\Odint V2\images"

FILES = [
    "lucent-logo-v3.png",
    "globe.svg",
]

def main():
    os.makedirs(DEST_DIR, exist_ok=True)
    for name in FILES:
        src = os.path.join(SRC_DIR, name)
        dest = os.path.join(DEST_DIR, name)
        if os.path.exists(src):
            shutil.copyfile(src, dest)
            print(f"Copied {name}")
        else:
            print(f"Missing {name} at {src}")

if __name__ == "__main__":
    main()
