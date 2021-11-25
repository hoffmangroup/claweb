
<div class="container" id="table-container">
	<div class="jumbotron">
		<h1>Cell type pairs</h1>

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
	{% for d in dataset_genes %}

	  <div class="panel panel-default">
	    <div class="panel-heading">
	      <h4 class="panel-title">
	        <a data-toggle="collapse" data-parent="#accordion" href="#collapse{{loop.index}}" class="collapsed">
	          {{d['name']}}
	        </a>
	      </h4>
	    </div>
	    <div id="collapse{{loop.index}}" class="panel-collapse collapse">
	      <div class="panel-body">
	      
	      <table class="table">
	      	<thead>
		        <tr>
		      		<th>Group1</th>
		      		<th>Group2</th>
		      		<th>Gene</th>
				    <th>T-Test</th>
				    <th>P-value</th>
{#				    <th>link</th>#}
		      	</tr>
	      	</thead>
	      	<tbody>
	      	{% for row in d.rows %}
	      		<tr>
		      		<td>{{row.name1}}</td>
		      		<td>{{row.name2}}</td>
		      		<td>{{row.gene}}</td>
				    <td>{{"%0.2f" % row['t-test']}}</td>
				    <td>{{'{:.2e}'.format(row['p-value'])}}</td>
{#                    <td><a href="{{row.gene_dist_url}}.html">distribution</a></td>#}
		      	</tr>
			{% endfor %}
	      	</tbody>
	      </table>
	      </div>
	    </div>
	  </div>
	 
	{% endfor %}	
  </div>

	{% include 'footer.html' %}
</div>

<script type="text/javascript" src="{{site.url}}/static/scripts/d3.v3.min.js"></script>
<script type="text/javascript" src="{{site.url}}/static/scripts/jquery.min.js"></script>
<script type="text/javascript" src="{{site.url}}/static/styles/dist/js/bootstrap.min.js"></script>
