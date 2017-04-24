# solidserver-challenge hook for `dehydrated`

This is a hook for the [Let's Encrypt](https://letsencrypt.org/) ACME client [dehydrated](https://github.com/lukas2511/dehydrated) (previously known as `letsencrypt.sh`) that allows you to use [Efficientip SolidServer] DNS records to respond to `dns-01` challenges. Requires Python and your credentials to access the Efficientip SolidServer. 

## Installation

```bash
$ cd ~
$ git clone https://github.com/lukas2511/dehydrated
$ cd dehydrated
$ mkdir hooks
$ git clone https://github.com/berni69/solidserver-challenge.git hooks
```

## Configuration

You need set up your environment in order to connect with dns server. To do that, you should modify `solid-hook.py`, username and password must be encoded in base64:

```python
name_server="ns.example.com"
headers = {'X-IPM-Username':'<username b64>','X-IPM-Password':'<password b64>'}
```



## Usage

```bash
$ ./dehydrated --cron --domain example.com --challenge dns-01 --hook 'hooks/solid-hook.py'
```
