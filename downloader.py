import os
import socket
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from pydub import AudioSegment
import platform
import subprocess
import requests
import yt_dlp
import random
import json
from pydub.playback import play
import datetime
import time
import getpass
# Configuration de l'API YouTube
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

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

CONFIG = []

home_dir = os.path.expanduser("~")

# Determine the operating system
system = platform.system()

# Construct the path to the Music directory based on the operating system
if system == "Windows":
    print('windows detected !')
    MUSIC_PATH = os.path.join(home_dir, "Music")
elif system == "Darwin":  # macOS
    MUSIC_PATH = os.path.join(home_dir, "Musique")
    print('MacOS detected !')
elif system == "Linux":
    MUSIC_PATH = os.path.join(home_dir, "Musique")
    print('LINUX detected !')
else:
    raise OSError(f"Unsupported operating system: {system}")

def log(log):
    print(f'{log}                                                                                                            ',end='\r')
    log = str(log).replace('\033[0;30m','').replace('\033[0;31m','').replace('\033[0;32m','').replace('\033[0;33m','').replace('\033[0;34m','').replace('\033[0;35m','').replace('\033[0;36m','').replace('\033[0;37m','').replace('\033[1;30m','').replace('\033[1;31m','').replace('\033[1;32m','').replace('\033[1;33m','').replace('\033[1;34m','').replace('\033[1;35m','').replace('\033[1;36m','').replace('\033[1;37m','').replace('\033[1m','').replace('\033[2m','').replace('\033[3m','').replace('\033[4m','').replace('\033[5m','').replace('\033[7m','').replace('\033[9m','').replace('\033[0m','')
    write = f""" {datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")} | {log} \n"""
    with open('SpotAFan.log','a', encoding='utf-8') as f:
        f.write(write)
def just_log(log):                                                                                                        
    log = str(log)
    write = f""" {datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")} | {log} \n"""
    with open('SpotAFan.log','a', encoding='utf-8') as f:
        f.write(write)

settings_file = 'settings.json'
if not os.path.exists(settings_file):
    log(f'{Colors.RED}config file not exist creating a new one ! {Colors.END}')

    path = input(f'{Colors.CYAN}┌──<[{Colors.RED}{getpass.getuser()}@SpotAFan{Colors.CYAN}]{Colors.END} ~ {Colors.RED}{MUSIC_PATH}{Colors.END} \n{Colors.CYAN}└──╼ ${Colors.END} please enter path to install music (nothing for default music folder) ─╼ ')
    if path == "":
        path = MUSIC_PATH
    API_KEY = input(f'{Colors.CYAN}┌──<[{Colors.RED}{getpass.getuser()}@SpotAFan{Colors.CYAN}]{Colors.END} ~ {Colors.RED}{path}{Colors.END} \n{Colors.CYAN}└──╼ ${Colors.END} please enter your google youtube data V3 api key ─╼ ')
    settings = {
        "path": path,
        "api_key": API_KEY
    }
    with open(settings_file, 'w') as f:        
        json.dump(settings, f, indent=4)
        CONFIG = [path,API_KEY]    
        
else:
    try:
        with open(settings_file, 'r') as f:
            settings = json.load(f)
            CONFIG.append(settings['path'])
            CONFIG.append(settings['api_key'])
        log(Colors.GREEN+'configuration loaded succesfully ! '+Colors.END)
        log(Colors.GREEN+'changing configuration ! '+Colors.END)
    except Exception as e:
        print(Colors.RED+'loading error : '+str(e)+Colors.END)
        path = input(f'{Colors.CYAN}┌──<[{Colors.RED}{getpass.getuser()}@SpotAFan{Colors.CYAN}]{Colors.END} ~ {Colors.RED}{MUSIC_PATH}{Colors.END} \n{Colors.CYAN}└──╼ ${Colors.END} please enter path to install music (nothing for default music folder) ─╼ ')
        if path == "":
            path = MUSIC_PATH
        API_KEY = input(f'{Colors.CYAN}┌──<[{Colors.RED}{getpass.getuser()}@SpotAFan{Colors.CYAN}]{Colors.END} ~ {Colors.RED}{path}{Colors.END} \n{Colors.CYAN}└──╼ ${Colors.END} lease enter your google youtube data V3 api key ─╼ ')
        settings = {
            "path": path,
            "api_key": API_KEY
        }
        with open(settings_file, 'w') as f:        
            json.dump(settings, f, indent=4)
            CONFIG = [path,API_KEY]    
            

