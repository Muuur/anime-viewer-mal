#!/usr/bin/python3
import re
import sys
from random import randrange
from os import system, name
try:
    import requests as r
    from colorama import init, Fore as f
except ModuleNotFoundError as md:
    sys.stderr.write(md + " please install it\n")
    exit(1)

if name == 'nt': system("cls")
init(autoreset=True)

anime = {}
titles = []
found = []
chars = ['english', 'episodes', 'airing', 'airstart', 'airend', 'sair', 'fair', 'id', 'type', 'genres', 'score']
i, l, online, home, bus, yo, nfilt, fo, rand, animeid, force = 1, '', False, False, "", False, r".*", 'table', False, 0, True
user = '' # Put your username here

def air(num):
    if num == 0: return f"{f.LIGHTBLUE_EX}Not yet aired"
    elif num == 1: return f"{f.LIGHTYELLOW_EX}Currently Airing"
    elif num == 2: return f"{f.LIGHTGREEN_EX}Finished airing"
    else: return f"{f.LIGHTRED_EX}Undefined"

# Program init
if len(sys.argv) == 1:
    system(f"start https://myanimelist.net/animelist/{user}" if name == 'nt' else f"xdg-open https://myanimelist.net/animelist/{user} > /dev/null 2>&1")
    exit(0)
else:
    while i < len(sys.argv):
        try:
            if sys.argv[i].lower() in ['-?', '--help']:
                print("""MAL [ OPCIONES ] [ BÚSQUEDA ]
                \nOpciones:
                \r  -?, --help
                \r  -v, --ver    Muestra la versión actual del programa
                \r  -h, --home   Página HOME de myanimelist
                \r  -y, --yo     Página de inicio de la página personal
                \r  -f, --noopen Modo de no apertura
                \r  -o, --online Modo online (consola)
                \r  -l  + #      Accede a una sublista concreta (0-6)
                \r  -r           Accede a un anime aleatorio de PTW
                \r  -id + ID     Accede a un anime específico mediante ID
                \nBúsqueda     Filtra la búsqueda general de animes
                \r  Sin online   Accede a la página de los animes que coinciden
                \r  Con online   Busca y muestra los resultados en consola
                \nNo se pueden usar -h y -y con -o
                \rCon -l se accede a la lista, sino se busca en general
                \rEl valor predeterminado para -l es 0
                \rEl modo -f impide acceder a imternet de forma externa
                \rEl modo -o imprime en consola en vez de acceder a internet
                \rEl modo -r Solo se puede usar con -l
                \rEl modo -id no se puede usar con ningun otro""")
                exit(0)
            elif sys.argv[i].lower() in ('-v', '--ver'):
                print("MAL - Version 3.0 multiplataforma\n\nMuuur software")
                exit(0)
            elif sys.argv[i].lower() == '-id':
                if sys.argv[i + 1][0] == '-':
                    raise IndexError
                elif sys.argv[i + 1].isdigit():
                    animeid = int(sys.argv[i + 1])
                    i += 1
                else:
                    sys.stderr.write(f.LIGHTRED_EX + sys.argv[i + 1] + " is not a number\n")
                    exit(1)
            elif sys.argv[i][0:2].lower() == '-r':
                rand = True
                if l == '':
                    if len(sys.argv[i]) > 2 and sys.argv[i][2].lower() in ['h', 'p', '6', '3']:
                        l = int(sys.argv[i][2].lower().replace('h', '3').replace('p', '6'))
                    else:
                        l = 6
                break
            elif sys.argv[i][0:2].lower() == '-l' and sys.argv[i][2].lower() in ['1', '2', '3', '4', '6', '0', 'p', 'w', 'a', 'h', 'c', 'd']: # Número de lista
                l = int(sys.argv[i][2].lower().translate({ord('a'): ord('0'), ord('w'): ord('1'), ord('c'): ord('2'), ord('h'): ord('3'), ord('d'): ord('4'), ord('p'): ord('6')}))
            elif sys.argv[i].lower() in ['-h', '--home']: # Welcome webpage
                home = True
            elif sys.argv[i].lower() in ['-y', '--yo']: # Personal webpage
                yo = True
            elif sys.argv[i].lower() in ('-f', '--noopen'): # No open mode
                force = False
            elif sys.argv[i].lower() in ('-o', '--online'): # CLI mode
                online = True
            else: # Search
                bus = "+".join(sys.argv[i:])
                break
        except IndexError:
            sys.stderr.write(f"{f.LIGHTRED_EX}An extra argument is needed for {sys.argv[i]}\n")
            exit(1)
        except ValueError:
            sys.stderr.write(f"{f.LIGHTRED_EX}A number was expected for {sys.argv[i]}\n")
            exit(1)
        i += 1

