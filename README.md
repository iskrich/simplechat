# Simple Python Chat

[![Build Status](https://travis-ci.org/iskrich/simplechat.svg?branch=master)](https://travis-ci.org/iskrich/simplechat)

Console chat based on sockets. 
# Dependencies

  - Python 2.x

# Launching

Just type:
```sh
$ python server.py
``` 
to start socket server. 


Then you can run 'users', by typing
```sh
$ python client.py
``` 

Enter your name and start awesome chat.

You can run several clients from one machine (I hope).
If you want change server parametres - edit [params.py](https://github.com/iskrich/simplechat/blob/master/params.py)

# Tests
Contains only simple login test. This is very hardly presents as code coverage, but demonstrates usage of client and server objects. 

Also, I needed starting point for Travis :)



# License
MIT