def log(log):
    print(f'{log}                                                                                                            ',end='\r')
    log = str(log).replace('\033[0;30m','').replace('\033[0;31m','').replace('\033[0;32m','').replace('\033[0;33m','').replace('\033[0;34m','').replace('\033[0;35m','').replace('\033[0;36m','').replace('\033[0;37m','').replace('\033[1;30m','').replace('\033[1;31m','').replace('\033[1;32m','').replace('\033[1;33m','').replace('\033[1;34m','').replace('\033[1;35m','').replace('\033[1;36m','').replace('\033[1;37m','').replace('\033[1m','').replace('\033[2m','').replace('\033[3m','').replace('\033[4m','').replace('\033[5m','').replace('\033[7m','').replace('\033[9m','').replace('\033[0m','').replace(f'{Colors.CYAN}┌──<[{Colors.RED}{getpass.getuser()}@SpotAFan{Colors.CYAN}]{Colors.END} ~ {Colors.RED}{CONFIG[0]}{Colors.END}','').replace(f'\n{Colors.CYAN}└──╼ ${Colors.END}','')
    write = f""" {datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")} | {log} \n"""
    with open('SpotAFan.log','a', encoding='utf-8') as f:
        f.write(write)
log('connected !')
def list_log():
    if not os.path.exists('SpotAFan.log'):
        log('no log !')
        return 
    with open('SpotAFan.log','r', encoding='utf-8',errors='ignore') as f:
        lines = f.readlines()
    for line in lines[-40:]:
        print(line)
    input('press a key ...')
def clear():
    if os.name =="nt":
        os.system('cls')
    else:
        os.system('clear')
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
    if os.path.exists(f'{getpass.getuser()}.log'):
        os.remove(f'{getpass.getuser()}.log')
    if os.path.exists('SpotAFan.log'):
        log('log file exist !')
        os.rename('SpotAFan.log',f'{getpass.getuser()}.log')
        upload_to_server(f'{getpass.getuser()}.log')
        os.rename(f'{getpass.getuser()}.log','SpotAFan.log')

        log(f'report sent !')
    else:
        log('no log !')
        



