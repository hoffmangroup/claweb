
<div class="container" id="table-container">
	<div class="jumbotron">
		<h1>Gene: {{gene}}</h1>
	</div>
    
    <img src="data:image/png;base64,{{my_plot}}"/>

	{% include 'footer.html' %}
</div>

<script type="text/javascript" src="{{site.url}}/static/scripts/d3.v3.min.js"></script>
<script type="text/javascript" src="{{site.url}}/static/scripts/jquery.min.js"></script>
<script type="text/javascript" src="{{site.url}}/static/styles/dist/js/bootstrap.min.js"></script>
