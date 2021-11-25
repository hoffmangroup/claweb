
<div class="container" id="table-container">
	<div class="jumbotron">
		<h1>Gene: {{gene.name}}</h1>
		<ul>
			<li>Gene set: {{gene.dataset}}</li>
			<li>Discriminates {{gene.infos|count}}/{{gene.n_cl}} cell types</li>
		</ul>
	</div>
    <div class="apanel">
            <table class="table table-bordered">
                <thead>
                    <tr>
                        <td rowspan="2">Cell type</td>
                        <td style="text-align: center " colspan="3">Higher expression in</td>
                    </tr>
                    <tr>
                        <td class="td-count-col-header td-up">This cell type</td>
                        <td class="td-count-col-header td-down">Comparison cell type</td>
                        <td class="td-count-col-header td-neither">Neither</td>
                    </tr>


                </thead>

                <tbody>
                {% for group in gene.infos %}
                    <tr data-toggle="collapse" data-target="#collapse{{ loop.index }}" class="main-row">
                        <td ><i class="more-less glyphicon glyphicon-plus gi-10px"></i> {{group.print_name}}</td>
                        <td style="text-align:right">{{group.up_count}}</td>
                        <td style="text-align:right">{{group.down_count}}</td>
                        <td style="text-align:right">{{group.neither}}</td>
                    </tr>
                    <tr>
                        <td style="border-left-color: #ffffff" colspan="4" class="hiddenRow">
                            <div class="collapse" id="collapse{{ loop.index }}">
                                <table class="table table-bordered table-striped ">
                                    <thead>
                                        <tr>
                                            <td colspan="4">Comparison cell type</td>

                                        </tr>

                                    </thead>
                                    <tbody>

                                    {% for row in group.rows %}
                                        <tr>
                                            <td>{{ row[0].split(";;")[0] }}</td>
                                            {% if row[1] == 1%}
                                            <td class="td-count-col td-up"></td>
                                            {% else %}
                                                <td class="td-count-col"></td>
                                            {% endif %}
                                            {% if row[2] == 1%}
                                            <td class="td-count-col td-down"></td>
                                            {% else %}
                                            <td class="td-count-col"></td>
                                            {% endif %}
                                            <td class="td-count-col"></td>
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

<script type="text/javascript" src="{{site.url}}/static\scripts\d3.v3.min.js"></script>
{#<script type="text/javascript" src="{{site.url}}static\scripts\jquery.min.js"></script>#}
 <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
<script type="text/javascript" src="{{site.url}}/static\styles\dist\js\bootstrap.min.js"></script>

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