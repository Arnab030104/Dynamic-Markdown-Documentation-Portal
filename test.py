from pathlib import Path

inter = input("enter path :")
base = Path("content").resolve()

target = (base / f"{inter}.md")
target2 = (base / f"{inter}.md").resolve()


print(f"this is the output : {target}")
print(f"this is the output : {target2}")