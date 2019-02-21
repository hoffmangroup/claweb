
<div class="container" id="table-container">
	<div class="jumbotron">
		<h1>Comparison</h1>

        <p>Here you can find the results for the comparison between {{group1_name}} and {{group2_name}}</p>
	</div>
		<div class="panel-group" id="accordion">
		<div class="panel panel-default">
    <div class="panel-heading">
      <h4 class="panel-title">
        <strong>Results</strong>

      </h4>
    </div>

  </div>
      <p>There is no results for this comparison</p>
  </div>

	{% include 'footer.html' %}
</div>

<script type="text/javascript" src="{{site.url}}/static/scripts/d3.v3.min.js"></script>
<script type="text/javascript" src="{{site.url}}/static/scripts/jquery.min.js"></script>
<script type="text/javascript" src="{{site.url}}/static/styles/dist/js/bootstrap.min.js"></script>
