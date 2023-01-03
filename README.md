# IDigital Python Integration

[![License][license-badge]][license-url]

> IDigital OpenID Connect integration for Python

## Usage

- Install package

```bash
# Poetry
$ poetry add git+https://github.com/FIEA-AL/idigital-python-integration.git

# Pip
$ pip install git+https://github.com/FIEA-AL/idigital-python-integration.git
```

&nbsp;
- Import package
```python
from idigital_python_integration.IDigital import IDigital
```

&nbsp;
- Instantiate package
```python
idigital = IDigital.create({
    'post_logout_redirect_uri': '<your-application-host>/idigital/auth/logout/callback',
    'issuer': 'https://sso<prod|homo|dev>.idigital.sistemafiea.com.br',
    'redirect_uri': '<your-application-host>/idigital/auth/callback',
    'application_host': '<your-application-host-with-protocol>',
    'client_id': '<your-client-id>'
})
```

&nbsp;
- Fast API Example

```python
@app.get('/login')
def login(request: Request):
    url = idigital.authorize(request.session)
    return RedirectResponse(url, status_code=status.HTTP_303_SEE_OTHER)


@app.get('/logout')
def login(request: Request):
    url = idigital.logout(request.session, reset)
    return RedirectResponse(url, status_code=status.HTTP_303_SEE_OTHER)


@app.get('/idigital/auth/callback')
def callback(request: Request):
    params = dict(request.query_params)
    state = params.get('state')
    code = params.get('code')
    iss = params.get('iss')

    idigital.callback(code, iss, state, request.session)
    return RedirectResponse('/after/login', status_code=status.HTTP_303_SEE_OTHER)


@app.get('/idigital/auth/logout/callback')
def logout_callback():
    return RedirectResponse('/', status_code=status.HTTP_303_SEE_OTHER)
```

## Development

- Clone the repo

```bash
$ git clone https://github.com/FIEA-AL/idigital-python-integration.git
```

- Install dependencies

```bash
# Poetry
$ poetry install

# Pip
$ pip install
```

## Author

[Vitor Barcelos](https://www.linkedin.com/in/vitorbarcelos)

## Contributors
- [Bruno Pereira](https://www.linkedin.com/in/batlopes)
- [Lucas Paz](https://github.com/lucasp165)

## License

[MIT](https://github.com/FIEA-AL/idigital-python-integration/blob/main/LICENSE)

[license-badge]: https://img.shields.io/badge/License-MIT-yellow.svg
[license-url]: https://opensource.org/licenses/MIT
