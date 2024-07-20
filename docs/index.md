---
template: index.html
title: 'reNgine 2.0 Redefining the future of reconnaissance!!'
hide:
  - navigation
hero:
  title: 'reNgine <small>2.0</small></br> Redefining the future of reconnaissance!'
  subtitle: '<strong>The only web application recon tool</strong> you will ever need!'
  description: Quickly discover the attack surface, identify vulnerabilities using highly customizable and powerful scan engines. <br><br>Enjoy peace of mind with reNgine's continous monitoring, deeper reconnaissance and open-source powered Vulnerability Scanner.
  install_button: Getting Started
features:
  - title: Reconnaissance like no other!
    description: reNgine has advanced reconnaissance capabilities, harnessing a range of open-source tools to deliver a comprehensive web application reconnaissance experience. With it's intuitive User Interface, it excels in subdomain discovery, pinpointing IP addresses and open ports, collecting endpoints, conducting directory and file fuzzing, capturing screenshots, and performing vulnerability scans. To summarize, it does end-to-end reconnaissance. With WHOIS identification and WAF detection, it offers deep insights into target domains. Additionally, it also identifies misconfigured S3 buckets and find interesting subdomains and URLS, based on specific keywords to helps you identify your next target, making it an go to tool for efficient reconnaissance.
  - title: Configurable Scan Engines!
    description: reNgine offers unparalleled flexibility through its highly configurable scan engines, based on a YAML-based configuration. It offers the freedom to create and customize recon scan engines based on any kind of requirement. Users can tailor them to their specific objectives and preferences, from thread management to timeout settings and rate-limit configurations, everything is customizable. Additionally, reNgine offers a range of pre-configured scan engines right out of the box, including Full Scan, Passive Scan, Screenshot Gathering, and the OSINT Scan Engine. These ready-to-use engines eliminate the need for extensive manual setup, aligning perfectly with reNgine's core mission of simplifying the reconnaissance process and enabling users to effortlessly access the right reconnaissance data with minimal effort.
  - title: Multiple Users, Roles and Permissions <small class="red_badge">2.0</small>
    description: Begining reNgine 2.0, we've taken your web application reconnaissance to a whole new level of control and security. Now, you can assign distinct roles to your team members—Sys Admin, Penetration Tester, and Auditor—each with precisely defined permissions to tailor their access and actions within the reNgine ecosystem. Sys Admin is a super user that has permission to modify system and scan related configurations, scan engines, create new users, add new tools etc. Super user can initiate scans and subscans effortlessly. Penetration Tester will be allowed to modify and initiate scans and subscans, add or update targets, etc. A penetration tester will not be allowed to modify system configurations. Auditor can only view and download the report. An auditor can not change any system or scan related configurations nor can initiate any scans or subscans.
  - title: LLM Report Generation <small class="red_badge">2.0</small>
    description: In addition to its robust reconnaissance capabilities, reNgine goes the extra mile by simplifying the report generation process, recognizing the crucial role that PDF reports play in the realm of end-to-end reconnaissance. Users can effortlessly generate and customize PDF reports to suit their exact needs. Whether it's a Full Scan Report, Vulnerability Report, or a concise reconnaissance report, reNgine provides the flexibility to choose the report type that best communicates your findings. Moreover, the level of customization is unparalleled, allowing users to select report colors, fine-tune executive summaries, and even add personalized touches like company names and footers. With LLM integration, your reports aren't just a report, with remediation steps, and impacts, you get 360-degree view of the vulnerabilities you've uncovered.
  - title: Projects <small class="red_badge">2.0</small>
    description: Say Hello to Projects! reNgine 2.0 introduces a powerful addition that enables you to efficiently organize your web application reconnaissance efforts. With this feature, you can create distinct project spaces, each tailored to a specific purpose, such as personal bug bounty hunting, client engagements, or any other specialized recon task. Each projects will have separate dashboard and all the scan results will be separated from each projects, while scan engines and configuration will be shared across all the projects.
  - title: Support for Subscans!
    description:  Subscan is a game-changing feature in reNgine, setting it apart as the only open-source tool of its kind to offer this capability. With Subscan, waiting for the entire pipeline to complete is a thing of the past. Now, users can swiftly respond to newfound discoveries during reconnaissance. Whether you've stumbled upon an intriguing subdomain and wish to conduct a focused port scan or want to delve deeper with a vulnerability assessment, reNgine has you covered.
  - title: Continuous Monitoring
    description:  Continuous monitoring is at the core of reNgine's mission, and it's robust continuous monitoring feature ensures that their targets are under constant scrutiny. With the flexibility to schedule scans at regular intervals, penetration testers can effortlessly stay informed about their targets. What sets reNgine apart is its seamless integration with popular notification channels such as Discord, Slack, and Telegram, delivering real-time alerts for newly discovered subdomains, vulnerabilities, or any changes in reconnaissance data. One can run clocked scan (Run reconnaissance exactly at X Hours and Y minutes) and Periodic Scans (Runs reconnaissance every X minutes/hours/days/week).
  - title: LLM-Powered Attack Surface Generation <small class="red_badge">2.0</small>
    description: With reNgine 2.0, reNgine seamlessly integrates with LLM to identify the attacks that you can likely perform on a subdomain. By making use of reconnaissance data such as page title, open ports, subdomain name etc, reNgine can advice you the attacks you could perform on a target. reNgine will also provide you the rationale on why the specific attack is likely to be successful.
  - title: Tools Arsenal
    description: Don't like our subdomain discovery tools? Wish to install any external tools? reNgine supports tools of your choice, update them, add them or remove simply from Tools Arsenal section.
  - title: Powerful Recon filtering!
    description: reNgine supports advanced recon lookup queries such as <code>name=admin&http_status=200</code> or <code>cve_id=CVE-1234-5678</code>! Combine multiple queries with operators such as &,| etc.
  - title: Recon data changes!
    description: reNgine can also identify recon data changes. If any new vulnerabilities has been identified, or any subdomain no longer found, reNgine can detect the changes. reNgine can also send recon data changes notifications on your favourite notification channels.
  - title: Customizable Alerts!
    description: Send scan related notifications on your favourite channel such as Discord, Slack or Telegram.
