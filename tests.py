from functions.get_files_info import get_files_info

stdout = get_files_info("calculator", ".")
print(f"Result for current directory:\n{stdout}")

stdout = get_files_info("calculator", "pkg")
print(f"Result for 'pkg' directory:\n{stdout}")

stdout = get_files_info("calculator", "/bin")
print(f"Result for '/bin directory:\n{stdout}")

stdout = get_files_info("calculator", "../")
print(f"Result for current directory:\n{stdout}")