if online and not rand and l != "" and 0 <= l <= 6:
    nfilt = bus.replace("+", " ")
    bus = ""

for i in chars:
    if i not in ['name',  'english', 'episodes', 'airing', 'genres', 'airstart', 'airend', 'sair', 'fair', 'id', 'type', 'score']:
        sys.stderr.write(f"{f.LIGHTRED_EX}Ffilter {i} doesn't exists\n")
        chars.remove(i)
if bool(bus):
    if l != "":
        sys.stderr.write(f"{f.LIGHTRED_EX}You can't specify a list page out of list\n")
        exit(1)
    if nfilt != ".*":
        sys.stderr.write(f"{f.LIGHTRED_EX}You can't filter by RegEx out of your own list\n")
        exit(1)
    if len(chars) < 10:
        sys.stderr.write(f"{f.LIGHTRED_EX}You can't filter content out of your list\n")
        exit(1)
    home, yo = False, False
if rand:
    if home or yo:
        sys.stderr.write(f.LIGHTRED_EX + "You can't access through welcome nor personal webpages if random was selected\n")
        exit(1)
    if bool(bus) or nfilt != '.*' or len(chars) < 10:
        sys.stderr.write(f.LIGHTRED_EX + "You can't search anything is random was selected\n")
        exit(1)
if animeid > 0:
    if bool(bus):
        sys.stderr.write(f.LIGHTRED_EX + "You can't search anything if you use id\n")
        exit(1)

