all: initial_data.json
pokemon.json: build.py tree_structure.json pokemon.txt
	python3 build.py pokemon.json
initial_data.json: json-concat.py pokemon.json tree_structure.json
	python3 json-concat.py tree_structure.json pokemon.json initial_data.json
