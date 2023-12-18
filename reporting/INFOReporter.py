def generate_info_report(data_file, output_file):
    html_template ="""
    <!DOCTYPE HTML>
<html>

<head>
  <title>WEB ARMOR</title>
  <meta name="description" content="website description" />
  <meta name="keywords" content="website keywords, website keywords" />
  <meta http-equiv="content-type" content="text/html; charset=UTF-8" />
  <!-- Include the extracted CSS styles here -->
  <style type="text/css">
    .textbox {
                font-style: normal;
                font-size: small;
                width: 100%;
                margin-bottom: 10px;
            }
    body {
      font: normal .80em 'trebuchet ms', arial, sans-serif;
      background: #F0EFE2 url(background.png) repeat;
      color: #000;
    }

    h1, h2, h3, h4, h5, h6 {
      font: normal 175% 'century gothic', arial, sans-serif;
      color: #000;
      margin: 0 0 15px 0;
      padding: 15px 0 5px 0;
    }

    h2 {
      font: normal 175% 'century gothic', arial, sans-serif;
    }

    h4, h5, h6 {
      margin: 0;
      padding: 0 0 5px 0;
      font: normal 120% arial, sans-serif;
    }

    h5, h6 {
      font: italic 95% arial, sans-serif;
      padding: 0 0 15px 0;
    }

    a, a:hover {
      outline: none;
      text-decoration: underline;
      color: #000;
    }

    a:hover {
      text-decoration: none;
    }

    #main, #logo, #menubar, #site_content, #footer {
      margin-left: auto;
      margin-right: auto;
    }

    #header {
      background: transparent;
      height: 202px;
    }

    #logo {
      width: 898px;
      position: relative;
      height: 148px;
      border-bottom: 2px solid #FFF;
    }

    #logo #logo_text {
      position: absolute;
      top: 20px;
      left: 0;
    }

    #logo h1, #logo h2 {
      font: normal 300% 'century gothic', arial, sans-serif;
      border-bottom: 0;
      text-transform: none;
      margin: 0;
    }

    #logo_text h1, #logo_text h1 a, #logo_text h1 a:hover {
      padding: 22px 0 0 0;
      color: black;
      letter-spacing: -1px;
      text-decoration: none;
    }

    #logo_text h1 a .logo_colour {
      color: Black;
    }

    #logo_text h2 {
      font-size: 100%;
      padding: 4px 0 0 0;
      color: #FFF;
    }

    #menubar {
      width: 898px;
      height: 52px;
      padding: 0;
      background: #000;
    }

    ul#menu, ul#menu li {
      float: left;
      margin: 0;
      padding: 0;
    }

    ul#menu li {
      list-style: none;
    }

    ul#menu li a {
      letter-spacing: 0.15em;
      font: normal 100% arial, sans-serif;
      display: block;
      float: left;
      height: 17px;
      margin: 10px 0 0 10px;
      padding: 9px 26px 6px 26px;
      text-align: center;
      color: #FFF;
      text-transform: uppercase;
      text-decoration: none;
      background: transparent;
    }

    ul#menu li a:hover, ul#menu li.selected a, ul#menu li.selected a:hover {
      color: skyblue;
      background: transparent url(transparent_light.png) repeat;
    }

    #site_content {
      width: 854px;
      overflow: hidden;
      margin: 0 auto 0 auto;
      padding: 0 24px 20px 20px;
      background: #FFF;
    }

    #content {
      text-align: left;
      float: left;
      width: 595px;
      padding: 0;
    }
    table {
          border-collapse: collapse;
          width: 100%;
        }
        th, td {
          border: 1px solid #dddddd;
          text-align: left;
          padding: 8px;
        }
        th {
          background-color: #f2f2f2;
        }
  </style>
  <!-- End of extracted CSS styles -->
  <link rel="stylesheet" type="text/css" href="style/style.css" title="style" />
</head>

<body>
  <div id="main">
    <div id="header">
      <div id="logo">
        <div id="logo_text">
          <!-- class="logo_colour", allows you to change the colour of the text -->
          <h1><a href="root/WebArmor/Report.html"><b>WEB ARMOR</b></a></h1>
        </div>
      </div>
      <div id="menubar">
        <ul id="menu">
          <!-- put class="selected" in the li tag for the selected page - to highlight which page you're on -->
          <li class="selected"><a href="root/WebArmor/Report.html">INFO</a></li>
          <li><a href="None">VULNERABILITY SCAN</a></li>
          <li><a href="root/WebArmor/reporting/utils/network.html">NETWORK SCAN</a></li>
          <li><a href="root/WebArmor/reporting/utils/owasp.html">OWASP SCAN</a></li>
          <li><a href="None">URLS</a></li>
          
        </ul>
      </div>
    </div>
    <div id="site_content">
      <div class="sidebar">
      <h3><b>SCAN REPORT</b></h3>
        <h4>Target : hackerone.com</h4>
        <h5>Scan date : 11 September 2001</h5>    
        <h1><b>TECHNOLOGY Detection</b></h1>

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
        if info == '{}':
            return '<i>no-info</i>'
        
        formatted_info = ''
        info_dict = eval(info)
        for key, values in info_dict.items():
            formatted_info += f'<b>{key}</b> : {", ".join(values)}<br>'

        return formatted_info

    def generate_table_rows(data_list):
        formatted_rows = []
        for website, info in data_list:
            formatted_info = format_information(info,website)
            formatted_rows.append(f'<tr><td>{website}</td><td>{formatted_info}</td></tr>\n')
        return formatted_rows

    data = read_data_from_file(data_file)
    parsed_data = parse_data(data)
    formatted_rows = generate_table_rows(parsed_data)
    
    table_rows=''.join(formatted_rows)
    html_template+=f"""{table_rows}
      </table>
      </div>
      </div>
      <div id="content">
</div>
    </div>
  </div>
</body>

</html>"""
    
    with open(output_file, 'w') as html_file:
        html_file.write(html_template)

    print(f'HTML report generated successfully: {output_file}')