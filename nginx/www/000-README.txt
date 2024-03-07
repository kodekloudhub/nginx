kodekloud/www

This directory contains directories that contain content that the nginx webserver should server.

The contents of this directory's file tree should be sent to the web server's /var/www directory
on the web server.

That can be done using 
1) git
2) scp from the development machine to the webserver
3) symlinking the file tree that git is managing under www to /var/www



The advantage of using git is that the development machine and the web server machine
can be on different branches, and git makes it harder to overwrite changes.

To do that, the directory has to be set up.

1. **Clone the Repository**:
   If you haven't already, clone the repository to your local machine.
   git clone REMOTE_REPOSITORY_URL

(as of 4-Mar-2024, 2024:03:04,  REMOTE_REPOSITORY_URL is
git@github.com:kodekloudhub/nginx.git
so the least confusing way to do this is:
cd ~/work/kodekloud/
git clone git@github.com:kodekloudhub/nginx.git
)


2. **Enable Sparse Checkout**:
   cd REPOSITORY_DIRECTORY
   (in this case, that would be kodekloud or ~/work/kodekloud`)

   and enable sparse checkout.
   git config core.sparseCheckout true

3. **Specify the Subdirectory**:
   Create a file named `.git/info/sparse-checkout` if it doesn't exist.

   touch .git/info/sparse-checkout

   Then, specify the subdirectory you want to pull by adding its path to this file.

   echo "PATH_TO_SUBDIRECTORY" >> .git/info/sparse-checkout

   e.g. echo "kodekloud/www >> .git/info/sparse-checkout


4. **Update Index and Checkout**:
   Update the index with the specified paths.

   git read-tree -mu HEAD

   This command updates the working directory with the content of the specified paths.

Now, you have only the contents of the specified subdirectory in your working directory.

5. **Pull Changes** (Optional):
   If you also want to pull changes for the subdirectory from the remote repository, you can do so by pulling normally.

   ```bash
   git pull origin BRANCH_NAME
   ```

Make sure to replace `<branch-name>` with the appropriate branch name.
jeffs@fedora:~/kodekloud$ sudo rm /var/www
jeffs@fedora:~/kodekloud$ sudo ln -s $HOME/kodekloud/www /var/www
jeffs@fedora:~/kodekloud$ ls /var/www
000-README.txt  cgi-bin  html  wsgi
jeffs@fedora:~/kodekloud$ 



The advantage of using the symlink is that it keeps the file tree together in one tree, and yet the 
files are where nginx expects them to be without too much additional trial and tribution.


Y
