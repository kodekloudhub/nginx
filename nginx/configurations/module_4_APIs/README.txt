kodekloud/www/wsgi

This directory is for server-side python programs that interface either using
WSGI or flask

In case of a 403 permission denied error, make sure the that the group id (GID) of all the files is nginx.  Both jeffs and nginx are members of the nginx group.  M
ake sure that all the directories have execute privilege turned on (chmod o+x -R ).


