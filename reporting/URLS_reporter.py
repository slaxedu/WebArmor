import requests
import yaml

def generate_html_report():
    with open('/root/WebArmor/config.yaml', 'r') as config_file:
        config = yaml.safe_load(config_file)

    urls_file_path = config['CRAWLING_URL_ENUMERATION']['OUTPUT_FOLDER_PATH']
    urls_html_temp_path = config['REPORT']['URLS_TEMP_PATH']
    network_html_report_path = config['REPORT']['NETWORK_PAGE_PATH']
    owasp_html_report_path = config['REPORT']['OWASP_PAGE_PATH']
    info_html_report_path = config['REPORT']['MAIN_PAGE_PATH']
    vulnscan_html_report_path = config['REPORT']['VULNSCAN_PAGE_PATH']
    urls_html_report_path = config['REPORT']['URLS_PAGE_PATH']
    github_token = config['REPORT']['GITHUB_GIST_TOKEN']

    with open(urls_file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    files = {
        urls_file_path.split('/')[-1]: {
            'content': text
        }
    }

    data = {
        'public': True,
        'files': files
    }

    response = requests.post('https://api.github.com/gists', json=data, headers=headers)

    if response.status_code == 201:
        gist_url = response.json()['html_url']
    else:
        print('Error:', response.text)

    with open(urls_html_temp_path, 'r') as f:
        html_template = f.read()

    html_template += f"""
<body>
  <div id="main">
    <div id="header">
      <div id="logo">
        <div id="logo_text">
          <!-- class="logo_colour", allows you to change the colour of the text -->
          <h1><a href={info_html_report_path}><b>WEB ARMOR</b></a></h1>
        </div>
      </div>
      <div id="menubar">
        <ul id="menu">
          <!-- put class="selected" in the li tag for the selected page - to highlight which page you're on -->
          <li><a href={info_html_report_path}>INFO</a></li>
          <li><a href={vulnscan_html_report_path}>VULNERABILITY SCAN</a></li>
          <li><a href={network_html_report_path}>NETWORK SCAN</a></li>
          <li><a href={owasp_html_report_path}>OWASP SCAN</a></li>
          <li class="selected"><a href={urls_html_report_path}>CRAWLED URLS</a></li>
        </ul>
      </div>
    </div>
    <div id="site_content">
      <div class="sidebar">
        <!-- insert your sidebar items here -->
      </div>
      <div id="content">
        <h1><b>CRAWLED AND ARCHIVED URLS :</b></h1>
        <input type="text" id="gistUrl" value="{gist_url}" readonly>
        <button onclick="copyToClipboard()" id="copyButton">Copy</button>
        <script>
            function copyToClipboard() {{
                var copyText = document.getElementById("gistUrl");
                copyText.select();
                document.execCommand("copy");
                alert("Copied the Gist URL: " + copyText.value);
            }}
        </script>
      </div>
    </div>
  </div>
</body>
</html>
"""

    with open(urls_html_report_path, 'w', encoding='utf-8') as html_file:
        html_file.write(html_template)
  
