from functions.write_file_content import write_file_content

print(write_file_content("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
print(write_file_content("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
print(write_file_content("calculator", "/tmp/temp.txt", "this should not be allowed"))