document.addEventListener("DOMContentLoaded", function() {

    // 1. HTMLからデータ要素を取得
    const taskDataElement = document.getElementById('tasks-data');
    const memberDataElement = document.getElementById('members-data');
    const container = document.getElementById('visualization');
    const projectId = container.getAttribute('data-project-id');
    const startTimeElement = document.getElementById('project-start-time');

    if (!taskDataElement || !memberDataElement || !container) return;

    // 2. タスクデータの取得
    let taskList = JSON.parse(taskDataElement.textContent);
    if (typeof taskList === 'string')
    {
        taskList = JSON.parse(taskList);
    }
    let memberList = JSON.parse(memberDataElement.textContent);
    if (typeof memberList == 'string')
    {
        memberList = JSON.parse(memberList)
    }

    // 3. タイムライン用のデータを生成（Djangoから来た start/end をそのまま使う）
    const timelineItems = taskList.map(task => {
        let name
        if (task.conflicting) {
            name = 'task-conflict'
        } else {
            name = ''
        }

        return {
            id: task.id,
            content: task.content, // Django側から来ている 'content' を使用
            group: task.group,
            start: new Date(task.start), // 文字列をDate型に変換
            end: new Date(task.end),     // 文字列をDate型に変換
            className: name
        };
    });

    let defaultTime = startTimeElement ? new Date(JSON.parse(startTimeElement.textContent)) : new Date();
    let startDate, endDate;

    // タスクの有無に応じた表示範囲の設定
    if (timelineItems.length > 0) {
        const sortedByStart = [...timelineItems].sort((a, b) => a.start - b.start);
        const firstTask = sortedByStart[0].start;

        const sortedByEnd = [...timelineItems].sort((a, b) => a.end - b.end);
        const lastTask = sortedByEnd[sortedByEnd.length - 1].end;

        startDate = new Date(firstTask.getFullYear(), firstTask.getMonth(), firstTask.getDate(), 0, 0, 0);
        endDate = new Date(lastTask.getFullYear(), lastTask.getMonth(), lastTask.getDate() + 1, 0, 0, 0);
    } else {
        startDate = new Date(defaultTime.getFullYear(), defaultTime.getMonth(), defaultTime.getDate(), 0, 0, 0);
        endDate = new Date(defaultTime.getFullYear(), defaultTime.getMonth(), defaultTime.getDate() + 1, 0, 0, 0);
    }

    // 4. タイムラインのオプション設定
    const options = {
        locale: 'ja',
        zoomable: true,
        moveable: true,
        stack: true,
        showCurrentTime: false,
        orientation:'top',
        editable: true,
        // 一つのみ選択可
        selectable: true,
        multiselect: false,

        margin: {
            axis: 3,
            item: {horizontal: 0, vertical: 6}
        },

        format: {minorLabels: {minute: 'HH:mm', hour: 'HH:mm'},
                 majorLabels: {minute: 'M/D', hour: 'M/D'}
        },

        onMove: function(item, callback) {
            fetch('/schedules/update_task/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    id: item.id,
                    group: item.group,
                    start: item.start,
                    end: item.end
                })
            })
            .then(response => response.json())
            .then(data => {
                if(data.success) {
                    callback(item); // 成功したら変更を確定する
                } else {
                    callback(null); // 失敗した場合は移動を元に戻す
                }
            })
            .catch(error => {
                callback(null); // エラー時も元に戻す
            });
        },

        onAdd: function(item, callback) {
            fetch('/schedules/add_new_task/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    project_id: projectId,
                    id: item.id,
                    content: "タイトル無し",
                    group: item.group,
                    start: item.start
                })
            })
            .then(response => response.json())
            .then(data => {
                if(data.success) {
                    callback(item); // 成功したら変更を確定する
                    location.reload();
                } else {
                    callback(null); // 失敗した場合は移動を元に戻す
                }
            })
            .catch(error => {
                callback(null); // エラー時も元に戻す
            });
        },

        onRemove: function(item, callback) {
            fetch(`/schedules/delete/${item.id}/`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(response => {
                if (response.ok) {
                    callback(item); // 成功した場合は callback(item) で確定
                    location.reload();
                } else {
                    callback(null); // 失敗した場合は callback(null) で削除をキャンセル
                }
            })
            .catch(error => {
                callback(null); // エラー時も元に戻す
            });
        },
        
        zoomMin: 1000 * 60 * 45,    // ミリ秒 * 秒 * 分
        zoomMax: 1000 * 60 * 60 * 24 * 2,   // ミリ秒 * 秒 * 分 * 時 * 日
        // 
        min: startDate, // これより過去にはスクロールできない
        max: endDate,   // これより未来にはスクロールできない
    };

    const goStartButton = document.getElementById('go-start-button');

    const firstTask = taskList.reduce((first, task) => {
        return new Date(task.start) < new Date(first.start) ? task : first;
    });

    // 開始時刻に戻るボタンのプログラム
    const firstStart = new Date(firstTask.start);
    const firstEnd = new Date(firstTask.end);

    goStartButton.addEventListener('click', () => {
        const viewStart = new Date(firstStart.getTime() - 5 * 60 * 1000);
        const viewEnd = new Date(firstEnd.getTime() + 15 * 60 * 1000);

        timeline.setWindow(viewStart, viewEnd,
            {
                animation: {
                    duration: 500,
                    easingFunction: 'easeInOutQuad'
                }
            }
        );
    });

    // 5. タイムラインを描画
    const items = new vis.DataSet(timelineItems)
    const groups = new vis.DataSet(memberList)
    const timeline = new vis.Timeline(container, items, groups, options);
    showProjectDetail();

    // 6. タイムライン上でのイベントの設定
    timeline.on('select', function(properties) {
        if (properties.items.length > 0) {
            const taskId = properties.items[0];
            const task = taskList.find(task => task.id === taskId);
            showTaskDetail(task);

        } else {
            showProjectDetail();
        }
    });
    timeline.on('doubleClick', function(properties) {
        // タスクをダブルクリックすることでそのタスクのdetailへ
        if (properties.item) {
            const taskId = properties.item;
            window.location.href = `/schedules/${projectId}/tasks/${taskId}/`;
        }
    });

}, false);

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function showTaskDetail(task) {
    const start = new Date(task.start);

    const startText = start.toLocaleString('ja-JP', {
        month: 'numeric',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });

    document.getElementById('detail-title').textContent = task.content;
    document.getElementById('detail-start').textContent = startText;
    document.getElementById('detail-duration').textContent = task.duration;
    document.getElementById('detail-description').textContent = task.description;
}

const projectData = {
    title: document.getElementById('detail-title').textContent,
    start: document.getElementById('detail-start').textContent,
    description: document.getElementById('detail-description').textContent
};
function showProjectDetail() {
    document.getElementById('detail-title').textContent = projectData.title;
    document.getElementById('detail-start').textContent = projectData.start;
    document.getElementById('detail-description').textContent = projectData.description;
}