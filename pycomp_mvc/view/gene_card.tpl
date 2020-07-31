
<div class="container" id="table-container">
	<div class="jumbotron">
		<h1>Gene: {{gene.name}}</h1>
		<ul>
			<li>Gene set: {{gene.dataset}}</li>
			<li>Discriminates {{gene.infos|count}}/{{gene.n_cl}} cell types</li>
		</ul>
	</div>
    <div class="apanel">
            <table class="table table-bordered table-striped">
                <thead>
                    <tr>
                        <td style="width:60%" rowspan="2">Cell type</td>
                        <td colspan="3">Higher in</td>
                    </tr>
                    <tr>
                        <td style="width:13%"><span class="label label-danger">This cell type</span></td>
                        <td style="width:13%"><span class="label label-primary">Comparison cell type</span></td>
                        <td style="width:13%">Neither</td>
                    </tr>


                </thead>

                <tbody>
                {% for group in gene.infos %}
                    <tr data-toggle="collapse" data-target="#collapse{{ loop.index }}" class="main-row">
                        <td style="width:60%"><i class="more-less glyphicon glyphicon-plus gi-10px"></i> {{group.name.split(";;")[0]}}</td>
                        <td style="width:13%">{{group.up_count}}</td>
                        <td style="width:13%">{{group.down_count}}</td>
                        <td style="width:13%">{{group.neither}}</td>
                    </tr>
                    <tr>
                        <td colspan="4" class="hiddenRow">
                            <div class="collapse" id="collapse{{ loop.index }}">
                                <table class="table table-bordered table-striped ">
                                    <thead>
                                        <tr>
                                            <td colspan="4"><strong>Comparison cell type</strong></td>

                                        </tr>

                                    </thead>
                                    <tbody>

                                    {% for row in group.rows %}
                                        <tr>
                                            {# move logic in model #}
                                            <td style="width:60%">{{ row[0].split(";;")[0] }}</td>
                                            {% if row[1] == 1%}
                                            <td style="width:13%;background-color: #dca7a7">{{ row[1] }}</td>
                                            {% else %}
                                                <td style="width:13%">{{ row[1] }}</td>
                                            {% endif %}
                                            {% if row[2] ==     1%}
                                            <td style="width:13%;background-color: #9acfea">{{ row[2] }}</td>
                                            {% else %}
                                            <td style="width:13%">{{ row[2] }}</td>
                                            {% endif %}
                                            <td style="width:13%">0</td>
{#                                        {% if row[2] >= 0 %}#}
{#                                            {% if row[0] == group.name %}#}
{#                                                <td><span class="label label-danger"> </span></td>#}
{#                                            {% else %}#}
{#                                                <td><span class="label label-primary"> </span></td>#}
{#                                            {% endif %}#}
{#                                            <td>{{row[1]}}</td>#}
{#                                        {% else %}#}
{#                                            {% if row[1] == group.name %}#}
{#                                                <td><span class="label label-danger"> </span></td>#}
{#                                            {% else %}#}
{#                                                <td><span class="label label-primary"> </span></td>#}
{#                                            {% endif %}#}
{#                                            <td>{{row[0]}}</td>#}
{#                                        {% endif %}#}

                                        </tr>
                                    {% endfor %}
                                    </tbody>
                                </table>
                            </div>
                        </td>
                    </tr>
            	{% endfor %}

                </tbody>
            </table>
    </div>


	{% include 'footer.html' %}
</div>

<script type="text/javascript" src="{{site.url}}static\scripts\d3.v3.min.js"></script>
{#<script type="text/javascript" src="{{site.url}}static\scripts\jquery.min.js"></script>#}
 <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
<script type="text/javascript" src="{{site.url}}static\styles\dist\js\bootstrap.min.js"></script>

<script>
    /*******************************
    * ACCORDION WITH TOGGLE ICONS
    *******************************/
	function toggleIcon(e) {
        {#console.log('toggle')#}
        {#console.log(#}
        {#    $(e.target.closest("tr"))#}
        {#        .prev(".main-row")#}
        {#        .find(".more-less")#}
        {#)#}

	    $(e.target.closest("tr"))
            .prev(".main-row")
            .find(".more-less")
            .toggleClass('glyphicon-plus glyphicon-minus');
    }
    $('.apanel').on('hidden.bs.collapse', toggleIcon);
    $('.apanel').on('shown.bs.collapse', toggleIcon);
</script>