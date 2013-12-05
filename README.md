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

* Install [Virtualbox 4.2.18](https://www.virtualbox.org/wiki/Download_Old_Builds_4_2)
* Install [Vagrant 1.3.4](https://github.com/edx/configuration/wiki/Installing-Vagrant)
* Install the `vagrant-hostsupdater` plugin:

    vagrant plugin install vagrant-hostsupdater

* Install [git](http://git-scm.com/downloads)
* Create a directory to store the image

    mkdir ~/edx-datajam-root

    cd ~/edx-datajam-root

* Download the installation script

    curl -O https://raw.github.com/edx/datajam/master/scripts/edx-datajam

    chmod a+x edx-datajam

* Ensure nfsd is running
    * Mac OS X: `sudo nfsd`
    * Ubuntu: `sudo service nfs-kernel-server start`

* Ensure ports 8000-8003, 4567 are not in use.  If you suspect they may be, use `netstat` to confirm.

*If you are currently using other edX development environments (devstack etc), you will need to "halt" those virtual machines before continuing*

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

# Issues / Workarounds

See this [wiki page](https://github.com/edx/datajam/wiki/Workarounds-for-Issues)
