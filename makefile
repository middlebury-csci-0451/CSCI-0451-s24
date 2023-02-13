.ONESHELL: 


SHELL = /bin/zsh
CONDA_ACTIVATE = source $$(conda info --base)/etc/profile.d/conda.sh ; conda activate ; conda activate


preview: 
	$(CONDA_ACTIVATE) ml-0451
	quarto preview 

render:
	$(CONDA_ACTIVATE) ml-0451
	quarto render

teams:
	$(CONDA_ACTIVATE) ml-0451
	python utils/teams.py assign
	python utils/teams.py teams

shuffle-A:
	$(CONDA_ACTIVATE) ml-0451
	python utils/teams.py shuffle A

shuffle-B:
	$(CONDA_ACTIVATE) ml-0451
	python utils/teams.py shuffle B
