def generate_network_report(network_file_path, network_html_report_path):
	   with open(network_file_path, 'r') as file:
	   	lines = file.readlines()
	   data = []
	   current_entry = {}
	   for line in lines:
	       line = line.strip()
	       if line:
	           key,value = line.split(':')
	           current_entry[key.strip()] = value.strip()
	       else:
	           data.append(current_entry)
	           current_entry = {}
	   if current_entry:
	   	data.append(current_entry)
	   html_template = """
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
            width: 120%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        th, td {
            border: 1px solid #dddddd;
            text-align: left;
            padding: 12px;
            word-wrap: break-word;
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
          <li><a href="root/WebArmor/Report.html">INFO</a></li>
          <li><a href="None">VULNERABILITY SCAN</a></li>
          <li class="selected"><a href="root/WebArmor/reporting/utils/network.html">NETWORK SCAN</a></li>
          <li><a href="root/WebArmor/reporting/utils/owasp.html">OWASP SCAN</a></li>
          <li><a href="None">URLS</a></li>
          
        </ul>
      </div>
    </div>
    <div id="site_content">
      <div class="sidebar">
          
        <!-- insert your sidebar items here -->
      </div>
      <div id="content">
        <h1><b>Network Scan Report</b></h1>
    <table>
        <thead>
            <tr>
                <th>IP</th>
                <th>State</th>
                <th>Open Ports</th>
                <th>Services</th>
                <th>Versions</th>
            </tr>
        </thead>
        <tbody>"""
	   for entry in data:
	   	html_template +=f"""<tr>
                <td>{ entry['IP'] }</td>
                <td>{ entry['State'] }</td>
                <td>{ entry['Open Ports'] }</td>
                <td>{ entry['Services'] }</td>
                <td>{ entry['Versions'] }</td>
            </tr>"""
	   html_template += """
    </tbody>
  </table>
            
            
    </div>
    </div>
    <!-- Removed the footer content -->
  </div>
</body>

</html>
    """
	   with open(network_html_report_path, 'w') as output_file:
	   	output_file.write(html_template)
	   print(f"HTML report generated and saved to '{network_html_report_path}'.")