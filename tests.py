from functions.get_file_contents import get_file_content

file_contents = get_file_content("calculator", "main.py")
print(file_contents)

file_contents = get_file_content("calculator", "pkg/calculator.py")
print(file_contents)

file_contents = get_file_content("calculator", "/bin/cat")
print(file_contents)

file_contents = get_file_content("calculator", "pkg/does_not_exist.py")
print(file_contents)