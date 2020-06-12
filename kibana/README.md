
- The presentation "slides" are on `presentation.md`. It is a simple markdown
  text file.

- If you want to "play" it as a presentation, install
  [mdp](https://github.com/visit1985/mdp) and run: 'make present'

- There is another file called `recommended_readings.md` that has the reference
  material used on the presentation, and can be used as a starting point to
deepen your studies.

- There are python scripts to populate data to elasticsearch. Read the
  docstrings on the beginning of each file so you can understand what you can
do with each one. A `requirements.txt` file was also provided so that you can
start a virtualenv to run the scripts.

- There are 2 docker-composes. One has an old version of Kibana that we
  currently use at dft, as the other one has a more recent version of it, which
has the "Machine Learning" functionality you can use to explore data.

- To summon a sandbox for your testing, you must:

1) Create a python virtualenv with the requirements file

2) Raise the elasticsearch/kibana containers:


```
make docker-compose-current-up
# or
make docker-compose-dft-up
```

3) Run the scripts to populate data:

```
make populate-simple`
make populate-bulk`
```


4) Then, to open the kibana dashboard on your browser:

```
make kibana-dashboard
```
