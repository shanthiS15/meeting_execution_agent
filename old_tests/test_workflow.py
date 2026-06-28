from agent import generate_workflow

workflow = generate_workflow(
    "UI Design",
    "Friday"
)

print("Generated Workflow:\n")

for step in workflow:
    print(step)