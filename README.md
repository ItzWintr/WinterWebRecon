# WinterWebRecon (wwtool)

A powerful, modular, and installable CLI tool for web reconnaissance.

## Features

- IP resolution
- robots.txt and sitemap.xml detection
- Common path brute-forcing
- Subdomain enumeration
- Tech detection from headers

## Usage

```bash
wwtool -u [target] [options]
EXAMPLE:
wwtool -u https://target.com --brute --sitemap -t -sD
