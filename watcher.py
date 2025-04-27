import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from embedder import generate_embedding
from opensearch_utils import create_index, index_document, delete_document
from config import data_folder
from datetime import datetime

class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith('.txt'):
            self.process(event.src_path)

    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith('.txt'):
            self.process(event.src_path)

    def on_deleted(self, event):
        if not event.is_directory and event.src_path.endswith('.txt'):
            filename = os.path.basename(event.src_path)
            delete_document(filename)
            print(f"Deleted from index: {filename}")

    def process(self, filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()
            embedding = generate_embedding(text)
            doc = {
                "content": text,
                "content_vector": embedding,
                "filename": os.path.basename(filepath),
                "timestamp": datetime.utcnow().isoformat()
            }
            index_document(os.path.basename(filepath), doc)
            print(f"Indexed: {filepath}")
        except Exception as e:
            print(f"Error processing {filepath}: {e}")

if __name__ == '__main__':
    os.makedirs(data_folder, exist_ok=True)
    create_index()

    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, path=data_folder, recursive=False)
    observer.start()
    print(f"Watching folder: {data_folder}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

