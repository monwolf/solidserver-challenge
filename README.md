# solidserver-challenge hook for `dehydrated`

This is a hook for the [Let's Encrypt](https://letsencrypt.org/) ACME client [dehydrated](https://github.com/lukas2511/dehydrated) (previously known as `letsencrypt.sh`) that allows you to use [SolidServer] DNS records to respond to `dns-01` challenges. Requires Python and your credentials to access the SolidServer. 

## Installation

```
$ cd ~
$ git clone https://github.com/lukas2511/dehydrated
$ cd dehydrated
$ mkdir hooks
$ git clone https://github.com/berni69/solidserver-challenge.git hooks
```

## Usage

```
$ ./dehydrated --cron --domain example.com --challenge dns-01 --hook 'hooks/solid-hook.py'
```
