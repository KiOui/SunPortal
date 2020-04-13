# Sunportal

Welcome to Sunportal! A visualizer for data stored in SBFspot. This tool was made for showing solar power statistics on a screen connected to a Raspberry Pi, although it will run on other systems as well. The interface is made for one screen height, this means that you don't need to scroll to see all content, perfect for creating a "status" monitor in your house or other place.

Sunportal was first made with bare PHP code but is now running on Flask, this makes it easier to setup and maintain.

You have a couple of choices regarding installation, you can try and run the Flask app that is in this repository yourself. This gives you full control over where and how to run it, alternatively there is a [docker image](https://hub.docker.com/r/larsvanrhijn/sunportal) available on docker hub. This allows you to run only the Flask application and connect a webserver to it (the docker container uses uWSGI). The last and most easy way to set up this application is using the docker-compose file in this repository, below are the instructions on how to do that.

## Installation on raspberry pi (and other systems)

Note that the files in this repository are made for running on a raspberry pi and the default locations that SBFspot uses on these machines. This means that if you are installing this software somewhere else, you might need to change some settings.

1. Install [SBFspot](https://github.com/SBFspot/SBFspot). A great guide for the installation of SBFspot can be found [here](https://github.com/SBFspot/SBFspot/wiki/Installation-Linux-SQLite#sbfspot-with-sqlite).
2. Install Docker, the most easy way to install docker is to use the following command: ``curl -sSL https://get.docker.com | sh``.
3. Docker might ask to add the ``pi`` user to the Docker group, please do so by executing ``sudo usermod -aG docker pi`` (this might be different on other systems). After executing this command, log out and log back in again.
4. First make sure ``pip3`` is installed: ``sudo apt install python3-pip``.
5. Now install ``docker-compose``, this allows us to use the configuration file in the ``SunPortal`` repository. Run ``pip3 install docker-compose``.
6. Now try to see if ``docker-compose`` works, run ``docker-compose version`` to see if ``docker-compose`` is working. If ``docker-compose`` is not working, try to add ``docker-compose`` to PATH. Execute ``export PATH=$HOME/.local/bin:$PATH`` to add it for this session, execute ``echo 'PATH=$HOME/.local/bin:$PATH' >> $HOME/.profile`` to add it permanently to PATH. If you use the last method you need to log out and log back in again.
7. The hard part is done! Now clone this repository ``git clone https://github.com/KiOui/SunPortal.git`` and go to the repository folder ``cd Sunportal``.
8. The ``docker-compose.yml`` file contains information about the containers we are about to start. The default settings are already inside the ``docker-compose.yml`` configuration file. If you need to adjust them, open ``docker-compose.yml`` (``nano docker-compose.yml``) and adjust the settings. Particularly, the location of the database is stored under ``services > sunportal > volumes > - /home/pi/smadata/SBFspot.db:/sunportal/db/database.db``. Adjust the ``/home/pi/smadata/SBFspot.db`` part to the location of the ``SBFspot.db`` database on your system if it is different.
9. Now, inside the ``SunPortal`` folder, run ``docker-compose up -d`` to start the docker containers. They will first start downloading and then begin running. If the command finished succesfully, check the raspberry pi server to see if it worked! The webserver should be running on port 80.