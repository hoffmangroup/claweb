<div class="container"  id="gene-list">
    <div class="jumbotron">
        <h1>Genes</h1>
        <p>The following list contains the genes reported as being important classifier in at least 1 pairwise comparison. Click on a gene to see details.</p>
    </div>
    <div class="row">
        <div class="col-xs-6">
            <form class="form-horizontal" role="form">

                <div class="form-group">
                    <label class="col-xs-4 control-label">Search: </label>
                    <div class="col-xs-8">
                        <input class="search form-control" placeHolder="Gene"/>
                    </div>
                </div>
            </form>
        </div>
    </div>
    <div class="row">
        {% for dataset in d %}
        <div class="col-xs-3">
            <table class="table table-bordered table-striped">
                <thead>
                    <tr>
                        <th>{{dataset.name}}</th>
                    </tr>
                </thead>
                <tbody class="{{dataset.name}}">
                    {% for gene in dataset.genes %}
                    <tr>
                        <td><a class="name" href="{{site.url}}/genes/{{dataset.name}}/{{gene.filename}}">{{gene.name}}</a>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        {% endfor %}
    </div>
    {% include 'footer.html' %}
</div>
<script type="text/javascript" src="{{site.url}}/static/scripts/list.js"></script>
<script type="text/javascript" src="{{site.url}}/static/scripts/gene_list.js"></script>
<script type="text/javascript">
      gene_list("{{datasets_name}}");
</script>