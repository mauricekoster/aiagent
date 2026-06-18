from functions.get_file_content import get_file_content

content = get_file_content("calculator", "main.py")
print(content)

content = get_file_content("calculator", "pkg/calculator.py")
print(content)

content = get_file_content("calculator", "/bin/cat")
print(content)

content = get_file_content("calculator", "pkg/does_not_exist.py")
print(content)
