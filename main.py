
import threading
import subprocess
import time
import webbrowser

def run_upload_img_captioner():
    subprocess.run(["python3.10", "uploaded_image_captioner.py"])

def run_url_img_captioner_automated():
    subprocess.run(["python3.10", "url_img_captioner_automated.py"])

def run_local_img_captioner_automated():
    subprocess.run(["python3.10", "local_img_captioner_automated.py"])

if __name__ == "__main__":
    threads = [
    threading.Thread(target=run_upload_img_captioner),
    threading.Thread(target=run_url_img_captioner_automated),
    threading.Thread(target=run_local_img_captioner_automated)
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()