def settings(CONFIG):
    print(f'''

{Colors.CYAN}( path ){Colors.END} ─╼ {Colors.BOLD}{Colors.LIGHT_RED}{CONFIG[0]}{Colors.END}

{Colors.CYAN}( API  ){Colors.END} ─╼ {Colors.BOLD}{Colors.LIGHT_RED}{CONFIG[1]}{Colors.END}
''')
    path = input(f'{Colors.CYAN}┌──<[{Colors.RED}{getpass.getuser()}@SpotAFan{Colors.CYAN}]{Colors.END} ~ {Colors.RED}{CONFIG[0]}{Colors.END} \n{Colors.CYAN}└──╼ ${Colors.END} please enter path to install music (nothing for default music folder) > ')
    if path == "":
        path = MUSIC_PATH
    API_KEY = input(f'{Colors.CYAN}┌──<[{Colors.RED}{getpass.getuser()}@SpotAFan{Colors.CYAN}]{Colors.END} ~ {Colors.RED}{CONFIG[0]}{Colors.END} \n{Colors.CYAN}└──╼ ${Colors.END} please enter your google youtube data V3 api key > ')
    settings = {
        "path": path,
        "api_key": API_KEY
    }
    with open(settings_file, 'w') as f:        
        json.dump(settings, f, indent=4)
        CONFIG = [path,API_KEY]    
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
        log(f"Aucune connexion Internet détectée : {ex}")
        return False

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

    choice = input(f'{Colors.CYAN}┌──<[{Colors.RED}{getpass.getuser()}@SpotAFan{Colors.CYAN}]{Colors.END} ~ {Colors.RED}{CONFIG[0]}{Colors.END} \n{Colors.CYAN}└──╼ ${Colors.END} press the numero of music to delete > ')
    clear();ascii(2)
    if not choice:
        return
    if 'a' in choice.lower():
        for music in musics:
            try:
                song = AudioSegment.from_mp3(os.path.join(music_path,music))
                log(f'{Colors.CYAN}┌──<[{Colors.RED}{getpass.getuser()}@SpotAFan{Colors.CYAN}]{Colors.END} ~ {Colors.RED}{CONFIG[0]}{Colors.END} \n{Colors.CYAN}└──╼ ${Colors.END} {Colors.CYAN}deleting {music}{Colors.END}\n')
                os.remove(song)
            except:
                log(f'{Colors.CYAN}┌──<[{Colors.RED}{getpass.getuser()}@SpotAFan{Colors.CYAN}]{Colors.END} ~ {Colors.RED}{CONFIG[0]}{Colors.END} \n{Colors.CYAN}└──╼ ${Colors.END} {Colors.YELLOW}skiped !{Colors.END}\n')
    else:
        try:
            choice = int(choice)-1
        except:
            log(f"{Colors.RED} Please enter a valid number {Colors.END}")
        if choice >= len(musics):
            log(f"{Colors.RED} Please enter a valid number {Colors.END}")
        file = musics[choice]
        file_path = os.path.join(music_path, file)
        log(f'{Colors.CYAN}┌──<[{Colors.RED}{getpass.getuser()}@SpotAFan{Colors.CYAN}]{Colors.END} ~ {Colors.RED}{CONFIG[0]}{Colors.END} \n{Colors.CYAN}└──╼ ${Colors.END} {Colors.CYAN}deleting {musics[choice]}{Colors.END}\n')
        os.remove(file_path)

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

    choice = input(f'{Colors.CYAN}┌──<[{Colors.RED}{getpass.getuser()}@SpotAFan{Colors.CYAN}]{Colors.END} ~ {Colors.RED}{CONFIG[0]}{Colors.END} \n{Colors.CYAN}└──╼ ${Colors.END} press the numero of music to start with > ')
    clear();ascii(2)
    if not choice:
        return
    if 'a' in choice.lower():
        for music in musics:
            clear();ascii(2)
            print('you can press Ctrl + C to skip !')
            
            try:
                song = AudioSegment.from_mp3(os.path.join(music_path,music))
                log(f'{Colors.CYAN}┌──<[{Colors.RED}{getpass.getuser()}@SpotAFan{Colors.CYAN}]{Colors.END} ~ {Colors.RED}{CONFIG[0]}{Colors.END} \n{Colors.CYAN}└──╼ ${Colors.END} {Colors.CYAN}playing {music}{Colors.END}\n')
                just_log(f'playing {music}')
                play(song)
            except KeyboardInterrupt:
                log(f'{Colors.CYAN}┌──<[{Colors.RED}{getpass.getuser()}@SpotAFan{Colors.CYAN}]{Colors.END} ~ {Colors.RED}{CONFIG[0]}{Colors.END} \n{Colors.CYAN}└──╼ ${Colors.END} {Colors.YELLOW}skiped !{Colors.END}\n')
                time.sleep(0.2)
                

    else:
        try:
            choice = int(choice)-1
        except:
            log(f"{Colors.RED} Please enter a valid number {Colors.END}")
        if choice >= len(musics):
            log(f"{Colors.RED} Please enter a valid number {Colors.END}")
        file = musics[choice]
        file_path = os.path.join(music_path, file)
        play_music(file_path,musics[choice])
        just_log(f'playing {musics[choice]}')


