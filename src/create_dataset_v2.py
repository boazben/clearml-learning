from clearml import Dataset
import shutil
import os

shutil.copy("data/raw/people_v1.csv", "data/raw/people_v2.csv")

with open("data/raw/people_v2.csv", "a") as f:
    f.write("Eve,22,97\n")

dataset = Dataset.create(
    dataset_name="people_dataset_v2",
    dataset_project="ClearML Learning",
    parent_datasets=["ed617a76beab45d586cd4d9b44d3c59a"],
)

dataset.add_files("data/raw/people_v2.csv")
dataset.upload()
dataset.finalize()

print(f"Dataset created and uploaded successfully! ID: {dataset.id}")