.ONESHELL: 

SHELL = /bin/zsh
CONDA_ACTIVATE = source $$(conda info --base)/etc/profile.d/conda.sh ; conda activate ; conda activate

preview: 
	$(CONDA_ACTIVATE) ml-0451
	quarto preview 

render:
	$(CONDA_ACTIVATE) ml-0451
	quarto render

init_teams:
	$(CONDA_ACTIVATE) ml-0451
	python utils/teams.py init

teams:
	$(CONDA_ACTIVATE) ml-0451
	python utils/teams.py teams

shuffle: 
	$(CONDA_ACTIVATE) ml-0451
	python utils/teams.py shuffle

clean: 
	find . -type f -name "* [0-9]*" -delete
	find . -name "* [0-9]*" -type d -exec rm -r "{}" \;