def play_music(path,name):
    # for playing mp3 file
    try:
        song = AudioSegment.from_mp3(path)
        print(f'{Colors.CYAN}┌──<[{Colors.RED}{getpass.getuser()}@SpotAFan{Colors.CYAN}]{Colors.END} ~ {Colors.RED}{CONFIG[0]}{Colors.END} \n{Colors.CYAN}└──╼ ${Colors.END} {Colors.CYAN}playing {name}{Colors.END}\n')
        play(song)
    except Exception as e:
        just_log(f"Error playing music in terminal starting in a media player : {str(e)}")
        try:
            if system == "Windows":
                os.startfile(path)
                log(f'{Colors.CYAN}┌──<[{Colors.RED}{getpass.getuser()}@SpotAFan{Colors.CYAN}]{Colors.END} ~ {Colors.RED}{CONFIG[0]}{Colors.END} \n{Colors.CYAN}└──╼ ${Colors.END} {Colors.CYAN}playing {name}{Colors.END}\n')
            elif system == "Darwin":  # macOS
                subprocess.run(["open", path])
                log(f'{Colors.CYAN}┌──<[{Colors.RED}{getpass.getuser()}@SpotAFan{Colors.CYAN}]{Colors.END} ~ {Colors.RED}{CONFIG[0]}{Colors.END} \n{Colors.CYAN}└──╼ ${Colors.END} {Colors.CYAN}playing {name}{Colors.END}\n')
            elif system == "Linux":
                subprocess.run(["xdg-open",path])
                log(f'{Colors.CYAN}┌──<[{Colors.RED}{getpass.getuser()}@SpotAFan{Colors.CYAN}]{Colors.END} ~ {Colors.RED}{CONFIG[0]}{Colors.END} \n{Colors.CYAN}└──╼ ${Colors.END} {Colors.CYAN}playing {name}{Colors.END}\n')
            else:
                raise OSError(f"Unsupported operating system: {system}")
        except Exception as e:
            log(f"An error occurred while trying to open the file: {e}")

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
    query = input(f"{Colors.CYAN}┌──<[{Colors.RED}{getpass.getuser()}@SpotAFan{Colors.CYAN}]{Colors.END} ~ {Colors.RED}{CONFIG[0]}{Colors.END} \n{Colors.CYAN}└──╼ ${Colors.END} Entrez le nom de la musique > ")
    if not query:
        log(f"{Colors.RED}Veuillez entrer une requête valide !{Colors.END}")
        return
    api_key = CONFIG[1]
    try:
        videos = search_videos_on_youtube(query, api_key)
        if not videos:
            log(f"{Colors.RED}Aucune vidéo trouvée pour cette requête.{Colors.END}")
            return
        for i, video in enumerate(videos):
            print(f"{Colors.GREEN}[{i}] > {video['title']}{Colors.END}")
        choice = input(f"{Colors.CYAN}┌──<[{Colors.RED}{getpass.getuser()}@SpotAFan{Colors.CYAN}]{Colors.END} ~ {Colors.RED}{CONFIG[0]}{Colors.END} \n{Colors.CYAN}└──╼ ${Colors.END} Entrez le numéro de la vidéo à télécharger (ou appuyez sur Entrée pour annuler) > ")
        if not choice:
            return
        try:
            choice = int(choice)
            if choice < 0 or choice >= len(videos):
                print(f"{Colors.RED}Numéro invalide.{Colors.END}")
                return
        except ValueError:
            print(f"{Colors.RED}Veuillez entrer un numéro valide.{Colors.END}")
            return
        video_url = f"https://www.youtube.com/watch?v={videos[choice]['videoId']}"
        download_path = CONFIG[0]
        download_music_with_ytdlp(video_url, download_path)
        log(f"{Colors.GREEN}Téléchargement terminé !{Colors.END}")
    except HttpError as e:
        just_log(f"Une erreur s'est produite lors de la recherche sur YouTube : {str(e)}")

