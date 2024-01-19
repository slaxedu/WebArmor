from datetime import datetime
import yaml
import json

def generate_html_report():
    with open('/root/WebArmor/config.yaml', 'r') as config_file:
        config = yaml.safe_load(config_file)

    info_html_temp_path = config['REPORT']['INFO_TEMP_PATH']
    network_html_report_path = config['REPORT']['NETWORK_PAGE_PATH']
    owasp_html_report_path = config['REPORT']['OWASP_PAGE_PATH']
    info_html_report_path = config['REPORT']['MAIN_PAGE_PATH']
    vulnscan_html_report_path = config['REPORT']['VULNSCAN_PAGE_PATH']
    urls_html_report_path = config['REPORT']['URLS_PAGE_PATH']
    domain_info_path = config['ASSET_DISCOVERY']['DOMAIN_INFO_FILE_PATH']
    technologies_file_path = config['ASSET_DISCOVERY']['TECHNOLOGIES_FILE_PATH']
    domain = config['GLOBAL']['DOMAIN']

    with open(info_html_temp_path, 'r') as f:
        html_template = f.read()

    html_template += """
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
          <li class="selected"><a href={info_html_report_path}>INFO</a></li>
          <li><a href={vulnscan_html_report_path}>VULNERABILITY SCAN</a></li>
          <li><a href={network_html_report_path}>NETWORK SCAN</a></li>
          <li><a href={owasp_html_report_path}>OWASP SCAN</a></li>
          <li><a href={urls_html_report_path}>CRAWLED URLS</a></li>
        </ul>
      </div>
    </div>
    <div id="site_content">
      <div class="sidebar">
        <h3><b>SCAN REPORT</b></h3>
        <h5 style='font-style:normal;'>Target : {domain}</h5>
        <h5 style='font-size:60%; font-style:normal;'>Scan date : {datetime.now().strftime('%d %B %Y')}</h5>
        <h1> </h1>
        <hr style="border: 0.5px solid #6b6b6b; width: 200%;">
        """

    with open(domain_info_path, 'r') as f:
        k = [i.strip().split(': ') for i in f.readlines()]

    k = [i for i in k[:10] if len(i[0]) > 2 and len(i) == 2]
    a = [i[0] for i in k]
    b = [i[1] for i in k]
    s = dict(zip(a, b))
    html_template += """
    <h1> </h1>
    """
    html_template += """<h1><b>DOMAIN INFO </b></h1>"""
    html_template += f"""<h6 style='font-style:normal; font-size:60%;'><strong>{list(s.keys())[0]}:</strong> {list(s.values())[0]}</h6>\n"""

    for key, value in list(s.items())[1:]:
        html_template += f"""<h6 style='font-style:normal; font-size:60%;'><strong>{key}:</strong> {value}</h6>\n"""

    html_template += f"""<h6 style='font-style:italic; font-size:50%;'>For more info <a href={domain_info_path} style='color:blue;'>here</a></h6>\n"""
    html_template += """
    <h1> </h1>
    <hr style="border: 0.5px solid #6b6b6b; width: 200%;">
    <h1> </h1>
    """

    html_template += """
        <h1><b>TECHNOLOGY DETECTION RESULT</b></h1>

      <table>
        <tr>
          <th>Domain</th>
          <th>Info</th>
        </tr>  
      
    """

    def read_data_from_file(file_path):
        with open(file_path) as f:
            return f.read()

    def parse_data(data):
        lines = data.strip().split('\n')
        result = []

        for line in lines:
            parts = line.split(' => ')
            website = parts[0]
            info = parts[1].strip()

            result.append((website, info))
        return result

    def format_information(info, website):
        if info == '{}' or info == 'set()':
            return '<i>no-info</i>'

        formatted_info = ''
        info_list = info.strip('{}').split(',')
        info_list = [item for item in info_list]
        for key in info_list:
            formatted_info += f'<b>{key}</b><br>'

        return formatted_info

    def generate_table_rows(data_list):
        formatted_rows = []
        for website, info in data_list:
            formatted_info = format_information(info, website)
            formatted_rows.append(f'<tr><td>{website}</td><td>{formatted_info}</td></tr>\n')
        return formatted_rows

    data = read_data_from_file(technologies_file_path)
    parsed_data = parse_data(data)
    formatted_rows = generate_table_rows(parsed_data)

    table_rows = ''.join(formatted_rows)
    html_template += f"""{table_rows}
      </table>
      </div>
      </div>
      <div id="content">
</div>
    </div>
  </div>
</body>

</html>"""

    with open(info_html_report_path, 'w') as html_file:
        html_file.write(html_template)

    print(f'HTML report generated and saved to : {info_html_report_path}')
