# YAML Configuration for Scan Engine

## How to write your reNgine Scan Engine YAML Configuration?
![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

reNgine provides the ability to customize scan engines via YAML based configuration. This configuration can be used to select the tools, choose the options provided by the tools etc.

!!! danger "Attention"
    reNgine 2.0 has new scan engine configuration. Configurations from reNgine < 2.0.0 will not work in >= 2.0.0


!!! danger "Attention"
    reNgine 2.0 does not provide switches to enable or disable tasks. The YAML configuration decides which tasks to use. Any `task: {}` that is in YAML config will run, rest will not.

Currently YAML config is supported for

!!! example "YAML Support for"
    * Subdomain Discovery as `subdomain_discovery`
    * HTTP Crawling as `http_crawl`
    * Screenshot Gathering as `screenshot`
    * OSINT as `osint`
    * Port Scan as `port_scan`
    * Directory and File Fuzzing as `dir_file_fuzz`
    * Endpoint Gathering as `fetch_url`
    * Vulnerability Scan as `vulnerability_scan`
    * Global Variable custom_headers as `custom_headers`

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)
## Default YAML Config

``` yaml
# Global vars for all tools
#
# custom_headers: ['Foo: bar', 'User-Agent: Anything']     # FFUF, Nuclei, Dalfox, CRL Fuzz, HTTP Crawl, Fetch URL, etc
# enable_http_crawl: true           # All tools
# threads: 30                       # All tools

subdomain_discovery: {
  'uses_tools': ['subfinder', 'ctfr', 'sublist3r', 'tlsx', 'oneforall', 'netlas'],  # amass-passive, amass-active, All
  'enable_http_crawl': true,
  'threads': 30,
  'timeout': 5,
  # 'use_subfinder_config': false,
  # 'use_amass_config': false,
  # 'amass_wordlist': 'deepmagic.com-prefixes-top50000'
}
http_crawl: {
  # 'threads': 30,
  # 'follow_redirect': true
}
port_scan: {
  'enable_http_crawl': true,
  'timeout': 5,
  # 'exclude_ports': [],
  # 'exclude_subdomains': [],
  'ports': ['top-100'],
  'rate_limit': 150,
  'threads': 30,
  'passive': false,
  # 'use_naabu_config': false,
  # 'enable_nmap': true,
  # 'nmap_cmd': '',
  # 'nmap_script': '',
  # 'nmap_script_args': ''
}
osint: {
  'discover': [
      'emails',
      'metainfo',
      'employees'
    ],
  'dorks': [
    'login_pages',
    'admin_panels',
    'dashboard_pages',
    'stackoverflow',
    'social_media',
    'project_management',
    'code_sharing',
    'config_files',
    'jenkins',
    'wordpress_files',
    'php_error',
    'exposed_documents',
    'db_files',
    'git_exposed'
  ],
  # 'custom_dorks': [],
  'intensity': 'normal',
  'documents_limit': 50
}
dir_file_fuzz: {
  'auto_calibration': true,
  'enable_http_crawl': true,
  'rate_limit': 150,
  'extensions': ['html', 'php','git','yaml','conf','cnf','config','gz','env','log','db','mysql','bak','asp','aspx','txt','conf','sql','json','yml','pdf'],
  'follow_redirect': false,
  'max_time': 0,
  'match_http_status': [200, 204],
  'recursive_level': 2,
  'stop_on_error': false,
  'timeout': 5,
  'threads': 30,
  'wordlist_name': 'dicc'
}
fetch_url: {
  'uses_tools': ['gospider', 'hakrawler', 'waybackurls', 'katana', 'gau'],
  'remove_duplicate_endpoints': true,
  'duplicate_fields': ['content_length', 'page_title'],
  'enable_http_crawl': true,
  'gf_patterns': ['debug_logic', 'idor', 'interestingEXT', 'interestingparams', 'interestingsubs', 'lfi', 'rce', 'redirect', 'sqli', 'ssrf', 'ssti', 'xss'],
  'ignore_file_extensions': ['png', 'jpg', 'jpeg', 'gif', 'mp4', 'mpeg', 'mp3'],
  'threads': 30,
  # 'exclude_subdomains': false
}
vulnerability_scan: {
  'run_nuclei': true,
  'run_dalfox': false,
  'run_crlfuzz': false,
  'run_s3scanner': false,
  'enable_http_crawl': true,
  'concurrency': 50,
  'intensity': 'normal',
  'rate_limit': 150,
  'retries': 1,
  'timeout': 5,
  'fetch_gpt_report': true,
  'nuclei': {
    'use_nuclei_config': false,
    'severities': ['unknown', 'info', 'low', 'medium', 'high', 'critical'],
    # 'tags': [],                 # Nuclei tags (https://github.com/projectdiscovery/nuclei-templates)
    # 'templates': [],            # Nuclei templates (https://github.com/projectdiscovery/nuclei-templates)
    # 'custom_templates': []      # Nuclei custom templates uploaded in reNgine
  }
}
waf_detection: {
  'enable_http_crawl': true
}
screenshot: {
  'enable_http_crawl': true,
  'intensity': 'normal',
  'timeout': 10,
  'threads': 40
}
```

