import os
import sys
import time
import shutil
import zipfile

def create_folders(path):
    if not os.path.exists(path):
        os.makedirs(path)

def sync_files( source_file, target_file ):
    msg = ['','INSERT','UPDATE','ERROR ']
    try:
        if not os.path.exists( target_file):
            #shutil.copy2( source_file, target_file )
            with zipfile.ZipFile(target_file, 'w') as new_zip:
                new_zip.write(source_file, compress_type=zipfile.ZIP_DEFLATED)
            result = 1; # Insert
        else:
            dst_info = os.stat(target_file)
            src_info = os.stat(source_file)
            if( src_info.st_mtime - dst_info.st_mtime > 1 ):
                #shutil.copy2( source_file, target_file )
                time_stamp = time.localtime(os.path.getmtime(target_file))
                time_stamp = time.strftime("%Y.%m.%d.%H.%M.zip",time_stamp)
                shutil.move(target_file, target_file[:-3] + time_stamp)
                with zipfile.ZipFile(target_file, 'w') as new_zip:
                    new_zip.write(source_file, compress_type=zipfile.ZIP_DEFLATED)
                result = 2 # Update
            else:
                result = 0 # NoAction
    except:
        os.remove(target_file)
        result = 3
    if result == 0 :
        return ""
    else:
        print(msg[result] + '\t' + source_file)
        return time.strftime('%Y-%m-%d %H:%M') + '\t' + msg[result] + '\t' + source_file + '\n'

def check_files(source_folder, target_folder):
    for p, _, files in os.walk(os.path.abspath(source_folder)):
        for file in files:
            create_folders(p.replace(source_folder, target_folder))
            source_file_name = os.path.join(p, file)
            target_file_name = source_file_name.replace(source_folder, target_folder) + '.zip'
            log = sync_files(source_file_name, target_file_name)
            with open(target_folder + "\\Backup.log", 'a') as log_file:
                log_file.writelines(log)

def main(args):
    p1 = args[1].replace('\\','\\')
    p2 = args[2].replace('\\','\\')
    print('Backup: ',p1,' -> ',p2)
    check_files(p1,p2)
    return 0
 
if __name__ == '__main__':
    #sys.exit(main(sys.argv))
    main(["","G:\.shortcut-targets-by-id\0B-pBzsI00IsJajFYREw3QnlJTVE\SMS", "D:\BACKUP"])
 