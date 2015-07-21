<div class="container">
	<div class="row">
		<div class="col-md-12">
			<div class="jumbotron">
				<h1>{{cl.name|capitalize}}</h1>
				<p>The table below is a summary of cell specific genes and the number of pairwise comparison in which they are found. 
				</p>
			</div>
			<div class="tab-content">
  				<div class="tab-pane fade active in" id="tableView">
					<div class="row">
						<div class="col-md-12">
							<table class="table table-bordered table-striped">
								<tr>
								{% for data, count in cl.header %}
									<th>{{data}}</th>
									<th>
										<a data-toggle="tooltip" title="Total number of pairwise comparison that return robust results">{{count}}</a>
									</th>
								{% endfo %}
								</tr>
								
								{% for row in cl.rows %}
									<tr>
									{% for gene, count in row %}
										<td><a href="{{site.url}}/genes/{{cl.header[loop.index0][0]}}/{{gene}}.html">{{gene}}</a></td>
										<td>{{count}}</td>
									{% endfor %}
									</tr>
								{% endfor %}
							</table>
						</div>

					</div>
				</div>
			</div>
		</div>
	</div>	
{% include 'footer.html' %}
	<hr>
</div>
    <!--<script type="text/javascript" src="{{site.url}}/scripts/jquery.min.js"></script>-->
    <!--<script type="text/javascript" src="{{site.url}}/scripts/list.js"></script>-->
    <!--<script type="text/javascript" src="{{site.url}}/styles/dist/js/bootstrap.min.js"></script>-->
    <!--<script type="text/javascript" src="{{site.url}}/scripts/d3.v3.min.js"></script>-->
    <!--<script type="text/javascript">-->
    	<!--var datasets = "{{site.datasets|join(',')}}".split(',');-->
		<!--celltype("{{site.datasets|join(',')}}", "../data/celltypes/gene_comparisons/{{cl.ID}}.json")-->

	<!--</script>-->
    
    



