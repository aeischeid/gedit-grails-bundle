#!/bin/sh

sudo cp ./groovy-mime.xml /usr/share/mime/packages/
sudo cp ./groovy.lang /usr/share/gtksourceview-2.0/language-specs/
sudo cp ./gsp-mime.xml /usr/share/mime/packages/
sudo cp ./gsp.lang /usr/share/gtksourceview-2.0/language-specs/
sudo cp ./Grails.tags.gz /usr/share/gedit-2/taglist/

sudo update-mime-database /usr/share/mime

