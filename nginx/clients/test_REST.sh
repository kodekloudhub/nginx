#! /bin/bash
#
# 
httpx -m POST -d key key_7007 -d value value_7007 http://e7240/api/items
httpx -m GET http://e7240/api/items
httpx -m POST -d key key_7008 -d value value_7008 http://e7240/api/items
httpx -m GET http://e7240/api/items
httpx -m POST -d key key_7009 -d value value_7009 http://e7240/api/items
httpx -m GET http://e7240/api/items
httpx -m PUT -d key key_7009 -d value value_7009_U_01 http://e7240/api/items/
httpx -m GET http://e7240/api/items
httpx -m DELETE -d key key_7008 http://e7240/api/items
httpx -m GET http://e7240/api/items

