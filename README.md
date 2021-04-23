Template layout for generate bali style service quickly  
Using pre-commit, flake8, isort, black, tox

```shell
pip install cookiecutter
cookiecutter https://github.com/Ed-XCF/cookiecutter-bali.git
```

After you enter the venv:
```shell
bali build
pb2py services/rpc/{{repo_name}}_pb2.py > services/rpc/{{repo_name}}_schema.py
```
