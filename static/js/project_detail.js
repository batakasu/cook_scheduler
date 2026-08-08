document.addEventListener("DOMContentLoaded", function() {
    const dataElement = document.getElementById('tasks-data');
    if (!dataElement) return;

    let rawData = JSON.parse(dataElement.textContent);
    const container = document.getElementById('visualization');
    if (!container || !rawData || rawData.length === 0) return;

    let taskList = rawData;
    if (typeof rawData === 'string') {
        taskList = JSON.parse(rawData);
    }

    if (!Array.isArray(taskList)) return;

    const formattedData = taskList.map(item => ({
        id: item.id,
        content: item.content,
        start: new Date(item.start),
        end: new Date(item.end)
    }));

    const items = new vis.DataSet(formattedData);
    const options = { locale: 'ja' };
    const timeline = new vis.Timeline(container, items, options);
}, false);