---

## 🥷 Introduction

reNgine is your go-to web application reconnaissance suite that's designed to simplify and streamline the reconnaissance process for security professionals, penetration testers, and bug bounty hunters. With its highly configurable engines, data correlation capabilities, continuous monitoring, database-backed reconnaissance data, and an intuitive user interface, reNgine redefines how you gather critical information about your target web applications.

Traditional reconnaissance tools often fall short in terms of configurability and efficiency. reNgine addresses these shortcomings and emerges as a excellent alternative to existing commercial tools.

reNgine was created to address the limitations of traditional reconnaissance tools and provide a better alternative, even surpassing some commercial offerings. Whether you're a bug bounty hunter, a penetration tester, or a corporate security team, reNgine is your go-to solution for automating and enhancing your information-gathering efforts.

reNgine is not an ordinary reconnaissance suite; it's a game-changer! With the 2.0 release we've turbocharged the traditional workflow with groundbreaking features that is sure to ease your reconnaissance game. reNgine redefines the art of reconnaissance!


## 🧭 Workflow

<img src="https://github.com/yogeshojha/rengine/assets/17223002/10c475b8-b4a8-440d-9126-77fe2038a386">

## ⭐ Features

**reNgine** is packed with features that no any open other source tool provides. Here are some list of cool features supported by reNgine:

* Reconnaissance:
  * Subdomain Discovery
  * IP and Open Ports Identification
  * Endpoints Discovery
  * Directory/Files fuzzing
  * Screenshot Gathering
  * Vulnerability Scan
    * Nuclei
    * Dalfox XSS Scanner
    * CRLFuzzer
    * Misconfigured S3 Scanner
  * WHOIS Identification
  * WAF Detection
* OSINT Capabilities
  * Meta info Gathering
  * Employees Gathering
  * Email Address gathering
  * Google Dorking for sensitive info and urls
