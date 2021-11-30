
<div class="container" id="table-container">
	<div class="jumbotron">
		<h1>List of cell type pairs</h1>
		<p>Click on a cell type to show the link for all comparison's results</p>
	</div>
		<div class="panel-group" id="accordion">
		<div class="panel panel-default">
    <div class="panel-heading">
      <h4 class="panel-title">
        <strong>Cell type</strong>
      </h4>
    </div>
    
  </div>
	{% for group, comparisons in groups.items() %}

	  <div class="panel panel-default">
	    <div class="panel-heading">
	      <h4 class="panel-title">
	        <a data-toggle="collapse" data-parent="#accordion" href="#collapse{{loop.index}}" class="collapsed">
	          {{group}}
	        </a>
	      </h4>
	    </div>
	    <div id="collapse{{loop.index}}" class="panel-collapse collapse">
	      <div class="panel-body">
	      
	      <table class="table">
	      	<thead>
		        <tr>
		      		<th>Group 1</th>
		      		<th>Group 2</th>
				    <th>Results</th>
		      	</tr>
	      	</thead>
	      	<tbody>
	      	{% for comp in comparisons %}
	      		<tr>
		      		<td>{{comp['group1']}}</td>
		      		<td>{{comp['group2']}}</td>
				    <td><a href="{{comp.url}}">results</a></td>
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
