import os
import sys
import time
import shutil

def create_folders(path):
    if not os.path.exists(path):
        os.makedirs(path)

def sync_files( source_file, target_file ):
    msg = ['','INSERT','UPDATE']
    print(source_file, '->', target_file)
    if not os.path.exists( target_file ):
        shutil.copy2( source_file, target_file )
        result = 1; # Insert
    else:
        dst_info = os.stat(target_file)
        src_info = os.stat(source_file)
        if( src_info.st_mtime - dst_info.st_mtime > 1 ):
            shutil.copy2( source_file, target_file )
            result = 2 # Update
        else:
            result = 0 # NoAction
    if result == 0 :
        return ""
    else:
        return time.strftime('%Y-%m-%d %H:%M') + '\t' + msg[result] + '\t' + source_file + '\n'

def check_files(source_folder, target_folder):
    log = []
    for p, _, files in os.walk(os.path.abspath(source_folder)):
        for file in files:
            create_folders(p.replace(source_folder, target_folder))
            source_file_name = os.path.join(p, file)
            target_file_name = source_file_name.replace(source_folder, target_folder)
            print(source_file_name, '->', target_file_name)
            log.append(sync_files(source_file_name, target_file_name))
    with open(target_folder + "\\Backup.log", 'a') as log_file:
        for item in log:
            log_file.writelines(item)

def main(args):
    p1 = args[1].replace('\\','\\')
    p2 = args[2].replace('\\','\\')
    print('Backup: ',p1,' -> ',p2)
    check_files(p1,p2)
    return 0
 
if __name__ == '__main__':
    sys.exit(main(sys.argv))
    #main(["","D:\LH\WEB", "G:\Meu Drive\Backup"])