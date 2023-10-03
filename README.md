# WebArmor v.1.0

## File Structure

```console
WebArmor/
│
├── asset_discovery/
│   ├── __init__.py                         # Empty package initializer
│   ├── asset_passive.py                    # Module for discovering related and owned assets by passive-only methods.
│   ├── asset_active.py                     # Module for more active reconnaissance technique.
│   └── ...                                 # Additional modules or files related to asset discovery (if needed).
│
├── vulnerability_scanning/
│   ├── __init__.py                        # Empty package initializer
│   ├── vuln_scanner.py                    # Core module responsible for implementing vulnerability scanning logic.
│   ├── yaml_templates/                    # Directory for YAML templates defining scanning techniques and payloads.
│   │   ├── xss_template.yaml              # YAML template for XSS (cross-site scripting) scanning.
│   │   ├── cve_template.yaml              # YAML template for Most Common CVEs.
│   │   └── ...                            # Additional YAML templates for other vulnerabilities.
│   └── ...
│
├── crawling_url_enumeration/
│   ├── __init__.py                        # Empty package initializer
│   ├── crawler.py                         # Module for web crawling and gathering URLs for enumeration.
│   ├── url_enumeration.py                 # Module for enumerating URLs on the target web application by (WebArchieve..).
│   └── ...                                # Additional modules or files related to URL enumeration.
│
├── network_scanning/                      # Directory for network-level scanning and open ports detection.
│   ├── __init__.py                        # Empty package initializer
│   ├── network_scanner.py                 # Module for network-level scanning.
│   └── ...                                # Additional modules or files related to network scanning.
│
├── vulnerability_scripts/                 # Directory for specific vulnerability detection scripts
│   ├── __init__.py                        # Empty package initializer
│   ├── xss_detection.py                   # Module for detecting cross-site scripting (XSS) vulnerabilities.
│   ├── sql_injection_detection.py         # Module for detecting SQL injection vulnerabilities.
│   └── ...                                 # Additional modules or files for detecting other vulnerabilities.
│
├── report_generation/                     # Directory for generating vulnerability reports
│   ├── __init__.py                        # Empty package initializer
│   ├── report_generator.py                # Module for generating detailed vulnerability reports.
│   └── ...                                # Additional modules or files related to report generation.
│
├── main.py                                 # The entry point of the application, coordinating various modules.
└── README.md                               # Comprehensive documentation for the project.

```

> The file structure is subject to change as the project evolves.
