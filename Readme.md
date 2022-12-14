# The Knowledge graph generator

The knowledge graph generator is an application that takes malware and attack pattern STIX ID for generating knowledge graphs with a searchable display. If the users do not know the STIX IDs or are unsure about them, they can search for the terms they are looking for, like ransomware, malware name, and attack pattern name, and then our application recommends them the STIX IDs that they might be interested in.

##### you need python and a browser for running this application. Alternatively you can use the server using the links below.

[The knowledge graph generator](https://threatintel99.herokuapp.com/)

## installing the required libraries using pip


```bash
pip install -r requirements.txt
```

## To start the server

```python
python init.py
```
## Usage

If you know the STIX ID enter the STIX ID to generate the knowledge graph.

If you don't know the STIX ID enter the keyword that you are interested about. It will recommend the STIX IDs and their names and you can later enter the STIX IDs to generate Knowledge graphs.





