```
 (                                        )                  
 )\ )                     *   )  *   ) ( /(          )    )  
(()/(  (          (  (  ` )  /(` )  /( )\())   )  ( /( ( /(  
 /(_))))\ `  )   ))\ )(  ( )(_))( )(_)|(_)\   /(( )\()))\()) 
(_)) /((_)/(/(  /((_|()\(_(_())(_(_())_ ((_) (_))((_)\((_)\  
/ __(_))(((_)_\(_))  ((_)_   _||_   _\ \ / / _)((_) (_)  (_) 
\__ \ || | '_ \) -_)| '_| | |    | |  \ V /  \ V /| || () |  
|___/\_,_| .__/\___||_|   |_|    |_|   |_|    \_/ |_(_)__/   
         |_|                                                 
         (c) Bad Hombres 2017
```
Reverse or bind shell catcher which uprgrades the caught shell to be more like a regular shell.

This method is not my own invention and was pinched from [this post](https://blog.ropnop.com/upgrading-simple-shells-to-fully-interactive-ttys/) by ropnop

## Install
Installation couldnt be simpler.

* Clone this repo
* `pip install docopt`

## Usage
Can be used as a catcher or to connect to a bind shell, at the moment it uses
python to spawn a PTY. I will work on other options in the future

```
Usage:
    supertty.py --port <port> --host <host> [--shell <shell>]
    supertty.py --port <port> [--ip <ip>] [--shell <shell>]
    supertty.py (-h | --help)

Options:
    -h --help           Show this screen
    --port <port>       Port number to listen on to to connect to the remote host on [default: 4445]
    --host <host>       Host to connect to for bind shells
    --ip <ip>           ip to listen on for reverse shells [default: "0.0.0.0"]
    --shell <shell>     Shell spawn as PTY [default: /bin/bash]
```
