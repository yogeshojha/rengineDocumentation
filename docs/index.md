# Introduction

## reNgine: An automated reconnaissance framework


reNgine is An automated reconnaissance framework for web applications with focus on highly configurable streamlined recon process via Engines, recon data correlation and organization, continuous monitoring, backed by database and simple yet intuitive User Interface.

reNgine makes is easy for penetration testers to gather reconnaissance with minimal configuration and with the help of reNgine's correlation, it just makes recon effortless.

![reNgine Logo](static/banner.gif)

## Description

reNgine is an automated reconnaissance framework with a focus on a highly configurable streamlined recon process. reNgine is backed by a database, with data correlation and organization, the custom query “like” language for recon data filtering, reNgine aims to address the shortcomings of traditional recon workflow. Developers behind the reNgine understand that recon data can be huge, manually looking up for entries to attack could be cumbersome, with features like Auto Interesting Subdomains discovery, reNgine automatically identifies interesting subdomains to attack based on certain keywords (both built-in and custom) and helps penetration testers focus on attack rather than recon.

reNgine is also focused on continuous monitoring. Penetration testers can choose to schedule the scan at periodic intervals, get notified on notification channels like Discord, Slack, and Telegram for any new subdomains or vulnerabilities identified, or any recon data changes.

Interoperability is something every recon tool needs, and reNgine is no different. Beginning reNgine 1.0, we additionally developed features such as import and export subdomains, endpoints, GF pattern matched endpoints, etc. This will allow you to use your favourite recon workflow in conjunction with reNgine.

reNgine features Highly configurable scan engines based on YAML, that allows penetration testers to create as many recon engines as they want of their choice, configure as they wish, and use it against any targets for the scan. These engines allow penetration testers to use tools of their choice, the configuration of their choice. Out of the box, reNgine comes with several scan engines like Full Scan, Passive Scan, Screenshot gathering, OSINT Engine, etc.

Our focus has always been on finding the right recon data with very minimal effort. While having a discussion with fellow hackers/pentesters, screenshots gallery was a must, reNgine 1.0 also comes with a screenshot gallery, and what's exciting than having a screenshot gallery with filters, filter screenshots with HTTP status, technology, ports, and services.

We also want our fellow hackers to stay ahead of the game, reNgine 1.0 introduces automatic vulnerability reporting (currently only Hackerone is supported, other platforms *may* come soon). This allows hackers to define their own vulnerability report template and reNgine will do the rest of the job to report vulnerability as soon as it is identified.


## Highlights

- Perform Recon: Subdomain Discovery, Ports Discovery, Endpoints Discovery, Directory Bruteforce, Screenshot gathering
- IP Discovery, CNAME discovery, Vulnerability scan using Nuclei
- Ability to Automatically report Vulnerabilities to Hackerone
- Support for Parallel Scans
- Recon Data visualization
- Highly configurable scan engines
- OSINT Capabilities (Metainfo Gathering, Employees Gathering, Email Address with option to look password in leaked database, dorks etc)
- Customizable Alerts/Notification on Slack, Discord and Telegram
- Perform Advanced Query lookup using natural language alike and, or, not operations
- Support for Recon Notes and Todos
- Support for Clocked Scans (Run reconnaissance exactly at X Hours and Y minutes) and Periodic Scans (Runs reconnaissance every X minutes/hours/days/week)
- Proxy Support
- Screenshot Gallery with Filters
- Powerful recon data filtering with auto suggestions
- Recon Data changes, finds new/removed subdomains/endpoints
- Support for tagging targets into Organization
- Ability to identify Interesting Subdomains
- Support for custom GF patterns and custom Nuclei Templates
- Support for editing tool related configuration files (Nuclei, Subfinder, Naabu, amass)
- Ability to Mark Important Subdomains
- Interoperable with other tools, Import/Export Subdomains/Endpoints
- Option to send scan data directly to discord


## 🚀 Getting Started

* If this is your first time using reNgine, head to [🚀 Install reNgine](install/index.md) to install reNgine.

* If are already using reNgine and wish to Update/Upgrade, head to [🔥 Update reNgine](update/index.md) to update reNgine.

## ⚡ Usage Guide

If have already installed reNgine, and want to learn how to use reNgine, head to [⚡ Usage](usage/index.md).

## 🙋 Need Help

If [⚡ Usage](usage/index.md) documentation is not sufficient, and you still need help, head to [💁 Discord](community/discord.md) section. This section contains instructions on how to use reNgine discord server.

## 🛡️ Reporting Security Issues

If you have found any security issues with reNgine, we recommend reporting them immediately.reNgine also has it's bug bounty program!

!!! danger
    Please do not disclose any security vulnerabilities on Github issues.

Guide on [How to report security issues](security/index.md) is available.

## 🤖 Changelogs

If you want to know the latest changes in reNgine, head to [🤖 Changelog](changelog/index.md) to know the latest changes in reNgine.

## Help to keep this project alive

PayPal: [https://www.paypal.com/paypalme/yogeshojha11](https://www.paypal.com/paypalme/yogeshojha11)
