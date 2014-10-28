# THIS REPO IS DEPRECATED

The edX *datajam stack* is a [Vagrant](http://www.vagrantup.com/about.html) instance designed for local development for datajam participants.  The instance:

* Uses the same system dependencies as edX production.
* Simplifies certain production settings to make development more convenient.  For example, it disables **nginx** and **gunicorn** in favor of **runserver** for Django development.

The datajam instance is designed to run code and tests, but you can do most development in the host environment:

* Git repositories are shared with the host system, so you can use your preferred text editor/IDE.
* You can load pages served by the running Vagrant instance.

The datajam configuration has the following components:
* LMS (student facing website)
* Studio (course authoring)
* Forums / elasticsearch / ruby (discussion forums)
* Insights (streaming analytics)
* XBlocks Workbench (courseware preview)

# Installing the edX Datajam Stack


* Create a directory to store the image

        mkdir ~/edx-datajam-root
        cd ~/edx-datajam-root

* For an offline install
    * Install Python 2.7, Virtualbox 4.2.18, and Vagrant 1.3.4 using the provided packages in the 'dependencies' folder
        * If you cannot find the packages for your hardware and OS configuration, follow the links in the "online install" instructions to get the correct dependencies for your system.
    * Copy all of the data off of the USB drive (you can copy the tar file off of the drive using a GUI file manager if you want, and then extract it using the command below if you are unsure where it is mounted)

            tar -C ~/edx-datajam-root -xzf /path/to/mounted/drive/edx-datajam-201312101139.tar.gz

    * Import the vagrant box

            vagrant box add edx-datajam-201312101139 ~/edx-datajam-root/201312101139-edx-datajam.box

* For an online install

    * Ensure you have [Python 2.7](http://www.python.org/download/releases/2.7.6/), [Virtualbox 4.2.18](https://www.virtualbox.org/wiki/Download_Old_Builds_4_2), [Vagrant 1.3.4](https://github.com/edx/configuration/wiki/Installing-Vagrant), and [git](http://git-scm.com/downloads) installed
    * Download the installation script

            curl -O https://raw.github.com/edx/datajam/master/scripts/edx-datajam
            chmod a+x edx-datajam

* Ensure nfsd is running
    * Mac OS X: `sudo nfsd`
    * Ubuntu: `sudo service nfs-kernel-server start`.  This will likely display a message about "no exports."  This is expected and can be ignored.

* Ensure ports 8000-8003, 4567 are not in use.  If you suspect they may be, use `netstat` to confirm.

*If you are currently using other edX development environments (devstack etc), you will need to "halt" those virtual machines before continuing*

* Ensure the following line appears in your /etc/hosts file (you will need to use sudo to edit this file)

        192.168.33.10  preview.localhost

* Run the installation script to setup the environment

        ./edx-datajam create

* Once it completes, you should be able to log in to the virtual machine

        ./edx-datajam ssh


# Using the edX Datajam Stack

It is recommended you open up a separate terminal for each application and and run them in the foreground so that you can monitor them closely.

## LMS Workflow

* Within the Vagrant instance, switch to the edxapp account:

        sudo su edxapp

*This will source the edxapp environment (`/edx/app/edxapp/edxapp_env`) so that the venv python, rbenv ruby and rake are in your search path.  It will also set the current working directory to the edx-platform repository (`/edx/app/edxapp/edx-platform`).*

* Start the server

        edx-lms-devserver

* Open a browser on your host machine and navigate to ``localhost:8000`` to load the LMS.  (Vagrant will forward port 8000 to the LMS server running in the VM.)

## Studio Workflow

* Within the Vagrant instance, switch to the edxapp account:

        sudo su edxapp

*This will source the edxapp environment (`/edx/app/edxapp/edxapp_env`) so that the venv python, rbenv ruby and rake are in your search path.  It will also set the current working directory to the edx-platform repository (`/edx/app/edxapp/edx-platform`).*

* Start the server

        edx-cms-devserver

* Open a browser on your host machine and navigate to ``localhost:8001`` to load Studio.  (Vagrant will forward port 8001 to the Studio server running in the VM.)


## Insights Workflow

* Within the Vagrant instance, switch to the edxapp account:

        sudo su edxapp

*This will source the edxapp environment (`/edx/app/edxapp/edxapp_env`) so that the venv python, rbenv ruby and rake are in your search path.  It will also set the current working directory to the edx-platform repository (`/edx/app/edxapp/edx-platform`).*

* Start the server

        edx-insights-devserver


## XBlock Workbench Workflow

* Within the Vagrant instance, switch to the edxapp account:

        sudo su edxapp

*This will source the edxapp environment (`/edx/app/edxapp/edxapp_env`) so that the venv python, rbenv ruby and rake are in your search path.  It will also set the current working directory to the edx-platform repository (`/edx/app/edxapp/edx-platform`).*

* Start the server

        edx-workbench-devserver


## Forum Workflow

* Within the Vagrant instance, switch to the forum account

        sudo su forum

* Start the server

        edx-forum-devserver

* Access the API at ``localhost:4567`` (Vagrant will forward port 4567 to the Forum server running in the VM.)

## Logging In

Login to the LMS and CMS with the user "datajam@edx.org" with password "datajam."

## Cleaning Up

Once you are done working in the virtual environment you can shut it down by running `./edx-datajam halt` from the host environment.  If you want to continue working after halting, you can restart it by running `./edx-datajam start`.  If you never want to work with it again, you can destroy the environment using `./edx-datajam destroy`.  Note that destroying the environment will delete any files stored in the virtual environment excluding the repositories that are stored in the host environment and NFS mounted into the virtual environment.

# Issues / Workarounds

See this [wiki page](https://github.com/edx/datajam/wiki/Workarounds-for-Issues)
There is also an [FAQ](https://github.com/edx/datajam/wiki/Tips-and-FAQ)
