# Changelog

This section contains the changes happened in reNgine.

## Backwards Compatibility Check

Please ensure backwards compatibility before updating reNgine.

| Version                                                      | Backwards Compatible |
|--------------------------------------------------------------|----------------------|
| 1.1                                                          | ❌ Not Compatible            |
| 1.0.1                                                          | ✔️ Compatible upto 1.0            |
| 1.0                                                          | ❌ Not Compatible                  |
| 0.5.3                                                          | ✔️ Compatible                  |
| 0.5.2                                                          | ✔️ Compatible                  |
| 0.5.1                                                          | ✔️ Compatible                  |
| 0.5                                                          | ✔️ Compatible                  |
| 0.4                                                          | ✔️ Compatible                  |
| 0.3                                                          | ✔️ Compatible                  |
| 0.2                                                          | ✔️ Compatible                  |
| 0.1                                                          | ✔️ Compatible                  |

## 🏷️ 1.1
**Release Date: Apr 24, 2022**

- Redeigned UI
- Added Subscan Feature

    Subscan allows further scanning any subdomains. Assume from a normal recon process you identified a subdomain that you wish to do port scan. Earlier, you had to add that subdomain as a target. Now you can just select the subdomain and initiate subscan.

- Ability to Download reconnaissance or vulnerability report
- Added option to customize report, customization includes the look and feel of report, executive summary etc.

- Add IP Address from IP
- WHOIS Addition on Detail Scan and fetch whois automatically on Adding Single Targets
- Universal Search Box
- Addition of Quick Add menus
- Added ToolBox Feature

    ToolBox will feature most commonly used recon tools. One can use these tools to identify whois, CMSDetection etc without adding targets. Currently, Whois, CMSDetector and CVE ID lookup is supported. More tools to follow up.

- Notify New Releases on reNgine if available
- Tools Arsenal Section to feature preinstalled and custom tools
- Ability to Update preinstalled tools from Tools Arsenal Section
- Ability to download/add custom tools
- Added option for Custom Header on Scan Engine
- Added CVE_ID, CWE_ID, CVSS Score, CVSS Metrics on Vulnerability Section, this also includes lookup using cve_id, cwe_id, cvss_score etc
- Added curl command and references on Vulnerability Section
- Added Columns Filtering Option on Subdomain, Vulnerability and Endpoints Tables
- Added Error Handling for Failed Scans, reason for failure scan will be displayed
- Added Related Domains using WHOIS
- Added Related TLDs
- Added HTTP Status Breakdown Widget
- Added CMS Detector
- Updated Visualization
- Option to Download Selected Subdomains
- Added additional Nuclei Templates from https://github.com/geeknik/the-nuclei-templates
- Added SSRF check from Nagli Nuclei Template
- Added option to fetch CVE_ID details
- Added option to Delete Multiple Scans
- Added ffuf as Directory and Files fuzzer
- 
- Added widgets such as Most vulnerable Targets, Most Common Vulnerabilities, Most Common CVE IDs, Most Common CWE IDs, Most Common Vulnerability Tags


## 🏷️ 1.0.1

**Release Date: Aug 29, 2021**

**Changelog**

