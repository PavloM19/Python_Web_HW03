from pathlib import Path
import sys
import os
import shutil
import re
import concurrent.futures
import logging


dict_extentions = {
'images'    : ('jpeg', 'png', 'jpg', 'svg'),
'video'     : ('avi', 'mp4', 'mov', 'mkv'),
'documents' : ('doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx'),
'audio'     : ('mp3', 'ogg', 'wav', 'amr'),
'archives'  : ('zip', 'gz', 'tar', 'rar', '7z'),
'other'     : ()
}


def dict_translit():
    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = ("a", "b", "v", "g", "d", "e", "jo", "zh", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
                "f", "h", "ts", "ch", "sh", "sch", "", "y", "'", "e", "yu", "ya", "ie", "i", "ji", "g")
    TRANS = {}
    for i in range(len(CYRILLIC_SYMBOLS)):
        TRANS[CYRILLIC_SYMBOLS[i]] = TRANSLATION[i]
        TRANS[CYRILLIC_SYMBOLS[i].upper()] = TRANSLATION[i].upper()

    return TRANS

TRANS = dict_translit()

def translit(name): #transliteration KYR -> LAT 
    return name.translate(TRANS)


def normalize(name):
    name = translit(name)
    dot = name.rfind('.')
    if dot == -1:
        name_ = name
        ext = ''
    else:
        name_ = name[:dot]
        ext = name[dot:]

    name_ = re.sub(r'\W', '_', name_)

    return name_ + ext


def folder_check(path):
    logging.debug(f'folder_check for: {path}') #add
    with concurrent.futures.ThreadPoolExecutor() as executor:
        list_file = [x for x in path.iterdir() if x.is_file()] 
        for file in list_file:
            name_file = file.name        
            name_file = normalize(name_file)
            dot = name_file.rfind('.')

            if dot == -1: #move the file without the extension to the 'other' folder
                os.replace(file, dict_path['other'] + '\\' + name_file)
            else:            
                ext = name_file[dot+1:] #extension 

                for key in dict_extentions:
                    if ext in dict_extentions[key]:
                        if key == 'archives' and ext in ['zip', 'tar']:
                            shutil.unpack_archive(file, dict_path[key] + '\\' + name_file[:dot])

                        os.replace(file, dict_path[key] + '\\' + name_file)                        
                        found_extention.add(ext)
                        break
                else:
                    os.replace(file, dict_path['other'] + '\\' + name_file)
                    unknown_extention.add(ext)
            
        list_dir = [x for x in path.iterdir() if x.is_dir()]    
        for dir in list_dir:    
            if not path.name in dict_extentions:            
                executor.submit(folder_check, dir)

        # logging.debug(f'before rmdir({path})')
        # print(path, os.listdir(path))
        if not os.listdir(path):
            os.rmdir(path)
            # logging.debug(f'rmdir - {path}')


if __name__ == "__main__":
    # ----START----
    if len(sys.argv) != 2:
        print('Please pass on just one path')
        quit()
    print(sys.argv[0])
    current_path = Path(sys.argv[1])
    if not os.path.exists(current_path):
        print(f'{current_path} <- there is no such path')
        quit()

    found_extention = set()
    unknown_extention = set()
    dict_path = {} #dict for save paths

    for folder in dict_extentions:
            dict_path[folder] = os.path.abspath(current_path) + '\\' + folder #save path
            if not os.path.exists(current_path / folder):
                os.makedirs(current_path / folder)  #create folders for sorting, if they are not in the initial folder


    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')
    folder_check(current_path)

    print('---Done---')
    print('Found extentions: ', list(found_extention))
    print('Unknown extentions: ', list(unknown_extention))
