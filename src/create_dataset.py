from clearml import Dataset


# get arsguments obout what files paths to add and what to remove - with flags: --a for add and --r for remove
import argparse
parser = argparse.ArgumentParser(description='Create a dataset with ClearML')
parser.add_argument('--a', '--add', nargs='+', help='Files to add to the dataset', required=False)
parser.add_argument('--r', '--remove', nargs='+', help='Files to remove from the dataset', required=False)
parser.add_argument('--p', '--parent_id', nargs='+', help='Parent dataset IDs to link to the new dataset', required=True)
parser.add_argument('--n', '--name', help='Name of the dataset to create', required=True)
args = parser.parse_args()

# create dataset
dataset = Dataset.create(
    dataset_name=args.n,
    dataset_project="ClearML Learning",
    parent_datasets=args.p if args.p else []
)

if args.a:
    for file in args.a:
        dataset.add_files(file)
if args.r:
    for file in args.r:
        dataset.remove_files(file)

dataset.upload()
dataset.finalize()
print(f"Dataset created and uploaded successfully! ID: {dataset.id}")


# # Example usage:
# # To create a dataset with files to add:
# # python src/create_dataset.py --n "more data to train" --p   ed617a76beab45d586cd4d9b44d3c59a --a data/raw/people_v1.csv

