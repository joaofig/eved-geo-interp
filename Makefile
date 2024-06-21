BIN = ./venv/bin/
PYTHON = $(BIN)python
UV = ./venv/bin/uv

install:
	pyenv install --skip-existing
	pyenv exec python -m venv venv
	$(BIN)pip install uv
	$(UV) pip sync requirements/run.txt

uninstall:
	rm -rf venv

compile:
	$(UV) pip compile requirements/run.in -o requirements/run.txt

sync:
	$(UV) pip sync requirements/run.txt

download-data:
	git clone https://bitbucket.org/datarepo/eved_dataset.git ../eved_tmp
	cp ../eved_tmp/data/eVED.zip ./data
	rm -rf ../eved_tmp
	7z x data/eVED.zip
	mv eVED data
	rm data/eVED.zip
	sed 's/;//g' data/eVED/eVED_180124_week.csv > data/eVED/no_semi.csv
	mv data/eVED/no_semi.csv data/eVED/eVED_180124_week.csv
	rm data/eVED/no_semi.csv
