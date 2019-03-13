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

## Usage
Can be used as a catcher or to connect to a bind shell, at the moment it uses
python to spawn a PTY. I will work on other options in the future

```
usage: supertty.py [-h] [--handler HANDLER]

Reverse shell catcher

optional arguments:
  -h, --help         show this help message and exit
  --handler HANDLER  Name of the handler module to use
```

Each handler has its own options see them with `--handler-help`

Currently has two handlers:

* netcat
* openssl

Pull requests for other types welcome!
