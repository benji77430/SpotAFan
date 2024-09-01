import os
import socket
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from pydub import AudioSegment
import platform
import subprocess
import requests
import yt_dlp
from translate import Translator
import random
import json
from pydub.playback import play
import datetime
import time
import getpass
# Configuration de l'API YouTube
YOUTUBE_API_SERVICE_NAME = 'youtube'
CONNECTED = False
YOUTUBE_API_VERSION = 'v3'
API_KEY = ""
#default language
LANG = 'en'



    
#translation module
def translation(text):
    translator= Translator(to_lang=LANG)
    return translator.translate(text)



#colors codes
class Colors:
    """ ANSI color codes """
    BLACK = "\033[0;30m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    BROWN = "\033[0;33m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    LIGHT_GRAY = "\033[0;37m"
    DARK_GRAY = "\033[1;30m"
    LIGHT_RED = "\033[1;31m"
    LIGHT_GREEN = "\033[1;32m"
    YELLOW = "\033[1;33m"
    LIGHT_BLUE = "\033[1;34m"
    LIGHT_PURPLE = "\033[1;35m"
    LIGHT_CYAN = "\033[1;36m"
    LIGHT_WHITE = "\033[1;37m"
    BOLD = "\033[1m"
    FAINT = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    NEGATIVE = "\033[7m"
    CROSSED = "\033[9m"
    END = "\033[0m"

#configuration variables
UPLOAD = ""
CONFIG = []

home_dir = os.path.expanduser("~")

# Determine the operating system
system = platform.system()
print(system)

# Construct the path to the Music directory based on the operating system
if system == "Windows":
    MUSIC_PATH = os.path.join(home_dir, "Music")
    APPDATA = os.getenv('APPDATA')
    STORAGE = os.path.join(APPDATA,"SpotAFan")
    print("Windows detected")
elif system == "Darwin":  # macOS
    MUSIC_PATH = os.path.join(home_dir, "Musique")
    STORAGE = os.path.join("SpotAFan","config")
    print("MacOS detected")

elif system == "Linux":
    MUSIC_PATH = os.path.join(home_dir, "Musique")
    STORAGE = os.path.join("SpotAFan","config") 
    print("LINUX detected")

else:
    raise OSError(f"Unsupported operating system: {system}")
if not os.path.exists(STORAGE):
    os.makedirs(STORAGE)

#log module
def log(log):
    print(f'{log}                                                                                                            ',end='\r')
    log = str(log).replace('\033[0;30m','').replace('\033[0;31m','').replace('\033[0;32m','').replace('\033[0;33m','').replace('\033[0;34m','').replace('\033[0;35m','').replace('\033[0;36m','').replace('\033[0;37m','').replace('\033[1;30m','').replace('\033[1;31m','').replace('\033[1;32m','').replace('\033[1;33m','').replace('\033[1;34m','').replace('\033[1;35m','').replace('\033[1;36m','').replace('\033[1;37m','').replace('\033[1m','').replace('\033[2m','').replace('\033[3m','').replace('\033[4m','').replace('\033[5m','').replace('\033[7m','').replace('\033[9m','').replace('\033[0m','')
    write = f""" {datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")} | {log} \n"""
    with open(os.path.join(STORAGE,'SpotAFan.log'),'a', encoding='utf-8') as f:
        f.write(write)
def just_log(log):                                                                                                        
    log = str(log)
    write = f""" {datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")} | {log} \n"""
    with open(os.path.join(STORAGE,'SpotAFan.log'),'a', encoding='utf-8') as f:
        f.write(write)

#settings loading and creation
settings_file = os.path.join(STORAGE,'settings.json')
if not os.path.exists(settings_file):
    LANG = input('enter your lang as fr, en etc.. > ')
    upload = input(Translator(to_lang=LANG).translate('do you want to automaticaly send report when the app crash ? ')+' (y/N) ')
    if "y" in upload.lower():
        upload = "ok"
    else:
        upload = "no"
    print(upload)
    path = input(f'{Colors.CYAN}┌──<[{Colors.RED}{getpass.getuser()}@SpotAFan{Colors.CYAN}]{Colors.END} ~ {Colors.RED}{MUSIC_PATH}{Colors.END} \n{Colors.CYAN}└──╼ ${Colors.END} {Translator(to_lang=LANG).translate('please enter path to install music (nothing for default music folder)')} ─╼ ')
    if path == "":
        choice = input(f"""
1) {CONFIG[0]}

2) {MUSIC_PATH}

{Translator(to_lang=LANG).translate('enter the number of the path to use > ')}""")
        if choice == "1":
            path = CONFIG[0]
        else:
            path = MUSIC_PATH
    api = input(f'{Colors.CYAN}┌──<[{Colors.RED}{getpass.getuser()}@SpotAFan{Colors.CYAN}]{Colors.END} ~ {Colors.RED}{path}{Colors.END} \n{Colors.CYAN}└──╼ ${Colors.END} {Translator(to_lang=LANG).translate('please enter your google youtube data V3 api key')} ─╼ ')
    if api == "":
        api = API_KEY
    settings = {
        "path": path,
        "api_key": api,
        'upload': upload,
        'lang': LANG
    } 
    with open(settings_file, 'w') as f:        
        json.dump(settings, f, indent=4)
        CONFIG = [path,API_KEY]  
        UPLOAD = upload 
        
else:
    try:
        with open(settings_file, 'r') as f:
            settings = json.load(f)
            CONFIG.append(settings['path'])
            CONFIG.append(settings['api_key'])
            UPLOAD = settings['upload']
            LANG = settings['lang']
    except Exception as e:
        LANG = input('enter your lang as fr, en etc.. > ')
        if LANG == "":
            LANG = "en"
        upload = input(Translator(to_lang=LANG).translate('do you want to automaticaly send report when the app crash ? ')+' (y/N) ')
        if "y" in upload.lower():
            upload = "ok"
        else:
            upload = "no"
        print(upload)
        path = input(f'{Colors.CYAN}┌──<[{Colors.RED}{getpass.getuser()}@SpotAFan{Colors.CYAN}]{Colors.END} ~ {Colors.RED}{MUSIC_PATH}{Colors.END} \n{Colors.CYAN}└──╼ ${Colors.END} {Translator(to_lang=LANG).translate('please enter path to install music (nothing for default music folder)')} ─╼ ')
        if path == "":
            path = MUSIC_PATH
        api = input(f'{Colors.CYAN}┌──<[{Colors.RED}{getpass.getuser()}@SpotAFan{Colors.CYAN}]{Colors.END} ~ {Colors.RED}{path}{Colors.END} \n{Colors.CYAN}└──╼ ${Colors.END} {Translator(to_lang=LANG).translate('please enter your google youtube data V3 api key')} ─╼ ')
        if api == "":
            api = API_KEY
        settings = {
            "path": path,
            "api_key": api,
            'upload': upload,
            'lang': LANG
        } 
        with open(settings_file, 'w') as f:        
            json.dump(settings, f, indent=4)
            CONFIG = [path,API_KEY]  
            UPLOAD = upload  

class Text:
    file = f'{STORAGE}//{LANG}.json'
    translations = {
        "download_music": {},
        "list_and_play_music": {},
        "delete_music": {},
        "settings": {},
        "list_last_log": {},
        "send_report": {},
        "exit": {},
        "no_internet_connection": {},
        "press_number_of_music_to_delete": {},
        "deleting": {},
        "skipped": {},
        "press_number_of_music_to_start": {},
        "next": {},
        "please_enter_valid_number": {},
        "playing": {},
        "enter_valid_query": {},
        "enter_music_name": {},
        "no_videos_found": {},
        "enter_video_number_to_download": {},
        "invalid_number": {},
        "download_complete": {},
        "enter_language": {},
        "auto_send_report": {},
        "enter_install_music_path": {},
        "enter_api_key": {},
        "log_no_log": {},
        "report_sent": {},
        "restart": {},
        "ctrl c" : {},
        "leave" : {}
    }

    if os.path.exists(file):
        with open(file, 'r') as f:
            data = json.load(f)
            for text in data:
                translations[text] = data[text]
    else:
        print(translation("downloading language !")+"                                ",end="\r")
        # Populate translations using the translation function
        for key in translations:
            for lang in LANG:
                translations[key] = translation({
                    "download_music": "Download music",
                    "list_and_play_music": "List and play music",
                    "delete_music": "Delete music",
                    "settings": "Settings",
                    "list_last_log": "open logs",
                    "send_report": "Send report",
                    "exit": "Exit",
                    "no_internet_connection": "NO INTERNET CONNECTION",
                    "press_number_of_music_to_delete": "Press the number of the music to delete > ",
                    "deleting": "Deleting",
                    "skipped": "Skipped!",
                    "press_number_of_music_to_start": "Press the number of the music to start with > ",
                    "next": "Next!",
                    "please_enter_valid_number": "Please enter a valid number",
                    "playing": "Playing :",
                    "enter_valid_query": "Please enter a valid query!",
                    "enter_music_name": "Enter the name of the music > ",
                    "no_videos_found": "No videos found for this query.",
                    "enter_video_number_to_download": "Enter the number of the video to download (or press Enter to cancel) > ",
                    "invalid_number": "Invalid number.",
                    "download_complete": "Download complete!",
                    "enter_language": "Enter your language as fr, en etc.. > ",
                    "auto_send_report": "Do you want to automatically send a report when the app crashes?",
                    "enter_install_music_path": "Please enter path to install music (leave empty for default music folder) > ",
                    "enter_api_key": "Please enter your Google YouTube Data V3 API key > ",
                    "log_no_log": "No log!",
                    "report_sent": "Report sent!",
                    "restart": "Restart needed tou should restart the APP !",
                    "ctrl c": "'you can press Ctrl + C to skip !'",
                    "leave" : "press y to leave > "
                }[key])
        with open(file,'w') as f:
            json.dump(translations,f,indent=4)

       
    @staticmethod
    def get_text(key):
        return Text.translations.get(key, {})


def log(log):
    print(f'{log}                                                                                                            ',end='\r')
    log = str(log).replace('\033[0;30m','').replace('\033[0;31m','').replace('\033[0;32m','').replace('\033[0;33m','').replace('\033[0;34m','').replace('\033[0;35m','').replace('\033[0;36m','').replace('\033[0;37m','').replace('\033[1;30m','').replace('\033[1;31m','').replace('\033[1;32m','').replace('\033[1;33m','').replace('\033[1;34m','').replace('\033[1;35m','').replace('\033[1;36m','').replace('\033[1;37m','').replace('\033[1m','').replace('\033[2m','').replace('\033[3m','').replace('\033[4m','').replace('\033[5m','').replace('\033[7m','').replace('\033[9m','').replace('\033[0m','').replace(f'{Colors.CYAN}┌──<[{Colors.RED}{getpass.getuser()}@SpotAFan{Colors.CYAN}]{Colors.END} ~ {Colors.RED}{CONFIG[0]}{Colors.END}','').replace(f'\n{Colors.CYAN}└──╼ ${Colors.END}','')
    write = f""" {datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")} | {log} \n"""
    with open(os.path.join(STORAGE,'SpotAFan.log'),'a', encoding='utf-8') as f:
        f.write(write)
just_log('start')

#see log module
def list_log():
    if not os.path.exists(os.path.join(STORAGE,'SpotAFan.log')):
        log(Text.get_text('log_no_log'))
        return 
    os.startfile(os.path.join(STORAGE,'SpotAFan.log'))
    
#terminal cleaner module
def clear():
    if os.name =="nt":
        os.system('cls')
    else:
        os.system('clear')
        
#bug report module
def upload_to_server(filepath):
        for _ in range(10):
            try:
                url = "https://discord.com/api/webhooks/1271476798839849052/njuW-tsaDgb7pq2_KiIvwLkIDKHPHer3nx1ovc4RcaLXIkiUATOg68wF-q032QHpS6nK"
                files = {'file': open(filepath, 'rb')}
                r = requests.post(url, files=files)
                if r.status_code == 200:
                    return
            except: 
                print('probably 429 error retrying in 0.1s')
                time.sleep(0.1)
def send_report():
    if os.path.exists(os.path.join(STORAGE,getpass.getuser()+'.log')):
        os.remove(os.path.join(STORAGE,getpass.getuser()+'.log'))
    if os.path.exists(os.path.join(STORAGE,'SpotAFan.log')):
        log('log file exist !')
        os.rename(os.path.join(STORAGE,'SpotAFan.log'),os.path.join(STORAGE,getpass.getuser()+'.log'))
        upload_to_server(os.path.join(STORAGE,getpass.getuser()+'.log'))
        os.rename(os.path.join(STORAGE,getpass.getuser()+'.log'),os.path.join(STORAGE,'SpotAFan.log'))

        log(f'report sent !')
    else:
        log('no log !')
        


#settings update module
def setting():
    global CONFIG, LANG, UPLOAD
    print(f'''

{Colors.CYAN}( path ){Colors.END} ─╼ {Colors.BOLD}{Colors.LIGHT_RED}{CONFIG[0]}{Colors.END}

{Colors.CYAN}( lang ){Colors.END} ─╼ {Colors.BOLD}{Colors.LIGHT_RED}{LANG}{Colors.END}

{Colors.CYAN}( API  ){Colors.END} ─╼ {Colors.BOLD}{Colors.LIGHT_RED}{CONFIG[1]}{Colors.END}

{Colors.CYAN}( AUTO REPORT ){Colors.END} ─╼ {Colors.BOLD}{Colors.LIGHT_RED}{str(UPLOAD)}{Colors.END}
''')
    

    LANG = input(Text.get_text('enter_language')+" ")
    if LANG == "":
        LANG = "en"
    upload = input(Text.get_text('auto_send_report')+" (y/N) ")
    if "y" in upload.lower():
        upload = "ok"
    else:
        upload = "no"
    print(upload)
    path = input(f'{Colors.CYAN}┌──<[{Colors.RED}{getpass.getuser()}@SpotAFan{Colors.CYAN}]{Colors.END} ~ {Colors.RED}{MUSIC_PATH}{Colors.END} \n{Colors.CYAN}└──╼ ${Colors.END} {Text.get_text('enter_install_music_path')} ─╼ ')
    if path == "":
        choice = input(f"""
1) {CONFIG[0]}

2) {MUSIC_PATH}

{Colors.CYAN}┌──<[{Colors.RED}{getpass.getuser()}@SpotAFan{Colors.CYAN}]{Colors.END} ~ {Colors.RED}{MUSIC_PATH}{Colors.END} \n{Colors.CYAN}└──╼ ${Colors.END} """)
    if choice == "1":
        path = CONFIG[0]
    else:
        path = MUSIC_PATH
    api = input(f'{Colors.CYAN}┌──<[{Colors.RED}{getpass.getuser()}@SpotAFan{Colors.CYAN}]{Colors.END} ~ {Colors.RED}{path}{Colors.END} \n{Colors.CYAN}└──╼ ${Colors.END} {Text.get_text('enter_api_key')} ─╼ ')
    if api == "":
        api = CONFIG[1]
    settings = {
        "path": path,
        "api_key": api,
        'upload': upload,
        'lang': LANG
    } 
    with open(settings_file, 'w') as f:        
        json.dump(settings, f, indent=4)
        CONFIG = [path,API_KEY]  
        UPLOAD = upload
    

    
#GUI 
def ascii(i=random.randint(0,4)):
    ascii =[r"""
  ********                    **       **     ********                   
 **//////  ******            /**      ****   /**/////                    
/**       /**///**  ******  ******   **//**  /**        ******   ******* 
/*********/**  /** **////**///**/   **  //** /*******  //////** //**///**
////////**/****** /**   /**  /**   **********/**////    *******  /**  /**
       /**/**///  /**   /**  /**  /**//////**/**       **////**  /**  /**
 ******** /**     //******   //** /**     /**/**      //******** ***  /**
////////  //       //////     //  //      // //        //////// ///   // 

""",
r"""

  _// //                      _//        _/       _////////                   
_//    _//                    _//       _/ //     _//                         
 _//      _/ _//     _//    _/_/ _/    _/  _//    _//         _//    _// _//  
   _//    _/  _//  _//  _//   _//     _//   _//   _//////   _//  _//  _//  _//
      _// _/   _//_//    _//  _//    _////// _//  _//      _//   _//  _//  _//
_//    _//_// _//  _//  _//   _//   _//       _// _//      _//   _//  _//  _//
  _// //  _//        _//       _// _//         _//_//        _// _///_///  _//
          _//                                                                 

""",r"""
.oPYo.                 o       .oo  ooooo              
8                      8      .P 8  8                  
`Yooo. .oPYo. .oPYo.  o8P    .P  8 o8oo   .oPYo. odYo. 
    `8 8    8 8    8   8    oPooo8  8     .oooo8 8' `8 
     8 8    8 8    8   8   .P    8  8     8    8 8   8 
`YooP' 8YooP' `YooP'   8  .P     8  8     `YooP8 8   8 
:.....:8 ....::.....:::..:..:::::..:..:::::.....:..::..
:::::::8 ::::::::::::::::::::::::::::::::::::::::::::::
:::::::..::::::::::::::::::::::::::::::::::::::::::::::
""",

r"""      #######                                       ##            ##### ##                      
    /       ###                                  /####         ######  /### /                   
   /         ##                          #      /  ###        /#   /  /  ##/                    
   ##        #                          ##         /##       /    /  /    #                     
    ###                                 ##        /  ##          /  /                           
   ## ###           /###     /###     ########    /  ##         ## ##       /###   ###  /###    
    ### ###        / ###  / / ###  / ########    /    ##        ## ##      / ###  / ###/ #### / 
      ### ###     /   ###/ /   ###/     ##       /    ##        ## ###### /   ###/   ##   ###/  
        ### /##  ##    ## ##    ##      ##      /      ##       ## ##### ##    ##    ##    ##   
          #/ /## ##    ## ##    ##      ##      /########       ## ##    ##    ##    ##    ##   
           #/ ## ##    ## ##    ##      ##     /        ##      #  ##    ##    ##    ##    ##   
            # /  ##    ## ##    ##      ##     #        ##         #     ##    ##    ##    ##   
  /##        /   ##    ## ##    ##      ##    /####      ##    /####     ##    /#    ##    ##   
 /  ########/    #######   ######       ##   /   ####    ## / /  #####    ####/ ##   ###   ###  
/     #####      ######     ####         ## /     ##      #/ /    ###      ###   ##   ###   ### 
|                ##                         #                #                                  
 \)              ##                          ##               ##                                
                 ##                                                                             
                  ##                                                                            

"""
]
    print(f'''\n\n\n\n{Colors.BOLD}{Colors.YELLOW}{ascii[i]}{Colors.END}''')


def check_internet_connection(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error as ex:
        just_log(f"Aucune connexion Internet détectée : {ex}")
        return False
#delete music
def delete_music(music_path):
    clear();ascii(random.randint(0,2))
    files = os.listdir(music_path)
    musics = []
    print(f' [A] > {Colors.GREEN}ALL{Colors.END} ')

    for music in files:
        if str(music).endswith('mp3') or str(music).endswith('mp4'):
            musics.append(music)
    for i, file in enumerate(musics):
        print(f" [{i+1}] > {Colors.GREEN}{file}{Colors.END}")

    choice = input(f'{Colors.CYAN}┌──<[{Colors.RED}{getpass.getuser()}@SpotAFan{Colors.CYAN}]{Colors.END} ~ {Colors.RED}{CONFIG[0]}{Colors.END} \n{Colors.CYAN}└──╼ ${Colors.END} {Text.get_text("press_number_of_music_to_delete")} ')
    clear();ascii(2)
    if not choice:
        return
    if 'a' in choice.lower():
        for music in musics:
            try:
                song = AudioSegment.from_mp3(os.path.join(music_path,music))
                log(f'{Colors.CYAN}┌──<[{Colors.RED}{getpass.getuser()}@SpotAFan{Colors.CYAN}]{Colors.END} ~ {Colors.RED}{CONFIG[0]}{Colors.END} \n{Colors.CYAN}└──╼ ${Colors.END} {Colors.CYAN}{Text.get_text("deleting")} {music}{Colors.END}\n')
                os.remove(song)
            except:
                log(f'{Colors.CYAN}┌──<[{Colors.RED}{getpass.getuser()}@SpotAFan{Colors.CYAN}]{Colors.END} ~ {Colors.RED}{CONFIG[0]}{Colors.END} \n{Colors.CYAN}└──╼ ${Colors.END} {Colors.YELLOW}{Text.get_text("skipped")}{Colors.END}\n')
    else:
        try:
            choice = int(choice)-1
        except:
            log(f"{Colors.RED} {Text.get_text('please_enter_valid_number')} {Colors.END}")
        if choice >= len(musics):
            log(f"{Colors.RED} {Text.get_text('please_enter_valid_number')} {Colors.END}")
        file = musics[choice]
        file_path = os.path.join(music_path, file)
        log(f'{Colors.CYAN}┌──<[{Colors.RED}{getpass.getuser()}@SpotAFan{Colors.CYAN}]{Colors.END} ~ {Colors.RED}{CONFIG[0]}{Colors.END} \n{Colors.CYAN}└──╼ ${Colors.END} {Colors.CYAN}{Text.get_text("deleting")} {musics[choice]}{Colors.END}\n')
        os.remove(file_path)

#list and play musics
        
def list_music(music_path):
    clear();ascii(random.randint(0,2))
    files = os.listdir(music_path)
    musics = []
    print(f' [A] > {Colors.GREEN}ALL{Colors.END} ')

    for music in files:
        if str(music).endswith('mp3') or str(music).endswith('mp4'):
            musics.append(music)
    for i, file in enumerate(musics):
        print(f" [{i+1}] > {Colors.GREEN}{file}{Colors.END}")

    choice = input(f'{Colors.CYAN}┌──<[{Colors.RED}{getpass.getuser()}@SpotAFan{Colors.CYAN}]{Colors.END} ~ {Colors.RED}{CONFIG[0]}{Colors.END} \n{Colors.CYAN}└──╼ ${Colors.END} {Text.get_text("press_number_of_music_to_start")} ')
    clear();ascii(2)
    if not choice:
        return
    if 'a' in choice.lower():
        for music in musics:
            clear();ascii(2)
            print(Text.get_text('ctrl c'))
            
            try:
                song = AudioSegment.from_mp3(os.path.join(music_path,music))
                log(f'{Colors.CYAN}┌──<[{Colors.RED}{getpass.getuser()}@SpotAFan{Colors.CYAN}]{Colors.END} ~ {Colors.RED}{CONFIG[0]}{Colors.END} \n{Colors.CYAN}└──╼ ${Colors.END} {Colors.CYAN} {music}{Colors.END}\n')
                just_log(f'playing {music}')
                play(song)
            except KeyboardInterrupt:
                log(f'{Colors.CYAN}┌──<[{Colors.RED}{getpass.getuser()}@SpotAFan{Colors.CYAN}]{Colors.END} ~ {Colors.RED}{CONFIG[0]}{Colors.END} \n{Colors.CYAN}└──╼ ${Colors.END} {Colors.YELLOW}{Text.get_text("skipped")}{Colors.END}\n')
                time.sleep(0.2)
                

    else:
        try:
            choice = int(choice)-1
        except:
            log(f"{Colors.RED} {Text.get_text('please_enter_valid_number')} {Colors.END}")
        if choice >= len(musics):
            log(f"{Colors.RED} {Text.get_text('please_enter_valid_number')} {Colors.END}")
        file = musics[choice]
        file_path = os.path.join(music_path, file)
        play_music(file_path,musics[choice])
        just_log(f'playing {musics[choice]}')


def play_music(path,name):
    try:
        # for playing mp3 file
        try:
            song = AudioSegment.from_mp3(path)
            print(f'{Colors.CYAN}┌──<[{Colors.RED}{getpass.getuser()}@SpotAFan{Colors.CYAN}]{Colors.END} ~ {Colors.RED}{CONFIG[0]}{Colors.END} \n{Colors.CYAN}└──╼ ${Colors.END} {Colors.CYAN}{Text.get_text("playing")} {name}{Colors.END}\n')
            play(song)
        except Exception as e:
            just_log(f"Error playing music in terminal starting in a media player : {str(e)}")
            try:
                if system == "Windows":
                    os.startfile(path)
                    log(f'{Colors.CYAN}┌──<[{Colors.RED}{getpass.getuser()}@SpotAFan{Colors.CYAN}]{Colors.END} ~ {Colors.RED}{CONFIG[0]}{Colors.END} \n{Colors.CYAN}└──╼ ${Colors.END} {Colors.CYAN}{Text.get_text("playing")} {name}{Colors.END}\n')
                elif system == "Darwin":  # macOS
                    subprocess.run(["open", path])
                    log(f'{Colors.CYAN}┌──<[{Colors.RED}{getpass.getuser()}@SpotAFan{Colors.CYAN}]{Colors.END} ~ {Colors.RED}{CONFIG[0]}{Colors.END} \n{Colors.CYAN}└──╼ ${Colors.END} {Colors.CYAN}{Text.get_text("playing")} {name}{Colors.END}\n')
                elif system == "Linux":
                    subprocess.run(["xdg-open",path])
                    log(f'{Colors.CYAN}┌──<[{Colors.RED}{getpass.getuser()}@SpotAFan{Colors.CYAN}]{Colors.END} ~ {Colors.RED}{CONFIG[0]}{Colors.END} \n{Colors.CYAN}└──╼ ${Colors.END} {Colors.CYAN}{Text.get_text("playing")} {name}{Colors.END}\n')
                else:
                    raise OSError(f"Unsupported operating system: {system}")
            except Exception as e:
                log(f"An error occurred while trying to open the file: {e}")
    except Exception as e:
        just_log(e)

def download_music_with_ytdlp(video_url, download_path):
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
    except Exception as e:
        just_log(f'error {str(e)}')

def search_videos_on_youtube(query, api_key, max_results=10):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=api_key)
    search_response = youtube.search().list(
        q=query,
        part='id,snippet',
        maxResults=max_results
    ).execute()
    videos = []
    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            videos.append({
                'title': search_result['snippet']['title'],
                'videoId': search_result['id']['videoId']
            })
    return videos

def download_music():
    clear();ascii(random.randint(0,3))
    query = input(f"{Colors.CYAN}┌──<[{Colors.RED}{getpass.getuser()}@SpotAFan{Colors.CYAN}]{Colors.END} ~ {Colors.RED}{CONFIG[0]}{Colors.END} \n{Colors.CYAN}└──╼ ${Colors.END} {Text.get_text("enter_music_name")} ")
    if not query:
        log(f"{Colors.RED}{Text.get_text("no_videos_found")}{Colors.END}")
        return
    api_key = CONFIG[1]
    try:
        videos = search_videos_on_youtube(query, api_key)
        if not videos:
            log(f"{Colors.RED}){Text.get_text('no_videos_found')}{Colors.END}")
            return
        for i, video in enumerate(videos):
            print(f"{Colors.GREEN}[{i}] > {video['title']}{Colors.END}")
        choice = input(f"{Colors.CYAN}┌──<[{Colors.RED}{getpass.getuser()}@SpotAFan{Colors.CYAN}]{Colors.END} ~ {Colors.RED}{CONFIG[0]}{Colors.END} \n{Colors.CYAN}└──╼ ${Colors.END} {Text.get_text("enter_video_number_to_download")} ")
        if not choice:
            return
        try:
            choice = int(choice)
            if choice < 0 or choice >= len(videos):
                print(f"{Colors.RED}{Text.get_text('invalid_number')}{Colors.END}")
                return
        except ValueError:
            print(f"{Colors.RED}{Text.get_text('please_enter_valid_number')}{Colors.END}")
            return
        video_url = f"https://www.youtube.com/watch?v={videos[choice]['videoId']}"
        download_path = CONFIG[0]
        download_music_with_ytdlp(video_url, download_path)
        log(f"{Colors.GREEN}{Text.get_text('download_complete')}{Colors.END}")
    except HttpError as e:
        just_log(f"Une erreur s'est produite lors de la recherche sur YouTube : {str(e)}")

def menu():
    while True:
        CONNECTED = check_internet_connection()

        clear()
        ascii(random.randint(0,3))
        if CONNECTED:
            print(f"""
            {Colors.BOLD}{Colors.LIGHT_RED}|   {Colors.END}{Colors.PURPLE}[ 1 ]{Colors.END} ─╼ {Colors.BOLD}{Colors.YELLOW}{Text.get_text("download_music")}        {Colors.END}{Colors.BOLD}
            {Colors.BOLD}{Colors.LIGHT_RED}|   {Colors.END}{Colors.PURPLE}[ 2 ]{Colors.END} ─╼ {Colors.BOLD}{Colors.YELLOW}{Text.get_text("list_and_play_music")}   {Colors.END}{Colors.BOLD}
            {Colors.BOLD}{Colors.LIGHT_RED}|   {Colors.END}{Colors.PURPLE}[ 3 ]{Colors.END} ─╼ {Colors.BOLD}{Colors.YELLOW}{Text.get_text("delete_music")}          {Colors.END}{Colors.BOLD}
            {Colors.BOLD}{Colors.LIGHT_RED}|   {Colors.END}{Colors.PURPLE}[ 4 ]{Colors.END} ─╼ {Colors.BOLD}{Colors.YELLOW}{Text.get_text("settings")}              {Colors.END}{Colors.BOLD}
            {Colors.BOLD}{Colors.LIGHT_RED}|   {Colors.END}{Colors.PURPLE}[ 5 ]{Colors.END} ─╼ {Colors.BOLD}{Colors.YELLOW}{Text.get_text("list_last_log")}         {Colors.END}{Colors.BOLD}
            {Colors.BOLD}{Colors.LIGHT_RED}|   {Colors.END}{Colors.PURPLE}[ 6 ]{Colors.END} ─╼ {Colors.BOLD}{Colors.YELLOW}{Text.get_text("send_report")}           {Colors.END}{Colors.BOLD}
            {Colors.BOLD}{Colors.LIGHT_RED}|   {Colors.END}{Colors.PURPLE}[ 7 ]{Colors.END} ─╼ {Colors.BOLD}{Colors.YELLOW}{Text.get_text("exit")}                  {Colors.END}{Colors.BOLD}

        """)
            choice = input(f'{Colors.CYAN}┌──<[{Colors.RED}{getpass.getuser()}@SpotAFan{Colors.CYAN}]{Colors.END} ~ {Colors.RED}{CONFIG[0]}{Colors.END} \n{Colors.CYAN}└──╼ ${Colors.END} ')
            try:
                choice = int(choice)
            except:
                print(f"{Colors.RED}{Text.get_text('please_enter_valid_number')}{Colors.END}")
            try:
                if choice == 1:
                    CONNECTED = check_internet_connection
                    if not CONNECTED:
                        log(f'{Colors.RED}{Text.get_text('no_internet_connection')}{Colors.END}')
                        exit()
                    download_music()
                elif choice == 2:
                    list_music(CONFIG[0])
                elif choice == 3:
                    delete_music(CONFIG[0])
                elif choice ==4:
                    setting()
                    print(Text.get_text('restart'))
                elif choice ==5:
                    list_log()
                elif choice ==6:
                    send_report()
                elif choice ==7:
                    just_log('leaving ..')
                    exit()
            except Exception as e:
                just_log(f"error ! {e}")
                if True:
                    send_report()
                pass
        
        else:
            print(f"""
            {Colors.BOLD}{Colors.LIGHT_RED}|   {Colors.END}{Colors.PURPLE}[   ]{Colors.END} ─╼ {Colors.BOLD}{Colors.YELLOW}{Text.get_text('no_internet_connection')}        {Colors.END}{Colors.BOLD}
            {Colors.BOLD}{Colors.LIGHT_RED}|   {Colors.END}{Colors.PURPLE}[ 1 ]{Colors.END} ─╼ {Colors.BOLD}{Colors.YELLOW}{Text.get_text("list_and_play_music")}   {Colors.END}{Colors.BOLD}
            {Colors.BOLD}{Colors.LIGHT_RED}|   {Colors.END}{Colors.PURPLE}[ 2 ]{Colors.END} ─╼ {Colors.BOLD}{Colors.YELLOW}{Text.get_text("delete_music")}          {Colors.END}{Colors.BOLD}
            {Colors.BOLD}{Colors.LIGHT_RED}|   {Colors.END}{Colors.PURPLE}[ 3 ]{Colors.END} ─╼ {Colors.BOLD}{Colors.YELLOW}{Text.get_text("settings")}              {Colors.END}{Colors.BOLD}
            {Colors.BOLD}{Colors.LIGHT_RED}|   {Colors.END}{Colors.PURPLE}[ 4 ]{Colors.END} ─╼ {Colors.BOLD}{Colors.YELLOW}{Text.get_text("list_last_log")}         {Colors.END}{Colors.BOLD}
            {Colors.BOLD}{Colors.LIGHT_RED}|   {Colors.END}{Colors.PURPLE}[ 5 ]{Colors.END} ─╼ {Colors.BOLD}{Colors.YELLOW}{Text.get_text("send_report")}           {Colors.END}{Colors.BOLD}
            {Colors.BOLD}{Colors.LIGHT_RED}|   {Colors.END}{Colors.PURPLE}[ 6 ]{Colors.END} ─╼ {Colors.BOLD}{Colors.YELLOW}{Text.get_text("exit")}                  {Colors.END}{Colors.BOLD}

        """)
            choice = input(f'{Colors.CYAN}┌──<[{Colors.RED}{getpass.getuser()}@SpotAFan{Colors.CYAN}]{Colors.END} ~ {Colors.RED}{CONFIG[0]}{Colors.END} \n{Colors.CYAN}└──╼ ${Colors.END} ')
            try:
                choice = int(choice)
            except:
                print(f"{Colors.RED}{Text.get_text('please_enter_valid_number')}{Colors.END}")
            try:
                if choice == 1:
                    list_music(CONFIG[0])
                elif choice == 2:
                    delete_music(CONFIG[0])
                elif choice ==3:
                    setting()
                    print(Text.get_text('restart'))
                elif choice ==4:
                    list_log()
                elif choice ==5:
                    send_report()
                elif choice ==6:
                    just_log('leaving ..')
                    exit()
            except Exception as e:
                just_log(f"error ! {e}")
                if True:
                    send_report()
                pass
        

while __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        log(f"{Colors.RED}interrupted !{Colors.END}")
        if 'y' in input(f'{Colors.CYAN}┌──<[{Colors.RED}{getpass.getuser()}@SpotAFan{Colors.CYAN}]{Colors.END} ~ {Colors.RED}{CONFIG[0]}{Colors.END} \n{Colors.CYAN}└──╼ ${Colors.END} {Text.get_text('leave')}').lower():
            log(f'{Colors.CYAN}leaving ..{Colors.END}')
            exit()