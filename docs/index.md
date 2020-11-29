# Welcome

## **reNgine**

**reNgine** is an automated reconnaissance framework meant information gathering during penetration testing of web applications. **reNgine** has pipeline of highly configurable reconnaissance steps. With the integration of various open source information gathering tools, **reNgine**, uses all or some of them depending upon the configuration and gathers the results at a single place.

!!! check "What's new in reNgine v0.5?"
    After months of work, reNgine is finally ready for v0.5 release. v0.5 brings some of the exciting features that you all have been asking for!

    **++Nuclei Integration**: v0.5 is primarily focused on vulnerability scanner using Nuclei. This was a long pending due and we've finally integrated it.

    **++Powerful search queries across endpoints, subdomains and vulnerability scan results**: reNgine reconnaissance data can now be queried using operators like <,>,&,| and !, namely greater than, less than, and, or, and not. This is extremely useful in querying the recon data. More details can be found at [Instructions to perform Queries on Recon data](/pentester/search)

    **++Out of scope options**: Many of you have been asking for out of scope option.
    Thanks to [Valerio Brussani](https://github.com/valbrux) for his pull request which made it possible for out of scope options.
    Please check the documentation on [how to define out of scope](/pentester/scan_engine/#excluded_subdomains) options.

    **++Official Documentation(WIP)**: We often get asked on how to use reNgine. For long, we had no official documentation. Finally, I've worked on it and we have the official documentation at [rengine.wiki](https://rengine.wiki)

    *The documentation is divided into two parts, for Developers and for Penetration Testers. For developers, it's a work in progress. I will keep you all updated throughout the process.*

    **++Redefined Dashboard**: We've also made some changes in the Dashboard. The additions include vulnerability scan results, **most vulnerable targets**, **most common vulnerabilities**.

    **++Global Search**: This feature has been one of the most requested features for reNgine. Now you can search all the subdomains, endpoints, and vulnerabilities.

    **++OneForAll Support**: reNgine now supports OneForAll for subdomain discovery, it is currently in beta. I am working on how to integrate OneForAll APIKeys and Configuration files.

    **++Configuration Support for subfinder**: You will now have ability to add configurations for subfinder as well.

    **++Timeout option for aquatone**: We added timeout options in yaml configuration as a lot of screenshots were missing. You can now define timeout for http, scan and screenshots for timeout in milliseconds.

    **++Design Changes**
    A lot of design changes has happened in reNgine. Some of which are:

    * Endpoints Results and Vulnerability Scan Results are now displayed as a separate page, this is to separate the results and decrease the page load time.
    * Checkbox next to Subdomains and Vulnerability report list to change the status, this allows you to mark all subdomains and vulnerabilities that you've already completed working on.
    * Sometimes due to timeout, aquatone was skipping the screenshots and due to that, navigations between screenshots was little annoying. We have fixed it as well.
    * Ability to delete multiple targets and initiate multiple scans.

    **--Subdomain Takeover**: As we decided to use Nuclei for Vulnerability Scanner, and also, since Subjack wasn't giving enough results, I decided to remove Subjack. The subdomain Takeover will now be part of Nuclei Vulnerability Scanner.

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
    * [Performing advanced lookup on recon results](/pentester/search/)
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
