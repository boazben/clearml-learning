from clearml import Task

task = Task.init(
    project_name="ClearML Learning",
    task_name="execute-remotely-demo",
    task_type=Task.TaskTypes.training,
)

print("Step 1 [LOCAL] - preparing the parameters - runs locally!")
params = {"learning_rate": 0.01, "epochs": 5}
task.connect(params)
print(f">>> [LOCAL] params: {params}")

print("[LOCAL] goning to jump to remotly agent...")
task.execute_remotely(queue_name="default", clone=False)

print("[REMOTE] - training the model - runs remotely on the agent!")
import time
for epoch in range(params["epochs"]):
    fake_loss = 1.0 / (epoch + 1)
    task.get_logger().report_scalar(
        title="Loss", series="train", value=fake_loss, iteration=epoch
    )
    print(f">>> [REMOTE] Epoch {epoch+1}: loss={fake_loss:.4f}")
    time.sleep(1)

print(">>> [REMOTE] Done!")