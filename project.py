# The os module is perfect for filesystem operations like "walking" throught directories and files
# Although there are many ways of achieving the same effect, a good way to loop over the filesystem is using `os.walk()`
import os
import sqlite3


user_data = input("Enter the dirctory you want to traverse: ")

# Persist the data into a dictionary. Since file paths are unique you can use those as dictionary keys
file_metadata = {}

for root, directories, files in os.walk(user_data):
    for _file in files:
        #print(f"File found: {_file}")

        # Update the loop so that it shows the absolute path of a file ignoring directories 
        # which we aren't going to track
        full_path = os.path.join(root, _file)
        #print(f"File found: {full_path}")

        # Update the loop to include the file size
        size = os.path.getsize(full_path)
        #print(f"Size: {size}b - File: {full_path}")

        file_metadata[full_path] = size

#print(file_metadata)

connection = sqlite3.connect('sample.db')
cursor = connection.cursor()

create_table_query = 'create table files (id integer primary key, filepath text, size integer)'
cursor.execute(create_table_query)
connection.commit()

insert_query = 'insert into files (filepath, size) values (?,?)'
for metadata in file_metadata.items():
	cursor.execute(insert_query, metadata)
connection.commit()

select_query = 'select filepath, size from files where id >=20'
result = cursor.execute(select_query)
for result in result:
	print(result)

select_query = 'select filepath, size from files where size <= 1000'
result = cursor.execute(select_query)
for result in result:
	print(result)