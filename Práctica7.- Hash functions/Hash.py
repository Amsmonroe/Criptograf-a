import hashlib

def calculate_hash(file_path, hash_function):
    hash_func = hashlib.new(hash_function)
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            hash_func.update(chunk)
    return hash_func.hexdigest()

def main():
    file_paths = [
        "/P7 Hash/file1.pdf", "/P7 Hash/file2.txt",
        "/P7 Hash/file4.pdf", "/P7 Hash/file5.txt", 
        "/P7 Hash/file7.pdf", "/P7 Hash/file8.txt", "/P7 Hash/file10.pdf"
    ]
    
    for file_path in file_paths:
        print(f"Calculating hashes for {file_path}")
        sha224_hash = calculate_hash(file_path, "sha224")
        sha256_hash = calculate_hash(file_path, "sha256")
        sha384_hash = calculate_hash(file_path, "sha384")
        
        print(f"SHA-224: {sha224_hash}")
        print(f"SHA-256: {sha256_hash}")
        print(f"SHA-384: {sha384_hash}")
        print()

    main()
