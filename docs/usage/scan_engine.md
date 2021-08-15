# YAML Configuration for Scan Engine

## How to write your reNgine Scan Engine YAML Configuration?
![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

reNgine provides the ability to customize scan engines via YAML based configuration. This configuration can be used to select the tools, choose the options provided by the tools etc.

Currently YAML config is supported for

!!! example "YAML Support for"
    * Subdomain Discovery as `subdomain_discovery`
    * Visual Identification as `visual_identification`
    * OSINT as `osint`
    * Port Scan as `port_scan`
    * Directory and File Search as `dir_file_search`
    * Endpoint Gathering as `fetch_url`
    * Vulnerability Scan as `vulnerability_scan`

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)
## Default YAML Config

``` yaml
subdomain_discovery:
  uses_tools: [ amass-passive, assetfinder, sublist3r, subfinder, oneforall ]
  threads: 10
  use_amass_config: false
  use_subfinder_config: false

visual_identification:
  timeout: 10
  threads: 5

osint:
  discover: [ emails, metainfo, employees ]
  intensity: normal
  # intensity: deep
  dork: [ stackoverflow, 3rdparty, social_media, project_management, code_sharing, config_files, jenkins, wordpress_files, cloud_buckets, php_error, exposed_documents, struts_rce, db_files, traefik, git_exposed ]

port_scan:
  ports: [ top-1000 ]
  rate: 1000
  use_naabu_config: false
  # exclude_ports: [80, 8080]

dir_file_search:
  extensions: [ php, git, yaml, conf, db, mysql, bak, asp, aspx, txt, conf, sql, json ]
  threads: 100
  recursive: false
  recursive_level: 1
  wordlist: default
  exclude_extensions: [jpg, png, jpeg, gif, tiff]

fetch_url:
  uses_tools: [ gauplus, hakrawler, waybackurls, gospider ]
  intensity: normal
  # intensity: deep
  ignore_file_extension: [jpg, png, jpeg, gif]
  gf_patterns: [ debug_logic, idor, img-traversal, interestingEXT, interestingparams, interestingsubs, jsvar, lfi, rce, redirect, sqli, ssrf, ssti, xss]

vulnerability_scan:
  concurrency: 10
  rate_limit: 150
  timeout: 5
  retries: 1
  templates: [ all ]
  # custom_templates: []
  severity: [ critical, high, medium, low, info ]
```

!!! info
    While the above YAML config is **good enough** to run the scan against the targets, modifying the configurations can give better results.

