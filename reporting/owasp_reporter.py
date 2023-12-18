def xss_reporter(xss_file_path):
    with open(xss_file_path, 'r') as input_file:
        content = [line.split() for line in input_file.readlines()]

    # Existing HTML template for the report
    global html_template
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
          border-collapse: collapse;
          width: 120%;
        }
        th, td {
          border: 1px solid #dddddd;
          text-align: left;
          padding: 8px;
          font:bold;
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
          <li><a href="root/WebArmor/reporting/utils/network.html">NETWORK SCAN</a></li>
          <li class="selected"><a href="root/WebArmor/reporting/utils/owasp.html">OWASP SCAN</a></li>
          <li><a href="None">URLS</a></li>
          
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
    if len(content)!=0:
        for con in content:
        	if len(con)!=0:
        	   for i in con:
        	   	if con.index(i) % 2 == 0 and con.index(i) < len(con) - 1:
        	   		title = i
        	   		content_text = con[con.index(i) + 1]
        	   		html_template += f"""
            <h4><b>{title}</b></h4>
            <textarea class="textbox" rows="4" cols="50">{content_text}</textarea>
            """
        	else:
        		html_template += """
            <h2><b>No Xss Vulns were found</b></h2>
            """
        		break
    else:
    	html_template += """
            <h2><b>No Xss Vulns were found</b></h2>
            """
    	

    html_template += """
    <hr style="border: 0.5px solid #6b6b6b; width: 200%;">
    """


def open_redir_reporter(open_redir_file_path):
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

    html_template+='''
   
      <h2><b>Open-Redirect Result/POC</b></h2>
      <table>
        <tr>
          <th>Endpoint</th>
          <th>Payload</th>
          <th>Vulnerable Param</th>
          <th>POC</th>
        </tr>
    '''

    for entry in data:
        html_template += f'''
        <tr>
          <td>{entry[0]}</td>
          <td>{entry[1]}</td>
          <td>{entry[2]}</td>
          <td>{entry[3]}</td>
        </tr>
        '''

    html_template+= '''</table>
    </div>
      </div>
      <div id="content">
</div>
    </div>
  </div>
</body>

</html>
    '''
def generate_owasp_report(xssFile_path,open_redirFile_path,output_path):
	xss_reporter(xssFile_path)
	open_redir_reporter(open_redirFile_path)
	with open(output_path,'w') as f:
		f.write(html_template)
	print(f'Report saved to : {output_path}')