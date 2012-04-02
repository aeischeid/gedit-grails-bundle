#!/bin/sh

#Added directory structure verification
MIME_PACKAGES="/usr/share/mime/packages/"
GTKSOURCEVIEW="/usr/share/gtksourceview-2.0/language-specs/"
TAGLIST="/usr/share/gedit/plugins/taglist/"
BASH_COMPLETION="/etc/bash_completion.d/"
PLUGINS="$HOME/.gnome2/gedit/plugins/"
SNIPPETS="$HOME/.gnome2/gedit/snippets/"
STYLES="$HOME/.gnome2/gedit/styles/"
SCRIPTS="/usr/local/bin/"

if [ ! -d $MIME_PACKAGES ]; then
	echo "$MIME_PACKAGES doesn't exist. Creating..."
	sudo mkdir -p $MIME_PACKAGES
fi

if [ ! -d $GTKSOURCEVIEW ]; then
	#Let's try version 3 first.
	GTKSOURCEVIEW="/usr/share/gtksourceview-3.0/language-specs/"
	
	if [ ! -d $GTKSOURCEVIEW ]; then
		echo "$MIME_PACKAGES doesn't exist. You may need to install missing requirments. Creating..."
		sudo mkdir -p $GTKSOURCEVIEW
	fi
fi

if [ ! -d $TAGLIST ]; then
	echo "$TAGLIST doesn't exist. Creating..."
	sudo mkdir -p $TAGLIST
fi

if [ ! -d $PLUGINS ]; then
	echo "$PLUGINS doesn't exist. Creating..."
	sudo mkdir -p $PLUGINS
fi

if [ ! -d $SNIPPETS ]; then
	echo "$SNIPPETS doesn't exist. Creating..."
	sudo mkdir -p $SNIPPETS
fi

#All directories should exist now, proceed with copy
sudo cp ./groovy-mime.xml $MIME_PACKAGES
sudo cp ./groovy.lang $GTKSOURCEVIEW
sudo cp ./gsp-mime.xml $MIME_PACKAGES
sudo cp ./gsp.lang $GTKSOURCEVIEW
sudo cp ./grails_commands $BASH_COMPLETION
sudo cp ./gred $SCRIPTS
sudo chmod +x /usr/local/bin/gred
sudo cp ./Grails.tags.gz $TAGLIST
#copy the snippets xml files
sudo cp ./snippets/groovy.xml $SNIPPETS
sudo cp ./snippets/gsp.xml $SNIPPETS

sudo update-mime-database /usr/share/mime
clear
echo "Install succesfull!\r\n" 


