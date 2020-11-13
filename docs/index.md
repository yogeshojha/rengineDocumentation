# Welcome

## **reNgine**

**reNgine** is an automated reconnaissance framework meant information gathering during penetration testing of web applications. **reNgine** has pipeline of highly configurable reconnaissance steps. With the integration of various open source information gathering tools, **reNgine**, uses all or some of them depending upon the configuration and gathers the results at a single place.

## reNgine current capabilities

!!! example "reNgine capabilities"
    * **Subdomain Discovery**: Discovers all the subdomains using tools like sublist3r, subfinder, amass, assetfinder, etc.
    * **Port Scan**: Use to identify the open ports on the subdomains that have been discovered. Currently reNgine uses naabu to check for open ports. *We have plans to use masscan in the future.*
    * **Directory and File Search**: Uses `dirsearch` to discover the directories and files.
    * **Fetch all Endpoints**: Fetches all the urls for each subdomains from various sources like Open Threat Exchange, Wayback machine, common crawl etc. reNgine uses `gau`, `hakrawler` to fetch the endpoints.
    * **Vulnerability Scan** *(Beta)*: reNgine uses `nuclei` to perform the Vulnerability Scans on the targets.

This documentation is designed for both Developers and Penetration Testers.

* [I am a Developer](developer/)

* [I am a Pentester](pentester/install.md)
    * [Introduction](pentester/install/#for-penetration-testers)
        * [Prerequisites](pentester/install/#prerequisites)
        * [Installation Instructions](/pentester/install/#rengine-installation)
    * [Usage](/pentester/usage/)
    * [Defining Scan Engines](/pentester/scan_engine/)
    * [Adding and Importing Targets](/pentester/usage/#targets)
    * [reNgine Configurations](/pentester/usage/#configurations)
    * [Wordlist](/pentester/usage/#wordlist)
    * [Notification](/pentester/usage/#notification)
    * [Initiating Scan](/pentester/usage/#initiating-scan)
        * [Scan Status](/pentester/usage/#scan-status)
    * [Scheduling Scan](/pentester/usage/#scheduling-scan)
    * [Vulnerability Scan (Beta)](/pentester/usage/#vulnerability-scan-beta)
    * [YAML configuration for Scan Engine](/pentester/scan_engine/)

!!! warning ""
    This documentation is currently under construction. [Help me build this documentation](https://github.com/yogeshojha/rengineDocumentation).

reNgine uses these tools and utilities, and would like to thank the developers for such awesome tools. reNgine would not have been possible without the usage of these tools. **Thank you!**

* [Project Discovery](https://github.com/projectdiscovery)
    * [nuclei](https://github.com/projectdiscovery/nuclei)
    * [httpx](https://github.com/projectdiscovery/httpx)
    * [naabu](https://github.com/projectdiscovery/naabu)
    * [subfinder](https://github.com/projectdiscovery/subfinder)
* [OWASP](https://github.com/OWASP)
    * [amass](https://github.com/OWASP/Amass)
* [Michael Henriksen](https://github.com/michenriksen)
    * [aquatone](https://github.com/michenriksen/aquatone)
* [Ahmed Aboul-Ela](https://github.com/aboul3la)
    * [Sublist3r](https://github.com/aboul3la/sublist3r)
* [Tom Hudson](https://github.com/tomnomnom)
    * [assetfinder](https://github.com/tomnomnom/assetfinder)
* [Corben Leo](https://github.com/lc)
    * [gau](https://github.com/lc/gau)
* [Luke Stephens](https://github.com/hakluke)
    * [hakrawler](https://github.com/hakluke/hakrawler)
* [Mauro Soria](https://github.com/maurosoria)
    * [dirsearch](https://github.com/maurosoria/dirsearch)
