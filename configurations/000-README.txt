kodekloud/configurations

This directory contains nginx configuration files.  Each subdirectory contains the nominal 
configuration file(s) for that particular module.

There are several ways you can use these configuration files.

1) Copy the files from your local git repository to /etc/nginx.
2) Symlink /etc/nginx to the appropriate module in your local git repository.
So, for example (all of these as root unless you figured out something else.
which is both doable and recommended):

mv /etc/nginx /etc/nginx_STASHED
ln -s /home/jeffs/kodekloud/configurations/module_3_virtual_servers_redirection_best_practice/ /etc/nginx
ls /etc/nginx/nginx.conf

This is my expectation

3) Use these configuration files as motivation to write your own configuration files.  Be wild!
Ask for help as needed.  Be prepared to make a presentation, unless you have stage fright.

This is my prefered option.



