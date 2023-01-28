import os
import time
import shutil

last_backup = 0

threshold = 30000
take_lines = 100000

source_file = 'file.txt'
small_file = 'checker-contacts.txt'
large_file = 'large.txt'
copy_file = 'checker-contacts-copy.txt'
backup_file = 'large_backup.txt'
backup_folder = 'backups'
viber = 'viber_contacts.txt'
if not os.path.exists(backup_folder):
    os.makedirs(backup_folder)

if not os.path.exists(small_file) and not os.path.exists(large_file) :
        with open(source_file, 'r') as source:
            lines = source.readlines()
            num_lines = len(lines)
            if take_lines > 0 and take_lines < num_lines:
                with open(small_file, 'w') as small:
                    small.writelines(lines[:take_lines])
                with open(copy_file, 'w') as copy:
                    copy.writelines(lines[:take_lines])
                with open(large_file, 'w') as large:
                    large.writelines(lines[take_lines:])
                with open(backup_file, 'w') as backup:
                    pass

limit = 140000

while True:
    try:
        time.sleep(2)
        with open(small_file, 'r') as small:
            small_lines = len(small.readlines())
        with open(large_file, 'r') as large:
            large_lines = len(large.readlines())
        if small_lines < threshold:
            if small_lines + take_lines < limit:
                copy = shutil.copy2('checker-contacts.txt', 'checker-contacts-copy.txt')
                with open(copy, 'a') as small_copy, open(large_file, 'r') as large:
                    small_copy.writelines(large.readlines()[:take_lines])
                    small_copy.close()
                    os.replace(copy_file, small_file)
                with open(large_file, 'r') as large:
                    lines = large.readlines()
                with open(large_file, 'w') as large:
                    large.writelines(lines[take_lines:])
                with open(large_file, 'r') as large:
                    lines = large.readlines()
                    large_lines = len(lines)
                    if large_lines == 0 :
                        break
        current_time = int(time.time())
        if current_time - last_backup > 3600:
            if os.path.exists('large.txt'):
                shutil.copy2(large_file, os.path.join(backup_folder, large_file + 'backup' + str(current_time)+'.txt'))
                last_backup = current_time
            viber = 'viber_contacts.txt'
            if os.path.exists('viber_contacts.txt'):
                shutil.copy2(viber, os.path.join(backup_folder, viber + 'backup' + str(current_time)+'.txt'))
                last_backup = current_time
    except (FileNotFoundError, PermissionError) as e:
        print(f"An error occurred while accessing the files: {e}")
        time.sleep(4)
