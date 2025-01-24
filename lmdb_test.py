import lmdb

def count_lmdb_samples(lmdb_path):
    # Open the LMDB environment in readonly mode
    env = lmdb.open(lmdb_path, readonly=True)

    total_samples = 0

    with env.begin() as txn:
        # Iterate through the keys in the LMDB database
        cursor = txn.cursor()
        for key, value in cursor:
            # Check if the key is an image key (starts with 'image-')
            if key.decode().startswith('image-'):
                total_samples += 1

    env.close()

    print(f"Total number of samples in LMDB: {total_samples}")

# Example usage
lmdb_train_path = 'E:/THESIS/merged_dataset/lmdb_dataset/val'
count_lmdb_samples(lmdb_train_path)
