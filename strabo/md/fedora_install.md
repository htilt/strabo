### Packages needed

    dnf install libjpeg-devel #allows jpeg files to be uploaded
    dnf install libpng-devel #allows png files to be uploaded
    dnf install redhat-rpm-config #needed for python modules to be installed
    dnf install python3-devel   #needed for python modules to be installed
    dnf install vim #editing files remotely
    dnf install emacs #editing files remotely

### Other configuration

Install virtualenv and virtualenvwrapper and set up as shown in install.md

### Postgres installation

You will probably have to be in root user for all of this:
All taken from https://fedoraproject.org/wiki/PostgreSQL#User_Creation_and_Database_Creation

    dnf install postgresql-server postgresql-contrib
    systemctl enable postgresql
    postgresql-setup initdb
    systemctl start postgresql

then type in

su #log into root user, not necessary if already root user
su - postgres   # log into postgres superuser
psql #check into admin database

Then run:

    CREATE USER strabo;

    CREATE DATABASE strabo;

To allow strabo user to create and delete tables:

    ALTER USER strabo WITH SUPERUSER;

To set login with no password required find the pg_hba.conf file, with

    cd /
    find -name "pg_hba.conf"

For me, this was at:

    ./var/lib/pgsql/data/pg_hba.conf

Open this file, scroll down to the actual table and replace the final column with trust on all three rows.

Then restart the service to take account of changes.

    systemctl restart postgresql
