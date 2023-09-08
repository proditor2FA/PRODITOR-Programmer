#!/usr/bin/python3
#Papa hat gesagt alles nur in 1 file!

import sys, os, subprocess


BLACK = "\033[30m"
RED = "\033[31m"
ORANGE = "\033[38;5;208m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
BLUE = "\033[94m"
VIOLET = "\033[95m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"

NORMAL = "\033[0m"


LOGO_ASCII = f'''
 {RED}    
                                     %%&@&&                                   
                              @@@@@@@@@@@@@@@@@@@@&                             
                          &@@@@@@@@@@@@@@@@@@@@@@@@@@@*                         
                        @@@@@@@@@@@           @@@@@@@@@@@                       
                      @@@@@@@@@                   @@@@@@@@&                     
                     @@@@@@@/                       &@@@@@@@                    
                    @@@@@@@                           @@@@@@@                   
                   @@@@@@@                             @@@@@@#                  
                   @@@@@@&                             @@@@@@@                  
                   @@@@@@&                             @@@@@@@                  
                   @@@@@@@                             @@@@@@#                   
                    @@@@@@@                           @@@@@@@                   
                     @@@@@@@                        #@@@@@@@                    
                      @@@@@@@@@                   @@@@@@@@@                     
                        @@@@@@@@@@/           (@@@@@@@@@@                       
                          @@@@@@@@@@@@@@@@@@@@@@@@@@@@%                         
                       @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                        
                   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                       
                &@@@@@@@@@@@@&                       @@%                         
            @@@@@@@@@@@                                                         
          @@@@@@@@@@ {WHITE}                            ,@@@@@@@@@@@@@@@@@/  {RED}     
        @@@@@@@@@  {WHITE}                            @@@@@@@@@@@@@@@@@@@@@@@  {RED} 
      @@@@@@@@. {WHITE}                             #@@@@@@@@@@@@@@@@@@@@@@@@@&  {RED}
     @@@@@@@.  {WHITE}       @@@@@@@@@@@@@@@@@@@@@@@@@@@@@&             #@@@@@@(  {RED}
   @@@@@@@@  {WHITE}      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@               @@@@@@@  {RED}
  @@@@@@@*  {WHITE}     @@@@@@@@@%%%%%%%%%%%%%%%%%%%%%%          %@@@@    @@@@@@  {RED}
 *@@@@@@   {WHITE}     @@@@@@@@                                  @@@@@@   @@@@@@  {RED}
 @@@@@@@   {WHITE}      @@@@@@@@@@@@@@@@@@@&         @@@          &@@*    @@@@@@  {RED}
@@@@@@@    {WHITE}         @@@@@@@@@@@@@@@@@@      @@@@@@@               @@@@@@@  {RED}
@@@@@@@    {WHITE}           &@@@@@@@@@@@@@@(       @@@@@@&             @@@@@@@  {RED}
 @@@@@@@@@@@@@@@@@@@@@@    {WHITE}                  %@@@@@@@@@@@@@@@@@@@@@@@@@  {RED}
   @@@@@@@@@@@@@@@@@@@@@   {WHITE}                    @@@@@@@@@@@@@@@@@@@@@@@  {RED} 
      /@@@@@@@@@@@@@@@@    {WHITE}                       &@@@@@@@@@@@@@@@/      
                                                                                
   @@@@@@@@  @@@@@@@@%  #@@@@@@@   @@@@@@@@   @@ @@@@@@@@@ @@@@@@@@   @@@@@@@@ 
   @@     @@ @@     @@  @@     @@  @@     @@  @@     @@    @@    &@,  @@    *@%
   @@@@@@@@  @@@@@@@@  .@@     @@  @@     @@  @@     @@   @@@    &@@  @@@@@@@   
   @@        @@   @@@   @@    @@@  @@     @@  @@     @@    @@    @@,  @@   @@   
   @@        @@     @@   @@@@@@    @@@@@@@    @@     @@     @@@@@@    @@    @@% 

{RED}
                ********  Programmer Version 2023/rev.1 ********

{CYAN}  
    '''

repeat = "3132333435363738393031323334353637383930"

def handle_files(key):
    key_str = ''.join([chr(int(key[i:i+2], 16)) for i in range(0, len(key), 2)])

    try:
        org_binary = open('Proditor-template.bin', 'rb').read()
    except Exception as e:
        print(f"{RED}ERROR: missing or corrupt file {CYAN}'Proditor_org.bin'{RED} pleas put the original binary in your working directory\nerror message: {ORANGE}{e}{NORMAL}")
        return

    try:
        marked_buffer = open('16KB-FF_marked.bin', 'rb').read()
    except Exception as e:
        print(f"{RED}ERROR: missing or corrupt file {CYAN}'16KB-FF_marked'{RED} pleas put the marked FF buffer in your working directory\nerror message: {ORANGE}{e}{NORMAL}")
        return
    
    marked_buffer = marked_buffer.replace(b'12345678901234567890', key_str.encode())
    marked_buffer = org_binary + marked_buffer[len(org_binary):]

    try:
        open('Proditor.bin', 'wb').write(marked_buffer)
        print(f"{GREEN}created new file successfully{NORMAL}")
    except Exception as e:
        print(f"{RED}ERROR: {ORANGE}{str(e)}{RED} occoured in {CYAN}'handle_file'{NORMAL}")
        return

    org_binary = ""
    marked_buffer = ""
    
def handle_openocd(key):
    try:
        subprocess.call(["openocd", "-f", "openocd.cfg"])
    except Exception as e:
        print(f"{RED}ERROR: openocd does not seem to be installed\nerror message: {ORANGE} {e}{NORMAL}")
#    os.remove("Proditor.bin")

def handle_input():
    global repeat 
    user_input = input("Enter Proditor HEX-40 secret - (q)uit (r)repeat: ")
    print("")
    if user_input == "exit" or user_input == "quit" or user_input == "q" or user_input == "e":
        print(f"{YELLOW}Good bye!{NORMAL}")
        sys.exit()

    elif user_input == "r" or user_input == "R":
        print(f"{YELLOW}Repeat programming (HEX-40): ", repeat)
        print("")
        handle_files(repeat)
        handle_openocd(repeat)

    elif len(user_input) != 40:
        print(f"{YELLOW}WARNING: the provided argument needs to be in {CYAN}HEX{YELLOW} and exactly {CYAN}40{YELLOW} chars long{NORMAL}")

    else:
        repeat = user_input
        print(f"{YELLOW}Programming (HEX-40): ", user_input)
        print("")
        handle_files(user_input)
        handle_openocd(user_input)

def main():
    print(LOGO_ASCII)
    running = True
    while(running):
        handle_input()
        print(f"{YELLOW}")
        input("Press Enter to continue...")
        print(f"{NORMAL}")
        print(LOGO_ASCII)
    sys.exit()



if __name__ == '__main__':
    main()