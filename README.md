# IP Threat List Ingestion for Illumio ASP

[![Slack](images/slack.svg)](http://slack.illumiolabs.com)
[![License](images/license.svg)](LICENSE)

This program takes external IP Threat Lists as command line parameter or
defaults to one provided and with it and then updates it in Illumio ASP
IP Threat List.

## Dependencies

This program depends on Python 3.x and Illumio ASP REST API v2.

## Installation

As of now the dependencies which needed are documented in requirements.txt, just run the following steps to install them.

```bash
git clone https://github.com/illumiolabs/illumio-ip-threat-list-ingestion.git
cd illumio-ip-threat-list-ingestion
pip install -r requirements.txt
./src/illumio-ip-threat-list-ingestion.py
```

## Usage

The following steps are needed to run the program:
```bash
# First set the enviornment variables needed for the program.
export ILO_API_VERSION=2
export ILO_SERVER=<illumio pce server address> # example: illumiopce.company.com
export ILO_PORT=8443
export ILO_ORG_ID=1
export ILO_API_KEY_ID=6cgdf632628jdncj # the api key from pce without the prefix 'api_'.
export ILO_API_KEY_SECRET=8Xoophookieteipex9ieg9e646c7672hdngc729ksndgdks77cd62147e4
export THREAT_LIST_KEY=135 # ID of the IP List as shown in image below.
```
![](images/threat-list-key.jpg)
```bash
# Finally when you have all the variables set, run the following command, you will see the output as shown.
./src/illumio-ip-threat-list-ingestion.py
ip threat list url is:  https://raw.githubusercontent.com/stamparm/ipsum/master/levels/7.txt
malicious ip threat list fetched successfully.
current pce ip threat list: [ 171.25.193.77 , 171.25.193.20 ...<snip>... 185.100.87.207 ]
duplicate ips found in new list: [ 171.25.193.77 , 171.25.193.20 ...<snip>... 222.186.175.163 ]
ip threat list successfully updated in draft version, trying to provision now.
ip threat list successfully provisioned.
```

## Help or Docs 

If you have questions, please use slack for asking them.
If you have issues, bug reports, etc, please file an issue in this repository's Issue Tracker.

## Support

**IP Threat List Ingestion for Illumio ASP** is released and distributed as open source
software subject to the [LICENSE](LICENSE). Illumio has no obligation or responsibility related to
the **IP Threat List Ingestion for Illumio ASP** with respect to support, maintenance,
availability, security or otherwise. Please read the entire [LICENSE](LICENSE) for additional
information regarding the permissions and limitations. You can engage with the author & contributors
team and community on SLACK.

## Contributing

Instructions on how to contribute:  [CONTRIBUTING](CONTRIBUTING.md).

