kodekloud/www/wsgi

Originally, I thought this directory would be for server-side python programs
that interface either using WSGI or flask.  It turns out that this is a Bad Idea.  
Some of these programs might contain sensitive information and should be hidden.
A misconfiguration of the server might expose these programs.

It is better to put all of these programs someplace else.  For this class, that's
nginx/server_scripts.  In production, that might be /home/nginx/server_scripts
or similar.


