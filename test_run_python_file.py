from functions.run_python_file import run_python_file

def main():
    working_dir = "calculator"

    print(run_python_file(working_dir, "main.py"))
    print(run_python_file(working_dir, "main.py", ["3 + 5"]))
    print(run_python_file(working_dir, "tests.py"))
    print(run_python_file(working_dir, "../main.py"))
    print(run_python_file(working_dir, "nonexistent.py"))
    print(run_python_file(working_dir, "lorem.txt"))

if __name__ == "__main__":
    main()