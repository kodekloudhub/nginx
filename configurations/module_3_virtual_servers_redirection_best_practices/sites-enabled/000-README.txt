# To generate the symlink to enable a site:

# cd /etc/nginx/sites-enabled
# ln -s -v ../sites-available/SITE .


#  e.g to enable the default site,


# ln -s -v ../sites-available/default .

# This assumes that the site is already set up and working and the configuration is in /etc/nginx/sites-available.
# Also, this is the debian convention.  If you want something simpler, then you can put the configuration file
# in /etc/nginx/conf.d



# This file is parsed by nginx, so everything in this file must be commented out.
