<div class="container">
<div id="table-container">
	<div class="jumbotron">
		<h1>Cell Types</h1>
		<p>The following list contains the cell types for which important genes has been reported. Click on a cell type to see details.</p>
	</div>
	<div class="row">
		<div class="col-xs-12">
			<input class="search form-control" placeHolder="Search for a cell type"/>
		</div>
    </div>
	<div class="row">
    	<div class="col-xs-12">
		<table class="table table-striped">
			<thead>
				<tr>
					<th>Name</th>
					<th style="text-align: center;">Number of comparisons</th>
					{% for dataset in datasets %}
					<th style="text-align: center;">{{dataset.name}}</th>
					{% endfor%}

				</tr>
			</thead>
			<tbody class="list">
				{% for group in groups %}
				<tr>
					<td><a class="name" href="{{group.link}}">{{group.print_name}}</a></td>
					<td style="text-align: center;">{{group.nb_of_comp}}</td>
					{% for count in group.gene_count %}
					<td style="text-align: center;">{{count}}</td>
					{% endfor %}
				</tr>
				{% endfor %}
			</tbody>
		</table>
		</div>	
	</div>
	
	{% include 'footer.html' %}
</div>
</div>	



<script type="text/javascript" src="{{site.url}}/static/scripts/list.js"></script>
<script type="text/javascript">
var options = {
	valueNames: ['name']
};
var featureList = new List('table-container', options);
</script>
<script type="text/javascript" src="{{site.url}}/static/scripts/d3.v3.min.js"></script>
