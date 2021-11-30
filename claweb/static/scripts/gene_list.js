var gene_list = function (datasets)
{
    datasets = datasets.split(",");
    for (var i = 0; i < datasets.length; i++) {
        
        var options = {
            valueNames: ['name'],
            listClass: [datasets[i]]
        };

        var transcript = new List('gene-list', options);
    }
}