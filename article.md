# FastAPI with JWT and API key
Build a FASTAPI service using a JWT to securely authenticate an API Key.  

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

## Use Case
_This is appropriate for a service meant to be used application(s) also under your control.  If it is generally available to multiple clients, you should probably have an API Key per client.  Even if you do, this is a good way to understand the basic principle of how to do this in FastAPI._

## Getting started
For this example we use [poetry](https://python-poetry.org/) as the dependency and package management.  If you don't like poetry, feel free to use your favorite (pyenv, conda, etc).  To install poetry, see [here](https://python-poetry.org/docs/#installation).  

### OSX Installation 
Poetry requires [pipx](https://pipx.pypa.io/stable/installation/).  It can be installed on OSX via [homebrew](https://brew.sh/)  
```bash
brew install pipx
pipx install poetry
```

## Create your app
With poetry installed, you can create your initial FastAPI service:
```bash
poetry new fast-api-jwt
cd fast-api-jwt
``` 

### Project setup
* Edit pyproject.toml and ensure it looks like [this](https://raw.githubusercontent.com/tangledpath/fast-api-jwt/master/pyproject.toml).  
  * Dependencies are python (3.12), fastapi, httpx, python-jose, uvicorn, python-dotenv, and loguru.
  * We also need pytest and pytest-mock configured as test dependencies.

### Dependency Injection
FastAPI provides a [dependency](https://fastapi.tiangolo.com/tutorial/dependencies/) injection mechanism.  We will use that to 



## Summary
There we have it; a FASTAPI that uses a JWT to verify the API Key.
This project can be found in its entirety at https://github.com/tangledpath/fast-api-jwt
