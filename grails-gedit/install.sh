#!/bin/sh

#Added directory structure verification
MIME_PACKAGES="/usr/share/mime/packages/"
GTKSOURCEVIEW="/usr/share/gtksourceview-2.0/language-specs/"
# TAGLIST="/usr/share/gedit-2/plugins/taglist/"
BASH_COMPLETION="/etc/bash_completion.d"
PLUGINS="$HOME/.gnome2/gedit/plugins/"
SNIPPETS="$HOME/.gnome2/gedit/snippets/"

if [ ! -d $MIME_PACKAGES ]; then
	echo "$MIME_PACKAGES doesn't exist. Creating..."
	sudo mkdir $MIME_PACKAGES
fi

if [ ! -d $GTKSOURCEVIEW ]; then
	echo "$GTKSOURCEVIEW doesn't exist. Creating..."
	sudo mkdir $GTKSOURCEVIEW
fi

#if [ ! -d $TAGLIST ]; then
#	echo "$TAGLIST doesn't exist. Creating..."
#	sudo mkdir $TAGLIST
#fi

if [ ! -d $PLUGINS ]; then
	echo "$PLUGINS doesn't exist. Creating..."
	sudo mkdir $PLUGINS
fi

if [ ! -d $SNIPPETS ]; then
	echo "$SNIPPETS doesn't exist. Creating..."
	sudo mkdir $SNIPPETS
fi

#All directories should exist now, proceed with copy
sudo cp ./groovy-mime.xml /usr/share/mime/packages/
sudo cp ./groovy.lang /usr/share/gtksourceview-2.0/language-specs/
sudo cp ./gsp-mime.xml /usr/share/mime/packages/
sudo cp ./gsp.lang /usr/share/gtksourceview-2.0/language-specs/
sudo cp ./grails_commands $BASH_COMPLETION
#sudo cp ./Grails.tags.gz /usr/share/gedit-2/plugins/taglist/
#copy the snippets xml files
sudo cp ./snippets/groovy.xml $SNIPPETS
sudo cp ./snippets/gsp.xml $SNIPPETS

sudo update-mime-database /usr/share/mime
