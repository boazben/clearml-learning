from clearml import Dataset, Task
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle

task = Task.init(
    project_name="ClearML Learning",
    task_name="add more data for improved accuracy",
    task_type=Task.TaskTypes.training,
)

task.set_parent("238b9377421b4205b3cce3a4cedea742")

dataset = Dataset.get(
    dataset_name="more data to train",
    dataset_project="ClearML Learning",
    alias="training-data"
    )
local_path = dataset.get_local_copy()
print(f"Dataset local path: {local_path}")

df = pd.read_csv(f"{local_path}/people_v1.csv")
print(df)

X = df[["age", "score"]]
y = (df["score"] > 88).astype(int)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
model = RandomForestClassifier()
model.fit(X_train, y_train)

acc = accuracy_score(y_test, model.predict(X_test))
task.get_logger().report_scalar(title="Accuracy", series="test", value=acc, iteration=0)
print(f"Accuracy: {acc:.4f}")

with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

task.upload_artifact("model", "model.pkl")
task.close()