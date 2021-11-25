<div class="container">

	<div class="jumbotron">
		<h1>Cell Lineage Analysis</h1>
    <p>This analysis aims to identify the minimum set of genes defining branches among the lineage tree
        relating the cell types to each other.
        In total we generated succinct lists of transcription factors, lncRNAs, and cell surface markers (CD genes)
        defining {{number_of_cl}} cell types. This interface allows exploring the results either by cell types, genes or by cell type pairs.</p>

		<a href="{{site.url}}/group_list.html" class="btn btn-primary btn-lg">Cell Types &raquo;</a>
		<a href="{{site.url}}/gene_list.html" class="btn btn-primary btn-lg">Genes &raquo;</a>
        <a href="{{site.url}}/comparison_list.html" class="btn btn-primary btn-lg">Cell type pairs &raquo;</a>
	</div>

  {% include 'footer.html' %}
</div>