# Ejecución del programa
if online or rand: # Modo online
    if bool(bus) or animeid > 0:
        if animeid > 0:
            try:
                page = r.get(f"https://myanimelist.net/anime/{animeid}").content.decode()
            except r.exceptions.ConnectionError:
                sys.stderr.write(f.LIGHTRED_EX + "Server error, maybe you have no internet connection\n")
                exit(9005)
            bus = re.search(r'property="og:title" content="([^"]+)"', page)
            titles.append(bus[1])
            bus = len(titles) - 1
        else:
            page = r.get(f"https://myanimelist.net/search/all?q={bus}&systemcat=anime").content.decode()
            for i in re.finditer(r'<a href="([^"]+)" class="[^"]+" id="#\w+" rel="#\w+">([^<]+).+\n(.*\n){2,4}\s+<a href="[^"]+">(TV|Movie|ONA|OVA|Special)</a>( \((\d+) eps\))?<br>\n\s*Scored (\d\.\d{0,2}|N/A)<br>', page, re.M):
                titles.append(i[2])
                anime.update({i[2]: {'link': i[1], 'type': i[4], 'episodes': i[6], 'val': i[7]}})
            for i in range(len(titles)):
                print(f"{f.BLUE}[{f.LIGHTCYAN_EX}{i}{f.BLUE}]{f.RESET} -> {f.LIGHTGREEN_EX}{titles[i]} " + str('\t' * (5 - len(titles[i])//8)) + f"{f.LIGHTYELLOW_EX}({anime[titles[i]]['type']})" + (' ' if anime[titles[i]]['type'] == 'Special' else '\t  ') + f"{f.LIGHTGREEN_EX}eps: {anime[titles[i]]['episodes']}\t{f.LIGHTYELLOW_EX}rating: {anime[titles[i]]['val']}")
            print(f.LIGHTBLUE_EX + "\nInput the anime name which you want to know about: ", end="")
            while True:
                try:
                    bus = int(input(f.LIGHTMAGENTA_EX))
                    page = r.get(anime[titles[bus]]['link']).content.decode()
                    break
                except (IndexError, ValueError):
                    sys.stderr.write(f.LIGHTRED_EX + "An error occured during number selection, please try it again: " + f.LIGHTMAGENTA_EX)
                except NameError:
                    sys.stderr.write(f.LIGHTRED_EX + "An error occured during link capture\n")
                    exit(9005)
                except r.exceptions.ConnectionError:
                    sys.stderr.write(f.LIGHTRED_EX + "Internal error, maybe you have no internet connection\n")
                    exit(9005)
                except (EOFError, OSError, KeyboardInterrupt):
                    exit(0)
        print(f"\n{f.RESET}{titles[bus]}\n")
        try:
            print(f.LIGHTYELLOW_EX + "English:    " + f.LIGHTGREEN_EX + re.search('<span class="dark_text">English:</span> (.+)', page, re.M)[1])
        except TypeError:
            print(f.LIGHTCYAN_EX + "English:    " + f.RED + "Not available")
        for i in ['Type', 'Episodes', 'Status', 'Aired', 'Premiered', 'Source', 'Duration', 'Rating', 'Score', 'Ranked', 'Popularity', 'Members', 'Favorites']:
            keyw = re.search(f'<span class="dark_text">{i}:</span>\n\\s*(<a href="[^"]+">|<span itemprop="[^>]+>)?([^<"\n]+)(</a>|</span>)?', page, re.M)
            if i == "Score": sys.stdout.write(f.LIGHTYELLOW_EX + "\nStatistics:\n")
            try:
                print(f.LIGHTCYAN_EX + i + ":" + (' ' * (11 - len(i))) + f.LIGHTGREEN_EX + keyw[2])
            except TypeError:
                print(f.LIGHTCYAN_EX + i + ":" + (" " * (11 - len(i))) + f.RED + "Unknown")
        sys.stdout.write(f.LIGHTBLUE_EX + "Genres:     ")
        for i in re.finditer(r'<span itemprop="genre" style="display: none">([\w\-. ]+)</span>', page):
            sys.stdout.write(f.LIGHTGREEN_EX + i[1] + ", ")
        print("\b\b ")
        try:
            if force and input(f.BLUE + "\nDo you want to open the page (Y/N) " + f.LIGHTMAGENTA_EX)[0].upper() in ["S", "Y"]: system(f'start "" "{anime[titles[bus]]["link"]}"' if name == 'nt' else f'xdg-open "{anime[titles[bus]]["link"]}" > /dev/null 2>&1')
        except (EOFError, OSError, IndexError, KeyboardInterrupt):
            exit(0)
    else:
        page = r.get(f"https://myanimelist.net/animelist/{user}?status={l}").content.decode()
        i = 0
        for j in re.finditer(r'anime_title&quot;:&quot;([^&]+)&', page): # Title
            titles.append(j[1])
            anime.update({j[1]: {}})
        for j in re.finditer(r'&quot;anime_title_eng&quot;:&quot;([^&]*)&', page):
            if j[1] == "":
                anime[titles[i]]['english'] = titles[i]
            else:
                anime[titles[i]]['english'] = j[1]
            i += 1
        i = 0
        for j in re.finditer(r'anime_num_episodes&quot;:(\d+)', page): # Episodes number
            anime[titles[i]]['episodes'] = int(j[1])
            i += 1
        i = 0
        for j in re.finditer(r'anime_airing_status&quot;:(\d)', page): # Airing status
            anime[titles[i]]['airing'] = air(int(j[1]))
            i += 1
        i = 0
        for j in re.finditer(r'&quot;genres&quot;:\[([^\]]+)\]', page): # Genres
            anime[titles[i]]['genres'] = []
            for k in re.finditer(r'name&quot;:&quot;([^&]+)&', j[1]):
                anime[titles[i]]['genres'].append(k[1])
            i += 1
        i = 0
        # Ignore, someday i will fix it
        # if l <= 2:
        #     for j in re.finditer(r';start_date_string&quot;:&quot;([^&]+)&quot;,&quot;finish_date_string&quot;:(&quot;)+([^&]+)&', page):
        #         anime[titles[i]]['airstart'] = j[1]
        #         anime[titles[i]]['airend'] = j[3] if l != 1 else chars.remove('airend')
        #         i += 1
        #     i = 0
        # else:
        chars.remove('airstart')
        chars.remove('airend')
        for j in re.finditer(r';anime_start_date_string&quot;:&quot;([^&]+)&quot;,&quot;anime_end_date_string&quot;:&quot;([^&]+)', page): # Air and end dates
            anime[titles[i]]['sair'] = j[1]
            anime[titles[i]]['fair'] = j[2]
            i += 1
        i = 0
        for j in re.finditer(r'anime_id&quot;:(\d+)', page): # id
            anime[titles[i]]['id'] = j[1]
            i += 1
        i = 0
        for j in re.finditer(r'anime_media_type_string&quot;:&quot;(\w+)', page): # Type (OVA, anime, movie...)
            anime[titles[i]]['type'] = j[1]
            i += 1
        i = 0
        for j in re.finditer(r'score&quot;:(\d{1,2})', page): # Score
            try:
                anime[titles[i]]['score'] = (j[1] if int(j[1]) > 0 else "N/A")
            except (TypeError, IndexError):
                anime[titles[i]]['score'] = "N/A"
            i += 1
        if rand:
            rand = randrange(len(titles))
            print(f.LIGHTGREEN_EX + titles[rand])
            try:
                if force and input(f.BLUE + "\nDo you want to open the page (Y/N) " + f.LIGHTMAGENTA_EX)[0].upper() in ["S", 'Y']: system(f"start https://myanimelist.net/anime/{anime[titles[rand]]['id']}" if name == 'nt' else f"xdg-open https://myanimelist.net/anime/{anime[titles[rand]]['id']} > /dev/null 2>&1")
            except (EOFError, OSError, IndexError, KeyboardInterrupt):
                exit(1)
        else:
            for i in filter(lambda t: bool(re.search(nfilt, t, re.I)),titles):
                sys.stdout.write( "\n" + i + "\n")
                for j in chars:
                    if j == 'genres':
                        sys.stdout.write(f"    {f.LIGHTCYAN_EX}genres{f.RESET} -> ")
                        for k in anime[i]['genres']:
                            sys.stdout.write(f.LIGHTGREEN_EX + k + ", ")
                        print("\b\b ")
                    else:
                        sys.stdout.write("    " + f.LIGHTBLUE_EX + j + f.RESET + " -> " + f.LIGHTGREEN_EX + str(anime[i][j]) + "\n")
else:
    if nfilt != ".*" or len(chars) < 10:
        sys.stderr.write(f.LIGHTRED_EX + "You can't use filters in offline mode\n")
    elif animeid > 0:
        system(f"start https://myanimelist.net/anime/{animeid}" if name == 'nt' else f"xdg-open https://myanimelist.net/anime/{animeid} > /dev/null 2>&1")
    else:
        if home:
            system("start https://myanimelist.net/" if name == 'nt' else "xdg-open https://myanimelist.net/ > /dev/null 2>&1")
        elif yo:
            system(f"start https://myanimelist.net/profile/{user}" if name == 'nt' else f"xdg-open https://myanimelist.net/profile/{user} > /dev/null 2>&1")
        elif bool(bus):
            system(f"start https://myanimelist.net/search/all?q={bus}\&cat=anime" if name == 'nt' else f"xdg-open https://myanimelist.net/search/all?q={bus}\&cat=anime > /dev/null 2>&1")
        else:
            system(f"start https://myanimelist.net/animelist/{user}?status={l}" if name == 'nt' else f"xdg-open https://myanimelist.net/animelist/{user}?status={l} > /dev/null 2>&1")
