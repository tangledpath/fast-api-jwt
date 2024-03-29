# FastAPI Service 
FastAPI Service with JWT verification and tests.

<p>
  <img src="https://raw.githubusercontent.com/tangledpath/fast-api-jwt/master/fast_api_jwt_sm.png" align="left" width="512"/>
</p>
<p>&nbsp</p>
<p>&nbsp</p>
<p>&nbsp</p>
<p>&nbsp</p>
<p>&nbsp</p>
<p>&nbsp</p>
<p>&nbsp</p>
<p>&nbsp</p>
<p>&nbsp</p>
<p>&nbsp</p>
<p>&nbsp</p>
<p>&nbsp</p>
<p>&nbsp</p>


## Article
Associated article can be found at these locations:
* Personal portfolio: 
* LinkedIn:
* Medium:

## GitHub
https://github.com/tangledpath/fast-api-jwt

## Documentation
https://tangledpath.github.io/fast-api-jwt

## Getting started
Clone repository:
git clone https://github.com/tangledpath/fast-api-jwt.git

## Development
### Linting is done via autopep8
```bash
script/lint.sh
```

### Documentation
```
# Shows in browser
poetry run pdoc fast_api_jwt/
# Generates to ./docs
script/build.sh
```

### Testing
```bash
  clear; pytest
```

### Building and Publishing
#### Building
`poetry build`
#### Publishing
Note: `--build` flag build before publishing
`poetry publish --build -u __token__ -p $PYPI_TOKEN`
