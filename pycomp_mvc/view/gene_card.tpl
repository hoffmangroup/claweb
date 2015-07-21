
<div class="container" id="table-container">
	<div class="jumbotron">
		<h1>Gene: {{gene.name}}</h1>
		<ul>
			<li>Dataset: {{gene.dataset}}</li>
			<li>Coordinates: {{gene.coordinates}}</li>
			<li>Found in {{gene.infos|count}} cell types</li>
            <li><a href="{{gene_dist}}.html">Show distribution</a></li>
		</ul>
	</div>
		<div class="panel-group" id="accordion">
		<div class="panel panel-default">
    <div class="panel-heading">
      <h4 class="panel-title">
        <strong>Cell type</strong>
    <span class="label label-primary pull-right">down</span>
        <span class="label label-danger pull-right">up</span>
      </h4>
    </div>
    
  </div>
	{% for group in gene.infos %}

	  <div class="panel panel-default">
	    <div class="panel-heading">
	      <h4 class="panel-title">
	        <a data-toggle="collapse" data-parent="#accordion" href="#collapse{{loop.index}}" class="collapsed">
	          {{group.name}}
	          {% if group.down_count %}
	          <span class="label label-primary pull-right">{{group.down_count}}</span>
	          {% endif %}
	          {% if group.up_count%}
	          <span class="label label-danger pull-right">{{group.up_count}}</span>
	          {% endif %}
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
				    <th>T-Test</th>
                    <th>P-value</th>

		      	</tr>
	      	</thead>
	      	<tbody>
	      	{% for row in group.rows %}
	      		<tr>
		      		<td>{{row[0]}}</td>
		      		<td>{{row[1]}}</td>
				    <td>{{"%0.2f" % row[2]}}</td>
                    <td>{{'{:.2e}'.format(row[3])}}</td>
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

<script type="text/javascript" src="{{site.url}}/scripts/d3.v3.min.js"></script>
<script type="text/javascript" src="{{site.url}}/scripts/jquery.min.js"></script>
<script type="text/javascript" src="{{site.url}}/styles/dist/js/bootstrap.min.js"></script>
