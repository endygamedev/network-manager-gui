TARGET = network-manager-gui 
PREFIX = /usr/local/bin
ASSETS = /usr/local/lib

.PHONY: all install uninstall update

all:
	echo $(TARGET)

install:
	chmod +x $(TARGET)
	install $(TARGET) $(PREFIX)
	mkdir $(ASSETS)/network-manager-gui
	cp ./src/main.py $(ASSETS)/network-manager-gui/

uninstall:
	sudo rm -rf $(PREFIX)/$(TARGET)
	sudo rm -rf $(ASSETS)/network-manager-gui

update:
	sudo make uninstall
	git pull
	sudo make install
	sudo chmod -R ug+w .;
