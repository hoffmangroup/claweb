<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="utf-8">
	<title>Cell lineage analysis using Random Forest</title>
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<meta name="description" content="">
	<meta name="author" content="">
	<!-- Le styles -->
	<link rel="stylesheet" href="{{site.url}}/static/styles/dist/css/bootstrap.css" />
	<link rel="stylesheet" href="{{site.url}}/static/styles/dist/css/bootstrap-theme.css" />
	<link rel="stylesheet" href="{{site.url}}/static/styles/navbar-fixed-top.css" />
	<link rel="stylesheet" href="{{site.url}}/static/styles/bootstrap-hack.css" />

	<!-- Fav and touch icons -->
	<!-- <link rel="shortcut icon" href="{{site.url}}/ico/favicon.ico"> -->
</head>
	<body>
  	<div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
        <div class="container">
          <div class="navbar-header">
            <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
              <span class="sr-only">Toggle navigation</span>
              <span class="icon-bar"></span>
              <span class="icon-bar"></span>
              <span class="icon-bar"></span>
            </button>
            <a class="navbar-brand" href="{{site.url}}/index.html">Cell Lineage Analysis</a>
          </div>
          <div class="navbar-collapse collapse">
            <ul class="nav navbar-nav">
              <li><a href="{{site.url}}/group_list.html">Cell types</a></li>
  			<li><a href="{{site.url}}/comparison_list.html">Cell type pairs</a></li>
  			<li><a href="{{site.url}}/gene_list.html">Genes</a></li>
            </ul>
            <ul class="nav navbar-nav navbar-right">
              <li><a href="#" class="navbar-link">Top</a></li>
            </ul>
          </div><!--/.nav-collapse -->
        </div>

      </div>
		  {% include tpl %}
	</body>
</html>