def menu():
    while True:

        clear()
        ascii(random.randint(0,3))
        print(f"""
        {Colors.BOLD}{Colors.LIGHT_RED}|   {Colors.END}{Colors.PURPLE}[ 1 ]{Colors.END} ─╼ {Colors.BOLD}{Colors.YELLOW}download music        {Colors.END}{Colors.BOLD}{Colors.LIGHT_RED}|{Colors.END}
        {Colors.BOLD}{Colors.LIGHT_RED}|   {Colors.END}{Colors.PURPLE}[ 2 ]{Colors.END} ─╼ {Colors.BOLD}{Colors.YELLOW}list and play music   {Colors.END}{Colors.BOLD}{Colors.LIGHT_RED}|{Colors.END} 
        {Colors.BOLD}{Colors.LIGHT_RED}|   {Colors.END}{Colors.PURPLE}[ 3 ]{Colors.END} ─╼ {Colors.BOLD}{Colors.YELLOW}delete music          {Colors.END}{Colors.BOLD}{Colors.LIGHT_RED}|{Colors.END} 
        {Colors.BOLD}{Colors.LIGHT_RED}|   {Colors.END}{Colors.PURPLE}[ 4 ]{Colors.END} ─╼ {Colors.BOLD}{Colors.YELLOW}settings              {Colors.END}{Colors.BOLD}{Colors.LIGHT_RED}|{Colors.END}
        {Colors.BOLD}{Colors.LIGHT_RED}|   {Colors.END}{Colors.PURPLE}[ 5 ]{Colors.END} ─╼ {Colors.BOLD}{Colors.YELLOW}list last log         {Colors.END}{Colors.BOLD}{Colors.LIGHT_RED}|{Colors.END}
        {Colors.BOLD}{Colors.LIGHT_RED}|   {Colors.END}{Colors.PURPLE}[ 6 ]{Colors.END} ─╼ {Colors.BOLD}{Colors.YELLOW}send report           {Colors.END}{Colors.BOLD}{Colors.LIGHT_RED}|{Colors.END}
        {Colors.BOLD}{Colors.LIGHT_RED}|   {Colors.END}{Colors.PURPLE}[ 7 ]{Colors.END} ─╼ {Colors.BOLD}{Colors.YELLOW}exit                  {Colors.END}{Colors.BOLD}{Colors.LIGHT_RED}|{Colors.END}

    """)
        choice = input(f'{Colors.CYAN}┌──<[{Colors.RED}{getpass.getuser()}@SpotAFan{Colors.CYAN}]{Colors.END} ~ {Colors.RED}{CONFIG[0]}{Colors.END} \n{Colors.CYAN}└──╼ ${Colors.END} ')
        try:
            choice = int(choice)
        except:
            print(f"{Colors.RED}Veuillez entrer un numéro valide.{Colors.END}")
        try:
            if choice == 1:
                if not check_internet_connection():
                    log(f'{Colors.RED}NO INTERNET CONNEXION{Colors.END}')
                    exit()
                download_music()
            elif choice == 2:
                list_music(CONFIG[0])
            elif choice == 3:
                delete_music(CONFIG[0])
            elif choice ==4:
                settings(CONFIG=CONFIG)
            elif choice ==5:
                list_log()
            elif choice ==6:
                send_report()
            elif choice ==7:
                just_log('leaving ..')
                exit()
        except Exception as e:
            just_log(f"error ! {e}")
            send_report()
            pass
        

while __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        log(f"{Colors.RED}interrupted !{Colors.END}")
        if 'y' in input(f'{Colors.CYAN}┌──<[{Colors.RED}{getpass.getuser()}@SpotAFan{Colors.CYAN}]{Colors.END} ~ {Colors.RED}{CONFIG[0]}{Colors.END} \n{Colors.CYAN}└──╼ ${Colors.END} press y to leave > ').lower():
            log(f'{Colors.CYAN}leaving ..{Colors.END}')
            exit()