- Fixed [#482](https://github.com/yogeshojha/rengine/issues/482) Endpoints and Vulnerability Datatable were showing results of other targets due to the scan_id parameter
- Fixed [#479](https://github.com/yogeshojha/rengine/issues/479) where the scan was failing due to recent httpx release, change was in the JSON output
- Fixed [#476](https://github.com/yogeshojha/rengine/issues/476) where users were unable to click on Clocked Scan (Reported only on Firefox)
- Fixed [#442](https://github.com/yogeshojha/rengine/issues/442) where an extra slash was added in Directory URLs
- Fixed [#337](https://github.com/yogeshojha/rengine/issues/337) where users were unable to link custom wordlist
- Fixed [#436](https://github.com/yogeshojha/rengine/issues/436) Checkbox in Notification Settings were not working due to same name attribute, now fixed
- Fixed [#439](https://github.com/yogeshojha/rengine/issues/439) Hakrawler crashed if the deep mode was activated due to -plain flag
- Fixed [#437](https://github.com/yogeshojha/rengine/issues/437) If Out of Scope subdomains were supplied, the scan was failing due to None value
- Fixed [#424](https://github.com/yogeshojha/rengine/issues/424) Multiple Targets couldn't be scanned

**Improvements**

- Enhanced install script, check for if docker is running service or not #468

**Security**

- Fixed Cross Site Scripting
    - [#460](https://github.com/yogeshojha/rengine/issues/460)
    - [#457](https://github.com/yogeshojha/rengine/issues/457)
    - [#454](https://github.com/yogeshojha/rengine/issues/454)
    - [#453](https://github.com/yogeshojha/rengine/issues/453)
    - [#459](https://github.com/yogeshojha/rengine/issues/459)
    - [#460](https://github.com/yogeshojha/rengine/issues/460)
- Fixed Cross Site Scripting reported on Huntr [#478](https://github.com/yogeshojha/rengine/issues/478)
    [https://www.huntr.dev/bounties/ac07ae2a-1335-4dca-8d55-64adf720bafb/](https://www.huntr.dev/bounties/ac07ae2a-1335-4dca-8d55-64adf720bafb/)

## 🏷️ 1.0

Release Date: Aug 15, 2021

After several months of work, I am excited to announce reNgine 1.0. In a nutshell, 1.0, is feature-packed with a lot of exciting features that are sure to ease your recon game.

[You may watch the trailer here](https://www.youtube.com/watch?v=_jBf_9qEG3U)

- **Introducing Dark Mode, a feature you all have been asking for, is finally here.**
- **Recon Data visualization**

    Recon Data visualization is the representation of recon data like subdomain, ips, endpoints, ports, vulnerabilities etc into the visual format like Trees and Charts.

- **Improved correlation among recon data**

    A considerable amount of effort has been spent on making sure that the correlation between recon data is consistent. With this improved correlation, you will now be able to identify recon data like, how many of the subdomains uses X as technology, how many of the subdomains use X.X.X.X as IP, etc. This also means that you will be able to see the number of vulnerabilities that a subdomain has, right from the subdomain table.

- **Ability to identify Interesting Subdomains.**

    reNgine uses certain keywords like admin, cpanel, ftp, dashboard to find what is interesting for you. Users will also be able to add their own keywords and choose conditions like, "A subdomain in an interesting subdomain if it matches this keyword but also HTTP status is 200". This allows you to identify what's the most important subdomains to attack against and super useful if you have a very large number of subdomains.

- **Ability to Automatically report Vulnerabilities to Hackerone with customizable vulnerability report.**

    I am excited about the possibilities of Hackerone api, this feature allows you to automatically report the vulnerability to HackerOne if a Critical or High vulnerability is found. Stay ahead of the game! What's exciting is that you also have an option to edit the vulnerability report. To prevent spamming triagers, I've made sure that only Critical and High vulnerabilities are reported. While you will still have an option to manually report the rest of the vulnerabilities.

- **Introducing OSINT Capabilities**

    OSINT is one of the most required features in any recon engine, and beginning 1.0, reNgine comes with OSINT capabilities. This includes support for Dorking, Employees, Emails, Leaked Passwords, etc to be searched.

- **Recon Todo**

    A good recon engine also requires a Todo feature, the idea is that you will be able to recon, add your recon todo or notes right inside reNgine. You will have an option to add todo for your Scan History, for your particular subdomain, or just a TODO! Anything is supported. You can also prioritize by making the Todo important.

- **Proxy Support**

    Proxies are an integral part of any web scraping. Every website has a limit to the certain number of requests for a certain period of time from a particular IP Address that it will allow, exceeding the limit will block incoming requests from such IP Address for a specific period of time.
    And this is especially true for Dorking and other OSINT reNgine does. After certain Dorking attempts Google is likely to ban your IP for a certain period of time. So using a proxy was a must. Introducing proxy support for reNgine, you will have an option to add hundreds of proxies, and reNgine will pick one of them randomly during the scan.

- **GF support**

    GF is an awesome tool for pattern matching in URLs! A lot of fellow hackers wanted GF support in reNgine. We now bring GF support with an option to upload your own custom GF template.

- **Screenshot Gallery with Filters**

    This probably was the most requested feature in reNgine. A recon engine is incomplete without a screenshot gallery. I am also excited to let you know that, the screenshot gallery also comes with filters, you will have an option to add filters like HTTP status, IP Address, Port, Services, and Technology. And, filters will also come with an autosuggestion feature.

- **Powerful recon data filtering with auto-suggestions**

    Recon data filtering was one of the most important features in reNgine, recon data is huge, and we do not want you to get lost, or spend a lot of time looking for the right recon data. So, presenting you, recon data filtering with autosuggestions. You will now be able to see a search bar in Subdomains Table, URLs, Vulnerabilities Table which will auto-suggest the col names. You can combine multiple queries using &, |, etc.

    !!! Example
          `gf_patterns=lfi&http_status=200&content_length>0`

    The possibilities are endless...

- **Recon Data changes, finds new/removed subdomains/endpoints**

    reNgine will now compare your last two scans to find out the recon data changes. You will have an option to send the changes to your notification channels as well. Super helpful while doing continuous monitoring on a target. Inside the scan dashboard, you will now see a separate section for Recon Data changes, which will identify any added or removed subdomains or endpoints.

- **Tagging of targets into Organization**

    There are times when you wish to perform a scan for all the targets that belong to an organization. reNgine 1.0 allows you to tag multiple targets to an organization and initiate or schedule scans with one click.

- **Support for custom GF patterns and Nuclei Templates**

    While nuclei was a part of the earlier release, but there wasn't any easy way to upload your custom nuclei templates. Now, you will have an option to add your custom GF or Nuclei templates right from the UI. You will also have an option to view the template.

- **Support for editing tool-related configuration files (Nuclei, Subfinder, Naabu, amass)**

    Tools like Nuclei, Subfinder uses configuration files to pass API keys and certain tool-related settings. We now bring an option to directly **edit** tool-related configuration files right from reNgine UI. This means you will also be able to view them.

- **Option to Mark Subdomains as important**

    This is a tiny little feature that will allow you to mark any subdomain as important! Watch out for a star icon on the subdomains table, you'll be able to mark them as important.

- **Separate tab for Directory scan results**

    It is true that directory scan results were breaking the subdomains table, from a UX perspective, it was not a really good idea to show everything in the subdomains table. So, a new tab has been added just for directory scan results.

- **Option to Import and Export Subdomains and export endpoints**

    Interoperability is something every recon tool needs, and reNgine is no different. You will now be able to import subdomains from your private recon tools to any scan before you initiate. You will see this option to import the subdomain just after you choose the scan engine. In the same section, you will also see an option to exclude subdomains.

    We also now allow you to download subdomains, or just download subdomains marked as important, or just download subdomains that are interesting. This also applies to endpoints, you can download all endpoints, just download any endpoints that have certain GF patterns matched.

- **Clean your scan results and screenshots**

    I understand most of you run reNgine on your VPS, and it is very understandable that you wish to clean scan results, screenshots to save up some space. reNgine now allows you to clean up your scan data and/or screenshots.

- **Enhanced and Customizable Scan alert with support for Slack, Discord & Telegram, also send recon data directly to Discord**

    Notification in the earlier version of reNgine was not very efficient, and support was only for slack. reNgine 1.0 comes with support for Slack, Discord, and Telegram. You will also have an option to customize what kind of notification to be sent, only want vulnerability-related notifications? You can choose that, only want subdomains changes? You can choose them as well. You also have an option to upload these scan data directly to your discord.

- You can view the complete changelog here: [https://github.com/yogeshojha/rengine/blob/master/CHANGELOG.md](https://github.com/yogeshojha/rengine/blob/master/CHANGELOG.md)


There are a lot more tiny improvements that I worked on for several months that are sure to give you a better experience, and let you stay ahead in the recon game! I really appreciate any feedback and suggestions.


## 🏷️ 0.5.3

**Release Date: Feb 25 2021**

- Build error for Naabu v2 Fixed
- Added rate support for Naabu

## 🏷️ 0.5.2

**Release Date: Feb 23 2021**

- Fixed XSS https://github.com/yogeshojha/rengine/issues/347

## 🏷️ 0.5.1

**Release Date: Feb 19 2021**

Features

- Added Discord Support for Notification Web hooks

## 🏷️ 0.5

Release Date: 29 Nov 2020

- Nuclei Integration: v0.5 is primarily focused on vulnerability scanner using Nuclei. This was a long pending due and we've finally integrated it.

- Powerful search queries across endpoints, subdomains and vulnerability scan results: reNgine reconnaissance data can now be queried using operators like <,>,&,| and !, namely greater than, less than, and, or, and not. This is extremely useful in querying the recon data. More details can be found at Instructions to perform Queries on Recon data

- Out of scope options: Many of you have been asking for out of scope option. Thanks to Valerio Brussani for his pull request which made it possible for out of scope options. Please check the documentation on how to define out of scope options.

- Official Documentation(WIP): We often get asked on how to use reNgine. For long, we had no official documentation. Finally, I've worked on it and we have the official documentation at rengine.wiki

    The documentation is divided into two parts, for Developers and for Penetration Testers. For developers, it's a work in progress. I will keep you all updated throughout the process.

- Redefined Dashboard: We've also made some changes in the Dashboard. The additions include vulnerability scan results, most vulnerable targets, most common vulnerabilities.

- Global Search: This feature has been one of the most requested features for reNgine. Now you can search all the subdomains, endpoints, and vulnerabilities.

- OneForAll Support: reNgine now supports OneForAll for subdomain discovery, it is currently in beta. I am working on how to integrate OneForAll APIKeys and Configuration files.

- Configuration Support for subfinder: You will now have ability to add configurations for subfinder as well.

- Timeout option for aquatone: We added timeout options in yaml configuration as a lot of screenshots were missing. You can now define timeout for http, scan and screenshots for timeout in milliseconds.

- Design Changes A lot of design changes has happened in reNgine. Some of which are:

- Endpoints Results and Vulnerability Scan Results are now displayed as a separate page, this is to separate the results and decrease the page load time.
- Checkbox next to Subdomains and Vulnerability report list to change the status, this allows you to mark all subdomains and vulnerabilities that you've already completed working on.
- Sometimes due to timeout, aquatone was skipping the screenshots and due to that, navigations between screenshots was little annoying. We have fixed it as well.
- Ability to delete multiple targets and initiate multiple scans.
- Subdomain Takeover (Removed): As we decided to use Nuclei for Vulnerability Scanner, and also, since Subjack wasn't giving enough results, I decided to remove Subjack. The subdomain Takeover will now be part of Nuclei Vulnerability Scanner.

## 🏷️ 0.4

**Release Date: 2020-10-08**

Features

- Background tasks migrated to Celery and redis
- Periodic and clocked scan added
- Ability to Stop and delete the scan
- CNAME and IP address added on detail scan
- Content type added on Endpoints section
- Ability to initiate multiple scans at a time

## 🏷️ 0.3

**Release Date: 2020-07-21**

Features

- YAML based Customization Engine
- Ability to add wordlists
- Login Feature

## 🏷️ 0.2

**Release Date: 2020-07-11**

Features

- Directory Search Enabled
- Fetch URLS using hakrawler
- Subdomain takeover using Subjack
- Add Bulk urls
- Delete Scan functionality

Fix

- Windows Installation issue fixed
- Scrollbar Issue on small screens fixed


## 🏷️ 0.1

**Release Date: 2020-07-08**

reNgine is released
