#!/bin/sh

#Added directory structure verification
MIME_PACKAGES="/usr/share/mime/packages/"
GTKSOURCEVIEW="/usr/share/gtksourceview-2.0/language-specs/"
TAGLIST="/usr/share/gedit-2/taglist/"

if [ ! -d $MIME_PACKAGES ]; then
	echo "$MIME_PACKAGES doesn't exists. Creating..."
	sudo mkdir $MIME_PACKAGES
fi

if [ ! -d $GTKSOURCEVIEW ]; then
	echo "$GTKSOURCEVIEW doesn't exists. Creating..."
	sudo mkdir $GTKSOURCEVIEW
fi

if [ ! -d $TAGLIST ]; then
	echo "$TAGLIST doesn't exists. Creating..."
	sudo mkdir $TAGLIST
fi	

#All directories should exist now, proceed with copy
sudo cp ./groovy-mime.xml /usr/share/mime/packages/
sudo cp ./groovy.lang /usr/share/gtksourceview-2.0/language-specs/
sudo cp ./gsp-mime.xml /usr/share/mime/packages/
sudo cp ./gsp.lang /usr/share/gtksourceview-2.0/language-specs/
sudo cp ./Grails.tags.gz /usr/share/gedit-2/taglist/

sudo update-mime-database /usr/share/mime
