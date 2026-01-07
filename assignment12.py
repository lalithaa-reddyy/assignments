import threading
import traceback

print_lock = threading.Lock()

def read_file(file_path, errors):
    try:
        with open(file_path, "r") as f:
            content = f.read()
        with print_lock:
            print(f"Contents of {file_path}:\n{content}\n", flush=True)
    except Exception as e:
        with print_lock:
            print(f"Error reading {file_path}: {e}")
            traceback.print_exc()
        errors.append((file_path, str(e))) 

def main():
    files = ["file1.txt", "file2.txt", "file3.txt", "file4.txt"]
    threads = []
    errors = []

    for file_path in files:
        t = threading.Thread(target=read_file, args=(file_path, errors))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print("All files processed.")
    if errors:
        print("Some files could not be read:")
        for file_path, error_msg in errors:
            print(f"{file_path}: {error_msg}")

if __name__ == "__main__":
    main()
