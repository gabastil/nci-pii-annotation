# nci-pii-annotation
`pii` `synthetic reports`

## Generate Random PII

```bash
python -m generators #cli args
```

**CLI Arguments**

Argument | Example | Description
--- | --- | ---
1 | `-t pii` | `-t {pii, mrn, id}` : Type of data to generate
2 | `-l 15` | `-l {1..n}` : Length of ID to generated. Default = 20 characters

Examples

```bash
>> # This will generate a full pii profile including names, SSNs, addresses, and other information
>> user@computer$ python -m generator -t pii
>>
>> # This will generate a medical record number (MRN) that is 9 digits long
>> user@computer$ python -m generator -t mrn -l 9
```

## Compare Document Contents

Use the `python` interpreter. Import and use compare directory.

```python
from compare import compare_directory

# Will return a list of dict of file pairs and a boolean
# indicating whether or not text contents are the same
compare_directory("/path/to/files")
```