!!! info
    While the above YAML config is **good enough** to run the scan against the targets, modifying the configurations may give better scan results.

!!! danger ""
    Before you make any modifications to the YAML Configuration, please note that, wrong configuration may crash the scans. It is adviced that you [learn about YAML](https://rollout.io/blog/yaml-tutorial-everything-you-need-get-started/) before you make any modifications.

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

## Detailed guide on configuring Scan Engines

This document will discuss about the available options, possibilities and different configurations required for reNgine Scan Engine YAML configuration.


![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

### subdomain_discovery

- `uses_tools`: *(list)* A list of subdomain discovery tools to use, such as 'subfinder', 'ctfr', 'sublist3r', etc. Available tools for subdomain_discovery are:
    - `all` (will use all default and custom subdomain enum tools)
    - `subfinder`
    - `ctfr`
    - `sublist3r`
    - `tlsx`
    - `oneforall`
    - `netlas`
    - `amass-passive`
    - `amass-active`
    - *custom_tool: You can also install custom subdomain enum tool and use it here.*

You can use one or more combination of these tools to improve the results.

- `threads`: *(int)* The number of threads or concurrent processes to use for subdomain discovery.
- `timeout`: *(int)* The maximum time, in seconds, to wait for subdomain discovery to complete.
- `use_amass_config`: *(boolean)* If set to true, reNgine will use configuration file for amass. [Find more about configuration files here.](/usage/tool_conf)
- `use_subfinder_config`: *(boolean)* If set to true, reNgine will use configuration file for subfinder. [Find more about configuration files here.](/usage/tool_conf)
- `amass_wordlist`: *(str)* Optional, Wordlist for `amass-active` which performs brute-force of subdomains using a the wordlists. Available Options for `amass_wordlist` are:
    * `default`
    * `short_name_for_wordlist`

Please follow the guide on [uploading your own wordlist](/usage/wordlist). You need to enter the wordlist short_name here.

!!! info "Default Wordlist"
    If `default` wordlist is choosed then [Deepmagic top 50,000 prefix wordlist](https://github.com/danielmiessler/SecLists/blob/master/Discovery/DNS/deepmagic.com-prefixes-top50000.txt) will be used.

!!! danger ""
    reNgine currently does not support multiple wordlists. This feature maybe available in future updates.

#### Using Custom Subdomain Enum Tool

!!! tip "TIP on using custom tools!"
    reNgine supports custom tools. Instruction on installing custom tool can be [found here](/usage/external-tool). You can use the name of the tool that was entered earlier.

    If your subdomain gathering tool was names as Turbo, you can use as

    `uses_tools: ['subfinder', 'turbo']`

## http_crawl
This option can be used to do http probing. Not using http_crawl will be a passive scan.

## port_scan
Port scan is currently being performed using [naabu](https://github.com/projectdiscovery/naabu), please refer [naabu documentation](https://github.com/projectdiscovery/naabu/blob/master/README.md) as well.

- `enable_http_crawl`: *(boolean)* A boolean indicating whether to enable HTTP crawling after port scanning.
- `timeout`: *(int)* The maximum time, in seconds, to wait for port scanning to complete.
- `ports`: *(list)* A list of ports to scan, such as 'top-100'. Available options are:
    - `top-100`
    - `top-1000`
    - `full` (will scan all 65k ports)
    - list of port numbers like `[80, 443, 8080]`
- `rate_limit`: *(int)* The rate limit for port scanning.
- `threads`: *(int)* The number of threads or concurrent processes to use for port scanning.
- `passive`: *(boolean)* A boolean indicating whether to use passive naabu port scan.
- `exclude_ports`: *(list)* Ports which you would like to exclude from the scan for example: `[8081, 443]`
- `exclude_subdomains`: *(boolean)* If set to true, port scanning will not be done on subdomains that are chosen to be ignored while starting scan.
- `use_naabu_config`: *(boolean)* If set to true, reNgine will use configuration file for naabu. [Find more about configuration files here.](/usage/tool_conf)
- `enable_nmap`: *(boolean)* If set to true, nmap will be used for scanning vulnerabilities on discovered ports.
- `nmap_cmd`: *(str)* Custom Nmap Command
- `nmap_script`: *(str)* Nmap Script to use: this will be passed in to nmap's `--script` option.
- `nmap_script_args`: *(str)* Nmap Script Args to use: this will be passed in to nmap's `--script-args` option.

## osint
Currently supported options for osint are:

- `discover` *(list)*: A list of items to discover, for example `['emails', 'metainfo']`, available options are:
    - `emails`
    - `metainfo`
    - `employees`
- `intensity` *(int)*: The intensity of the OSINT scan, e.g., `normal` or `deep`.
- `documents_limit` *(int)*: The maximum number of documents to retrieve.
- `dorks` *(list)*: A list of dork types to search for. Available options are:
    - `login_pages`
    - `admin_panels`
    - `dashboard_pages`
    - `stackoverflow`
    - `social_media`
    - `project_management`
    - `code_sharing`
    - `config_files`
    - `jenkins`
    - `wordpress_files`
    - `php_error`
    - `exposed_documents`
    - `db_files`
    - `git_exposed`
- `custom_dorks` *(list)*: Custom dorks will be a list of dictionaries, for example:
    - `[{'lookup_site': 'google.com', 'lookup_keywords': '/home/'}]`
    - `[{'lookup_site': '__target__', 'lookup_extensions': 'db, php, jpg'}]`

    `lookup_site` is where the information should be looked for. Example stackoverflow.com, or even the target, so the possible values for `lookup_site` could be any website or the target itself. Suppose, if you want to look for all db files in the target itself, `lookup_site` will be `__target__`. reNgine will automatically replace this with actual target. Do not put the target name here, rather `__target__`.

    `lookup_keywords` or `lookup_extensions`

    `lookup_keywords` or `lookup_extensions` can not be used together, you can either search for specific path file in google or certain files that are indexed, so they can not be used together. You will need to use either `lookup_keywords` or `lookup_extensions`.

    `lookup_keywords` could be certain keywords, paths, separated by comma.
    `lookup_extensions` could be file extensions separated by comma.

## dir_file_fuzz

This configuration will be used in Directory and file fuzzing. Currently supported options for `dir_file_fuzz` are:

- `auto_calibration`: *(boolean)* Automatically calibrate filtering options (ffuf specific)
- `enable_http_crawl`: *(boolean)* If set to true, only alive URLs will be used for dir_file_fuzz gathering.
- `rate_limit`: *(int)* The rate limit for fuzzing.
- `extensions`: *(list)* This option will allow you to define the extensions for the file fuzzing. You can define as many file extensions as you wish. Please note that, more file extensions will take longer to complete fuzzing. For example: `['php', 'git', 'xml']`
- `follow_redirect`: *(boolean)* Follow redirects (ffuf specific)
- `max_time`: *(int)* If you don't want ffuf to run indefinitely, you can use the max_time. This stops the entire process after a given time (in seconds).
- `match_http_status`: *(list)* List of HTTP status codes to consider as a match.
- `recursive_level`: *(int)* Enabling `recursive_level` option will bruteforce recursively inside all the directories. Turning on this option will increase scan time exponentially but will gather more information. Use it wisely.
- `stop_on_error`: *(boolean)* Stop on spurious errors (ffuf specific)
- `timeout`: *(int)* The maximum time, in seconds, to wait for fuzzing to complete.
- `threads`: *(int)* The number of threads or concurrent processes to use for fuzzing.
- `match_http_status`: *(list)* Match HTTP status codes, or "all" for everything. For example: `[200, 204]`
- `wordlist_name`: *(str)* This option is used to supply wordlist for files and directory fuzzing. Available Options for `wordlist_name` are:
    - `default`
    - `short_name_for_wordlist`

    Please follow the guide on [uploading your own wordlist](/usage/wordlist). You need to enter the wordlist short_name here.

    !!! info "Default Wordlist"
        If `default` wordlist is choosed then [default dicc.txt](https://github.com/maurosoria/dirsearch/blob/master/db/dicc.txt) will be used.

    !!! danger ""
        reNgine currently does not support multiple wordlists. This feature maybe available in future updates.

## fetch_url

`fetch_url` uses tools like `gau` and `hakrawler` to gather the endpoints. Currently supported options for `fetch_url` are:

- `uses_tools`: *(list)* A list of tools to use for URL fetching. Available tools are:
    - `gospider`
    - `hakrawler`
    - `waybackurls`
    - `gospider`
    - `katana`

    It can be used as `'uses_tools': ['gospider', 'hakrawler', 'waybackurls', 'gospider']`

- `remove_duplicate_endpoints`: *(boolean)* A boolean indicating whether to remove duplicate endpoints.
- `duplicate_fields`: *(list)* Fields used to identify duplicate endpoints. Available options are:
      - `content_length`
      - `page_title`
      - `http_status`
      - `content_type`
      - `webserver`

      Use these available options as combination to identify duplicate endpoints, for example `['content_length', 'page_title']`

- `enable_http_crawl`: *(boolean)* If set to true, only alive URLs will be used for fetch_url gathering.
- `gf_patterns`: *(list)* List of patterns to search for using Gf. Available patterns are:
      - `debug_logic`
      - `idor`
      - `interestingEXT`
      - `interestingparams`
      - `interestingsubs`
      - `lfi`
      - `rce`
      - `redirect`
      - `sqli`
      - `ssrf`
      - `ssti`
      - `xss`

    Use the combination of GF patterns as: `['xss', 'lfi', 'rce']`

    !!! tip "Custom GF Pattern"
         You can also upload custom gf patterns, and use filename here, without extension.

- `ignore_file_extensions`: *(list)* This option will allow you to ignore certain file extensions while gathering URLs. You can use one or more combination of extensions to exclude. For example `['png', 'jpg', 'jpeg', 'gif', 'mp4', 'mpeg', 'mp3']`
- `exclude_subdomains`: *(boolean)* If set to true, URLs will not be fetched for subdomains that are chosen to be ignored while initiating scan.


## vulnerability_scan

- `run_nuclei`: *(boolean)* If set to true, nuclei will be used for vulnerability scan.
- `run_dalfox`: *(boolean)* If set to true, dalfox will be used for XSS scans.
- `run_crlfuzz`: *(boolean)* If set to true, CRLFuzz will be used for CRLF vulnerability detection.
- `run_s3scanner`: *(boolean)* If set to true, misconfigured s3 buckets will be used during vulnerability scan.
- `concurrency`: *(int)* This option will specify the number of threads/go routines to perform vulnerability scan.
- `rate_limit`: *(int)* Maximum number of requests to send per second
- `retries`: *(int)* Number of times to retry a failed request
- `timeout`: *(int)* Time to wait in seconds before timeout
- `fetch_gpt_report`: *(boolean)* If set to true, GPT will be used to fetch vulnerability details such as impact and remediation. **OpenAiAPIKey is required.**

    - `nuclei`: Nuclei specific configurations
        - `use_conf`: *(boolean)* If set to true, reNgine will use configuration file for nuclei. [Find more about configuration files here.](/usage/tool_conf)
        - `severities`: *(list)* You can run the templates based on the specific severity of the template, single or multiple severity can be used for scan. Available options are:
            - `all`
            - `critical`
            - `high`
            - `medium`
            - `low`
            - `info`
            - `unknown`
        - `tags`: *(list)* List of nuclei tags, refer to Nuclei's documentation.
        - `templates`: *(list)* Please refer to [nuclei's documentation](https://github.com/projectdiscovery/nuclei) to check which templates are supported. Nuclei may release any new templates which may not be possible to update here in the documentation, so it is adviced that you refer to [Nuclei's documentation](https://github.com/projectdiscovery/nuclei). For example `['files', 'cve']`
        - `custom_templates`: *(list)*
            !!! tip "Custom Nuclei Templates"
                 You can also upload custom Nuclei Templates from Tool Settings, and use filename here, without extension.

    - `s3scanner`: s3scanner specific configurations
        - `threads`: *(int)* s3scanner number of threads
        - `providers`: *(list)* List of providers to look for misconfigured s3 buckets. Availble options are:
            - `aws`
            - `gcp`
            - `digitalocean`
            - `dreamhost`
            - `linode`

            For example: `['aws', 'gcp']`

## waf_detection

Use this to detect the WAF in subdomains, wafw00f will be used to identify WAF.

## screenshot

Screenshot gathering

- `enable_http_crawl`: *(boolean)* If set to true, only alive URLs will be used for screenshot gathering.
- `timeout`: *(int)* Timeout in seconds for screenshot gathering
- `threads`: *(int)* Numbers of threads to use for EyeWitness


## Shared Scan Configuration

Some of the scan configurations such as threads or custom_header could be used across all the tasks. Instead of using them in individual task, you can also use them as shared configuration, outside the task object configuration.

  - enable_http_crawl
  - timeout
  - rate_limit
  - retries
  - custom_headers

Example:

```yaml
subdomain_discovery: {}
http_crawl: {}
port_scan: {}
osint: {}
dir_file_fuzz: {}
fetch_url: {}
vulnerability_scan: {}
waf_detection: {}
screenshot: {}

# shared scan config
enable_http_crawl: true
timeout: 10
rate_limit: 5
retries: 2
custom_headers: ["Foo: bar"]
```

These shared scan config will be used across all the tasks.

## Passing cookies for authenticated scans

reNgine can perform authenticated scans, in order to do so, you must pass the authenticated cookies using global variable called `custom_headers`

For example the target website supports cookie based authentication, you will need to pass cookies as below in YAML configuration

```yaml
custom_headers: ['Cookies: foo=bar;bar=foo;another=cookie']
```

You can pass in multiple cookies and also multiple headers if required.

For websites that uses Basic Headers for authentication, you can use

```yaml
custom_headers: ['Authorization: Basic yourtoken']
```