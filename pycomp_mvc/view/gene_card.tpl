
<div class="container" id="table-container">
	<div class="jumbotron">
		<h1>Gene: {{gene.name}}</h1>
		<ul>
			<li>Gene set: {{gene.dataset}}</li>
			<li>Discriminates {{gene.infos|count}} cell types</li>
		</ul>
	</div>
    <div>
{#		<div class="panel-group" id="accordion">#}
{#		<div class="panel panel-default">#}
{#    <div class="panel-heading">#}
{#      <h4 class="panel-title">#}
{#        <strong>Cell type</strong>#}
{#    <span class="label label-primary pull-right">down</span>#}
{#        <span class="label label-danger pull-right">up</span>#}
{#      </h4>#}
{#    </div>#}
            <table class="table table-bordered table-striped">
                <thead>
                    <tr>
                        <td>Cell type</td>
                        <td><span class="label label-danger">Up</span></td>
                        <td><span class="label label-primary">Down</span></td>
                    </tr>
                </thead>

                <tbody>
                {% for group in gene.infos %}
                    <tr class="accordion-toggle">
                        <td >{{group.name}}</td>
                        <td >{{group.up_count}}</td>
                        <td >{{group.down_count}}</td>
                    </tr>
                    <tr><td colspan="3">

                    <table class="table table-bordered table-striped ">
                        <thead>
                            <tr>
                                <td>Expression in cell type</td>
                                <td>Compared cell type</td>
                            </tr>

                        </thead>
                        <tbody>

                        {% for row in group.rows %}
                            <tr>
                            {% if row[2] >= 0 %}
                                {% if row[0] == group.name %}
                                    <td><span class="label label-danger"> </span></td>
                                {% else %}
                                    <td><span class="label label-primary"> </span></td>
                                {% endif %}
                                <td>{{row[1]}}</td>
                            {% else %}
                                {% if row[1] == group.name %}
                                    <td><span class="label label-danger"> </span></td>
                                {% else %}
                                    <td><span class="label label-primary"> </span></td>
                                {% endif %}
                                <td>{{row[0]}}</td>
                            {% endif %}
    {#                            <td>{{row[1]}}</td>#}
    {#                            <td>{{"%0.2f" % row[2]}}</td>#}
    {#                            <td>{{'{:.2e}'.format(row[3])}}</td>#}
                            </tr>
                        {% endfor %}
                        </tbody>
                    </table>
                    </td></tr>
            	{% endfor %}

                </tbody>
            </table>
    </div>


	{% include 'footer.html' %}
</div>

<script type="text/javascript" src="{{site.url}}/static/scripts/d3.v3.min.js"></script>
<script type="text/javascript" src="{{site.url}}/static/scripts/jquery.min.js"></script>
<script type="text/javascript" src="{{site.url}}/static/styles/dist/js/bootstrap.min.js"></script>
