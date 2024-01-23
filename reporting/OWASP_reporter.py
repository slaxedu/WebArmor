import yaml
import os

with open('/root/WebArmor/config.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)
    sqli_folder_path = config['OWASP']['SQLI_OUTPUT_PATH']
    xss_file_path = config['OWASP']['XSS_OUTPUT_PATH']
    open_redir_file_path = config['OWASP']['OP_OUTPUT_PATH']
    ssrf_xxe_file_path = config['OWASP']['XXE_SSRF_OUTPUT_PATH']
    owasp_html_temp_path = config['REPORT']['OWASP_TEMP_PATH']
    network_html_report_path = config['REPORT']['NETWORK_PAGE_PATH']
    owasp_html_report_path = config['REPORT']['OWASP_PAGE_PATH']
    info_html_report_path = config['REPORT']['MAIN_PAGE_PATH']
    vulnscan_html_report_path = config['REPORT']['VULNSCAN_PAGE_PATH']
    urls_html_report_path = config['REPORT']['URLS_PAGE_PATH']


def xss_reporter():
    global html_template
    with open(owasp_html_temp_path, 'r') as f:
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
              <li class="selected"><a href={owasp_html_report_path}>OWASP SCAN</a></li>
              <li><a href={urls_html_report_path}>CRAWLED URLS</a></li>
            </ul>
          </div>
        </div>
        <div id="site_content">
          <div class="sidebar">
          <!-- insert your sidebar items here -->
          </div>
          <div id="content">
            <h1><b>XSS Report/POCS</b></h1>
    """
    try:
        with open(xss_file_path, 'r') as input_file:
            content = [line.split() for line in input_file.readlines()]

    except (FileExistsError, FileNotFoundError):
        html_template += """
                <h2><b>No Xss Vulns were found</b></h2>
                """
        html_template += """
    <h1> </h1>
    <hr style="border: 0.5px solid #6b6b6b; width: 200%;">
    """
        return None

    if len(content) != 0:
        for con in content:
            if len(con) != 0:
                for i in con:
                    if con.index(i) % 2 == 0 and con.index(i) < len(con) - 1:
                        title = i
                        content_text = con[con.index(i) + 1]
                        html_template += f"""
                        <h4><b>{title}</b></h4>
                        <textarea class="textbox" rows="4" cols="50" readonly>{content_text}</textarea>
                        """
    else:
        html_template += """
                <h2><b>No Xss Vulns were found</b></h2>
                """

    html_template += """
    <h1> </h1>
    <hr style="border: 0.5px solid #6b6b6b; width: 200%;">
    """


def open_redir_reporter():
    global html_template
    with open(open_redir_file_path, 'r') as f:
        vuln_urls = [i.split()[1][1:-1] for i in f.readlines()]

    data = []

    def url_parser(url):
        endpoint = url[:url.index('?')]
        payload = url[url.index('=') + 1:]
        parameter = url[url.index('?'):url.index('=')]
        data.append([endpoint, payload, parameter, url])

    for url in vuln_urls:
        url_parser(url)

    html_template += '''
      <h2><b>Open-Redirect Result/POC</b></h2>
      <table>
        <tr>
          <th>Endpoint</th>
          <th>POC</th>
        </tr>
    '''

    for entry in data:
        html_template += f'''
        <tr>
          <td>{entry[0]}</td>
          <td>{entry[3]}</td>
        </tr>
        '''

    html_template += '''</table>'''
    html_template += """
    <h1> </h1>
    <hr style="border: 0.5px solid #6b6b6b; width: 200%;">
    """


def sqli_reporter():
    log_file = 'log'
    target_file = 'target.txt'
    global html_template

    items_in_base_folder = os.listdir(sqli_folder_path)

    if not items_in_base_folder:
        html_template += """<h3>No SQLi vulnerabilities were found.</h3>"""
        html_template += """
    <h1> </h1>
    <hr style="border: 0.5px solid #6b6b6b; width: 200%;">
    """
        return None

    for item in items_in_base_folder:
        item_path = os.path.join(sqli_folder_path, item)
        if os.path.isdir(item_path):
            file_path1 = os.path.join(item_path, target_file)
            file_path2 = os.path.join(item_path, log_file)

            if os.path.exists(file_path1) and os.path.exists(file_path2):
                with open(file_path1, 'r') as file:
                    target_file_cont = file.read()

                with open(file_path2, 'r') as file:
                    log_file_cont = file.readlines()

                if len(log_file_cont) < 1:
                    html_template += f"""<h3>-No SQLi vulnerabilities were found for target : [ {target_file_cont.split(' ')[0]} ]</h3>"""
                    html_template += """
    <h1> </h1>
    <hr style="border: 0.5px solid #6b6b6b; width: 200%;">
    """
                    return None

                dbs = [i.strip() for i in log_file_cont][:-1]
                databases = [[dbs[-3][:-1], dbs[-2] + ' ' + dbs[-1]]]

                log_details = [i.strip().split(':') for i in log_file_cont if len(i.strip().split(':')) == 2][1:-1] + databases
                log_title = log_file_cont[0]
                target = target_file_cont.split(' ')[0]

                html_template += f"""
                <h1><b>SQLI SCAN REPORT</b></h1>
                <label for='target' style='font-weight: bold; font-size: 16px;'>Target: </label><input type='text' id='target' name='target' value='{target}' readonly style='width: 400px; height: 20px;'>
"""
                html_template += f"""
                <h1> </h1>
                <h4><b>{log_title}</b></h4>"""
                html_template += """<table><tr><th> </th><th> </th></tr>"""

                for detail in log_details:
                    html_template += f"""<tr><td>{detail[0]}</td><td>{detail[1]}</td></tr>"""

                html_template += """</table>"""
    html_template += """
    <h1> </h1>
    <hr style="border: 0.5px solid #6b6b6b; width: 200%;">
    """


def xxeANDssrf_reporter():
    global html_template
    html_template += f"""
        <h1><b>XXE & SSRF SCAN REPORT</b></h1>
    """
    with open(ssrf_xxe_file_path, 'r') as file:
        log_data = file.read()
    entries = log_data.strip().split('\n')
    if len(entries) < 2:
        html_template += """<h3>No Vulnerabilities were found</h3>"""
    else:
        html_template += """
    <table>
        <tr>
            <th>Issue</th>
            <th>Type</th>
            <th>Severity</th>
            <th>Details</th>
        </tr>
"""

        for entry in entries:
            parts = entry.split(' ')
            issue = parts[2][1:-1]
            details = ' '.join(parts[5:])
            type_value = parts[3][1:-1] if len(parts) > 3 else ""
            severity = parts[4][1:-1] if len(parts) > 3 else ""
            html_template += f"""   <tr><td>{issue}</td><td>{type_value}</td><td>{severity}</td><td>{details}</td></tr>\n"""
        html_template += """</table>"""
    html_template += """</div>
      </div>
      <div id="content">
    </div>
    </div>
  </div>
</body>

</html>
    """


def generate_html_report():
    xss_reporter()
    open_redir_reporter()
    sqli_reporter()
    xxeANDssrf_reporter()
    with open(owasp_html_report_path, 'w') as f:
        f.write(html_template)
