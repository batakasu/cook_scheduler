document.addEventListener("DOMContentLoaded", function() {
        var rawData = JSON.parse(document.getElementById('tasks-data').textContent);
        
        var items = new vis.DataSet(rawData);
        
        var container = document.getElementById('visualization');
        
        var options = {};
        var timeline = new vis.Timeline(container, items, options);
    });