!!! danger ""
    Before you make any modifications to the YAML Configuration, please note that, wrong configuration may crash the scans. It is adviced that you [learn about YAML](https://rollout.io/blog/yaml-tutorial-everything-you-need-get-started/) before you make any modifications.

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

## Detailed guide on configuring Scan Engines

This document will discuss about the available options, possibilities and different configurations required for reNgine Scan Engine YAML configuration.



![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)
### subdomain_discovery


`subdomain_discovery` currently supports five different options

!!! example "Available option for subdomain_discovery"
    * **uses_tools** **(required)**
    * threads (optional)
    * amass_wordlist (optional)
    * use_amass_config (optional)
    * use_subfinder_config (optional)


* **uses_tools (required)**

This option allows you to choose the tools required to gather the subdomains. You can use one or more combination of these tools to improve the results.

* Available options for `uses_tools` are:
    * all
    * amass-passive
    * amass-active
    * subfinder
    * sublist3r
    * assetfinder
    * oneforall

You can have one or more combination of these tools to improve the results.

!!! check "Supported"
    ``` yaml
    subdomain_discovery:
      uses_tools: [all]
    ```

!!! check "Supported"
    ``` yaml
    subdomain_discovery:
      uses_tools: [amass-active, amass-passive, subfinder]
    ```

!!! danger "Not Supported"
    ``` yaml
    subdomain_discovery:
      uses_tools: [amass-active amass-passive subfinder]
    # Unsupported because comma is missing
    ```

!!! danger "Not Supported"
    ``` yaml
    subdomain_discovery:
    uses_tools: [all]
    # Unsupported because uses_tools is a property inside subdomain_discovery and must be indented
    ```

* **threads (optional)**

Number of threads to perform the subdomain discovery. **By default the value for threads is 10.**

* **amass_wordlist (optional)**

Wordlist for `amass-active` which performs brute-force of subdomains using a the wordlists.

* Available Options for `wordlist` are:
    * default
    * short_name_for_wordlist

Please follow the guide on [uploading your own wordlist](/usage/wordlist). You need to enter the wordlist short_name here.

!!! info "Default Wordlist"
    If `default` wordlist is choosed then [Deepmagic top 50,000 prefix wordlist](https://github.com/danielmiessler/SecLists/blob/master/Discovery/DNS/deepmagic.com-prefixes-top50000.txt) will be used.

!!! check "Supported"
    ``` yaml
    subdomain_discovery:
      wordlist: default
    ```

!!! danger ""
    reNgine currently does not support multiple wordlists. This feature maybe available in future updates.

* **use_amass_config (optional)** and **use_subfinder_config (optional)**

If set to true, reNgine will use configuration files for these tools. [Find more about configuration files here.](/usage/tool_conf)

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

### visual_identification

Visual Identification will run `EyeWitness` for visual inspection.

Currently supported options for `visual_identification` are

!!! example "Supported options for visual_identification"
    * threads
    * timeout

* **threads**

Number of threads to run EyeWitness visual identification. **By default the value for thread is 10.** This is a integer value.

* **timeout**

Timeout in seconds, **default timeout value is 10.**

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

### osint

Currently supported options for osint are:

!!! example "Supported options for visual_identification"
    * discover
    * intensity
    * dork

* **discover**

reNgine can currently discover

  * emails
  * metainfo
  * employees

for any target.

* **dork**

reNgine does not support custom dork as of now, and support is provided for these dorks:

!!! example "supported options for dork"
    * stackoverflow
    * 3rdparty
    * social_media
    * project_management
    * code_sharing
    * config_files
    * jenkins
    * wordpress_files
    * cloud_buckets
    * php_error
    * exposed_documents
    * struts_rce
    * db_files
    * traefik
    * git_exposed


* **intensity**

!!! example "supported options for intensity"
    * deep
    * normal

 **If intensity is set to deep, reNgine will perform dorking for all the subdomains.**

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

### port_scan

Port scan is currently being performed using [naabu](https://github.com/projectdiscovery/naabu), please refer [naabu documentation](https://github.com/projectdiscovery/naabu/blob/master/README.md) as well.

`port_scan` currently supports three options

!!! example "Supported option for port_scan"
    * **ports** **(required)**
    * rate (optional)
    * use_naabu_config (Optional)
    * exclude_ports (optional)

* **ports (required)**

Ports to Scan

* Available options for `ports` are
    * top-100
    * top-1000
    * full (will scan all 65k ports)
    * custom like [80, 443]

!!! check "Supported"
    ``` yaml
    port_scan:
      ports: [80, 443, 8000, 8080]
    ```

!!! check "Supported"
    ``` yaml
    port_scan:
      ports: [top-1000, 9000, 1234]
    ```

!!! check "Supported"
    ``` yaml
    port_scan:
      ports: [full]
    ```

* **rate (optional)**

Rate of port scan probe requests, **default is 1000**

* **exclude_ports (optional)**

Ports which you would like to exclude from the scan.

!!! check "Supported"
    ``` yaml
    port_scan:
      exclude_ports: [80,443]
    ```

* **use_naabu_config (optional)**

If set to true, reNgine will use configuration files for Naabu. [Find more about configuration files here.](/usage/tool_conf)

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

### dir_file_search

This configuration will be used in Directory and file search. Currently supported options for `dir_file_search` are

!!! example "Supported options for dir_file_search"
    * **extensions (required)**
    * **recursive (required)**
    * **recursive_level (required)**
    * threads (optional)
    * exclude_extensions (optional)
    * exclude_texts (optional)
    * wordlist (required)

* **extensions (required)**

This option will allow you to define the extensions for the file search. You can define as many file extensions as you wish. Please note that, more file extensions will take longer to complete the scan.

!!! check "Supported"
    ``` yaml
    dir_file_search:
      extensions: [php, git, xml]
    ```

!!! error "Unsupported"
    ``` yaml
    dir_file_search:
      extensions: [.php, .git, .xml]
    ```

* **recursive (required)**

Enabling `recursive` option will bruteforce recursively inside all the directories. Turning on the bruteforce option will increase directories scan time exponentially but will gather more information.

**Default value for `recursive` is `false`**

**recursive_level (required)**

`recursive_level` is the Max recursion depth into subdirectories.

!!! warning ""
    If `recursive_level` is set to 0, then it is infinity. Meaning it wil perform file search and direcory scan inside all the found subdirectories.

!!! info ""
    Setting up a very high number for `recursive_level` will also increase the scan time.

* **threads (optional)**

Number of threads to run directory and file search. **By default the value for threads is 100**

* **exclude_extensions (optional)**

This is to exclude any extensions that you do not want during directories bruteforce. Default values are [jpg, png, jpeg, gif, tiff]

!!! check "Supported"
    ``` yaml
    dir_file_search:
      exclude_extensions: [jpg, png, jpeg, gif, tiff]
    ```

* **exclude_texts (optional)**

If there are certain texts like Error, 404, that you wish to skip during directory bruteforce, they can be placed here. Default values are [404, Not Found, Error ]

!!! check "Supported"
    ``` yaml
    dir_file_search:
      exclude_texts: [Error, 404, Not Found]
    ```

* **wordlist (required)**

This option is used to supply wordlist to `dirsearch` for files and directory scan.

* Available Options for `wordlist` are:
    * default
    * short_name_for_wordlist

Please follow the guide on [uploading your own wordlist](/usage/wordlist). You need to enter the wordlist short_name here.

!!! info "Default Wordlist"
    If `default` wordlist is choosed then [default dicc.txt](https://github.com/maurosoria/dirsearch/blob/master/db/dicc.txt) will be used.

!!! check "Supported"
    ``` yaml
    dir_file_search:
      wordlist: default
    ```

!!! danger "Unsupported"
    ``` yaml
    dir_file_search:
      wordlist: [default, short_name]
    ```

!!! danger ""
    reNgine currently does not support multiple wordlists. This feature maybe available in future updates.

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

### fetch_url

`fetch_url` uses tools like `gau` and `hakrawler` to gather the endpoints. Currently supported options for `fetch_url` are:

!!! check "Supported Options for fetch_url"
    * uses_tools **(required)**
    * intensity **(required)**
    * ignore_file_extension **(optional)**
    * gf_patterns **(optional)**

* **uses_tools**

This option allows you to choose the tools required to gather the endpoints. You can use one or more combination of these tools to improve the results.

* Available options for `uses_tools` are:
    * gauplus
    * hakrawler
    * waybackurls
    * gospider

You can have one or more combination of these tools to improve the results.

!!! check "Supported"
    ``` yaml
    fetch_url:
      uses_tools: [all]
    ```

!!! check "Supported"
    ``` yaml
    fetch_url:
      uses_tools: [gauplus, hakrawler]
    ```

* **intensity**

This option will allow you to set the intensity for gathering URLs. Available options are

!!! example "Available options for intensity"
    * **normal** (default): This will only fetch the URLs for main domain. Suppose if your targets is example.com, the URLs associated with example.com are only fetched. `normal` intensity takes shorter time.
    * **deep**: This will fetch URLs for main domain as well as all the subdomains. This is likely to take very long time and will gather more endpoints compared to `normal` intensity.

* **ignore_file_extension**

This option will allow you to ignore certain file extensions while gathering URLs. You can use one or more combination of extensions to exclude.

!!! check "Supported"
    ``` yaml
    fetch_url:
      ignore_file_extension: [jpg, png, jpeg, gif]
    ```

* **gf_patterns**

You can now use gf patterns on the gathered URLs. Supported options are combination of these patterns.

!!! example "gf_patterns available options"
    * debug_logic
    * idor
    * img-traversal
    * interestingEXT
    * interestingparams
    * interestingsubs
    * jsvar
    * lfi
    * rce
    * redirect
    * sqli
    * ssrf
    * ssti
    * xss

!!! tip "Custom GF Pattern"
     You can also upload custom gf patterns, and use filename here, without extension.

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

### vulnerability_scan

`vulnerability_scan` uses [nuclei](https://github.com/projectdiscovery/nuclei) to perform the vulnerability scan. Please refer to [nuclei documentation](https://github.com/projectdiscovery/nuclei) as well.

Available options for `vulnerability_scan` are

!!! example "vulnerability_scan options"
    * concurrency (optional)
    * rate_limit (optional)
    * timeout (optional)
    * retries (optional)
    * custom_templates (optional)
    * **template (required)**
    * **severity (required)**

* **concurrency (optional)**

This option will specify the number of threads/go routines to perform vulnerability scan. **Default value is 10**

* **rate_limit (optional)**

Maximum number of requests to send per second **(default 150)**

* **timeout (optional)**

Time to wait in seconds before timeout **(default 5)**

* **retries (optional)**

Number of times to retry a failed request **(default 1)**

* **template (required)**

Please refer to [nuclei's documentation](https://github.com/projectdiscovery/nuclei) to check which templates are supported. Nuclei may release any new templates which may not be possible to update here in the documentation, so it is adviced that you refer to [Nuclei's documentation]((https://github.com/projectdiscovery/nuclei).

Some of the supported options for template are:

!!! check "Supported"
    ``` yaml
    vulnerability_scan:
      templates: [all]
    ```

!!! info ""
    We recommend using `all` options in `templates` for a detailed scan.

!!! check "Supported"
    ``` yaml
    vulnerability_scan:
      templates: [files, cves]
    ```

!!! check "Supported"
    ``` yaml
    vulnerability_scan:
      templates: [files/git-core.yaml, cves/CVE-2020-1234]
    ```

* **severity (required)**

You can run the templates based on the specific severity of the template, single and multiple severity can be used for scan.

Available options for `severity` are

!!! example "Available options for severity"
    * all
    * critical
    * high
    * medium
    * low
    * info

This will only run the specific templates related to the severity. You can provide multiple options for severity as well.

!!! check "Supported"
    ``` yaml
    vulnerability_scan:
      severity: [all]
    ```

Above will run all the templates.

!!! check "Supported"
    ``` yaml
    vulnerability_scan:
      severity: [low, info]
    ```

This will only run the templates based on low and informational severity.

* **Recommended**

!!! check "Recommended"
    ``` yaml
    vulnerability_scan:
      severity: [critical, high, medium, low]
    ```

This will exclude informational vulnerabilities from your scan results.


* **custom_templates**

!!! check "Recommended"
    ``` yaml
    vulnerability_scan:
      custom_templates: [my_templaete]
    ```

!!! tip "Custom Nuclei Templates"
     You can also upload custom Nuclei Templates from Tool Settings, and use filename here, without extension.

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)