* Projects, create distinct project spaces, each tailored to a specific purpose, such as personal bug bounty hunting, client engagements, or any other specialized recon task.
* Perform Advanced Query lookup using natural language alike and, or, not operations
* Highly configurable YAML-based Scan Engines
* Support for Parallel Scans
* Support for Subscans
* Recon Data visualization
* LLM Vulnerability Description, Impact and Remediation generation
* LLM Attack Surface Generator
* LLM Toolkit to download and manage LLM models
* Multiple Roles and Permissions to cater a team's need
* Customizable Alerts/Notifications on Slack, Discord, and Telegram
* Automatically report Vulnerabilities to HackerOne
* Recon Notes and Todos
* Clocked Scans (Run reconnaissance exactly at X Hours and Y minutes) and Periodic Scans (Runs reconnaissance every X minutes/- hours/days/week)
* Proxy Support
* Screenshot Gallery with Filters
* Powerful recon data filtering with autosuggestions
* Recon Data changes, find new/removed subdomains/endpoints
* Tag targets into the Organization
* Smart Duplicate endpoint removal based on page title and content length to cleanup the reconnaissance data
* Identify Interesting Subdomains
* Custom GF patterns and custom Nuclei Templates
* Edit tool-related configuration files (Nuclei, Subfinder, Naabu, amass)
* Add external tools from Github/Go
* Interoperable with other tools, Import/Export Subdomains/Endpoints
* Import Targets via IP and/or CIDRs
* Report Generation
* Toolbox: Comes bundled with most commonly used tools during penetration testing such as whois lookup, CMS detector, CVE lookup, etc.
* Identification of related domains and related TLDs for targets
* Find actionable insights such as Most Common Vulnerability, Most Common CVE ID, Most Vulnerable Target/Subdomain, etc.

!!! tip
    Follow [me on Twitter](//twitter.com/ojhayogesh11) to keep yourself updated about new features.

## 🚀 Getting Started

* If this is your first time visiting reNgine, here is a guide on [🚀 Getting Started ](getting-started.md).

* If are already using reNgine and wish to Update/Upgrade, head to [🔥 Update ](update/index.md).

## ⚡ Usage Guide

If have already installed reNgine, and want to learn how to use, head to [⚡ Usage](usage/index.md).

## 💻 Developer's Guide

If you wish to add new features or want to contribute to reNgine, head to [Developer's Guide](developer/index.html)

## 🙋 Need Help

If [⚡ Usage](usage/index.md) documentation is not sufficient, and you still need help, head to [💁 Discord](community/discord.md) section. This section contains instructions on how to join reNgine discord server.

## 📹 Community published blogs/videos

Community may have published blogs/videos on your own language. Please check the [community published blogs/videos here](community/blog-videos.md).

## 🛡️ Reporting Security Issues

If you have found any security issues on reNgine, we recommend reporting them immediately. reNgine also has it's bug bounty program and is your chance to get paid for security issues.

!!! danger
    Please do not disclose any security vulnerabilities on Github issues.

Guide on [How to report security issues](security/index.md) is available.

## 🤖 Changelogs

If you want to know the latest changes in reNgine, head to [🤖 Changelog](changelog.md).

## Support

Over the last few years I have been working insane on reNgine to bring new features with the only goal to make this as De-facto standard for reconnaissance. Most of my out of office hours and weeknds are spent on working on reNgine. I do this with addition to my primary job. I am happy to have received such an overwhelming support from community. But to keep this project alive, I am seeking financial support.

|                                                                       Paypal                                                                       |                                                            Bitcoin                                                             |                                                            Ethereum                                                            |
| :-------------------------------------------------------------------------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------------------------------------------------: |
|[https://www.paypal.com/paypalme/yogeshojha11](https://www.paypal.com/paypalme/yogeshojha11)                                 |                                              `35AiKyNswNZ4TZUSdriHopSCjNMPi63BCX`                                              |                                          `0xe7A337Da6ff98A28513C26A7Fec8C9b42A63d346`                                          |

It takes a considerable amount of time to add new features and make sure everything is working. A donation is your way saying: **reNgine is awesome**

Any support is greatly appreciated! _Thank you!_

## License

reNgine is licensed under the GNU General Public License v3.0
