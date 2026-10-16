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
    if (typeof taskList === 'string') {
        taskList = JSON.parse(taskList);
    }
    let memberList = JSON.parse(memberDataElement.textContent);
    if (typeof memberList === 'string') {
        memberList = JSON.parse(memberList);
    }

    // 3. タイムライン用のデータを生成
    const timelineItems = taskList.map(task => {
        let name = task.conflicting ? 'task-conflict' : '';
        return {
            id: task.id,
            content: task.content,
            group: task.group,
            start: new Date(task.start),
            end: new Date(task.end),
            className: name
        };
    });


    // タスクの有無に応じた全体制限範囲の設定 (min / max)
    let firstTaskDate = null;
    let lastTaskDate = null;
    let startDate, endDate;

    if (timelineItems.length > 0) {
        firstTaskDate = timelineItems[0].start;
        lastTaskDate = timelineItems[0].end;

        for (let i = 1; i < timelineItems.length; i++) {
            if (timelineItems[i].start < firstTaskDate) firstTaskDate = timelineItems[i].start;
            if (timelineItems[i].end > lastTaskDate) lastTaskDate = timelineItems[i].end;
        }

        startDate = new Date(firstTaskDate.getFullYear(), firstTaskDate.getMonth(), firstTaskDate.getDate(), 0, 0, 0);
        endDate = new Date(lastTaskDate.getFullYear(), lastTaskDate.getMonth(), lastTaskDate.getDate() + 1, 0, 0, 0);
    }

    // --- ★ localStorage から前回の表示範囲（ズーム・スクロール状態）を復元 ---
    const savedStart = localStorage.getItem(`timeline_start_${projectId}`);
    const savedEnd = localStorage.getItem(`timeline_end_${projectId}`);
    
    let initialStart = savedStart ? new Date(savedStart) : startDate;
    let initialEnd = savedEnd ? new Date(savedEnd) : endDate;

    // 4. タイムラインのオプション設定
    const options = {
        locale: 'ja',
        zoomable: true,
        moveable: true,
        stack: true,
        showCurrentTime: false,
        orientation: 'top',
        editable: true,
        selectable: true,
        multiselect: false,
        start: initialStart, // 復元した開始位置
        end: initialEnd,     // 復元した終了位置

        margin: {
            axis: 3,
            item: {horizontal: 0, vertical: 6}
        },

        format: {
            minorLabels: {minute: 'HH:mm', hour: 'HH:mm'},
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
                if (data.success) {
                    callback(item);
                } else {
                    callback(null);
                }
            })
            .catch(() => callback(null));
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
                if (data.success) {
                    callback(item);
                    location.reload();
                } else {
                    callback(null);
                }
            })
            .catch(() => callback(null));
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
                    callback(item);
                    location.reload();
                } else {
                    callback(null);
                }
            })
            .catch(() => callback(null));
        },
        
        zoomMin: 1000 * 60 * 45,
        zoomMax: 1000 * 60 * 60 * 24 * 2,
        min: startDate,
        min: startDate,
        max: endDate,
    };

    // 5. タイムラインを描画（ここで初めて timeline インスタンスが生成される）
    const items = new vis.DataSet(timelineItems);
    const groups = new vis.DataSet(memberList);
    const timeline = new vis.Timeline(container, items, groups, options);

    // 初期表示としてプロジェクトの詳細を表示
    showProjectDetail();

    // --- ★ タイムライン生成後にイベントやボタン処理を記述 ---

    // ズームやスクロール位置が変わったときに保存（プロジェクトごとに分けるためIDを付与）
    timeline.on('rangechanged', function (properties) {
        localStorage.setItem(`timeline_start_${projectId}`, properties.start.toISOString());
        localStorage.setItem(`timeline_end_${projectId}`, properties.end.toISOString());
    });

    // 選択イベント
    timeline.on('select', function(properties) {
        if (properties.items.length > 0) {
            const taskId = properties.items[0];
            const task = taskList.find(t => t.id === taskId);
            showTaskDetail(task, memberList);
        } else {
            showProjectDetail();
        }
    });

    // ダブルクリックイベント
    timeline.on('doubleClick', function(properties) {
        if (properties.item) {
            const taskId = properties.item;
            window.location.href = `/schedules/${projectId}/tasks/${taskId}/`;
        }
    });

    // タスクコピーボタン
    const copyButton = document.getElementById('copy-button');
    if (copyButton) {
        copyButton.addEventListener('click', () => {
            const selectedItems = timeline.getSelection();
            if (selectedItems.length === 0) return;
            const selectedTaskId = selectedItems[0];

            fetch('/schedules/copy_task/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({ task_id: selectedTaskId })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    location.reload();
                } else {
                    console.error(data.error);
                }
            });
        });
    }

    // 開始時刻に戻るボタン
    const goStartButton = document.getElementById('go-start-button');
    if (goStartButton && taskList.length > 0) {
        const firstTask = taskList.reduce((first, task) => {
            return new Date(task.start) < new Date(first.start) ? task : first;
        });

        const firstStart = new Date(firstTask.start);
        const firstEnd = new Date(firstTask.end);

        goStartButton.addEventListener('click', () => {
            const viewStart = new Date(firstStart.getTime() - 5 * 60 * 1000);
            const viewEnd = new Date(firstEnd.getTime() + 15 * 60 * 1000);

            timeline.setWindow(viewStart, viewEnd, {
                animation: { duration: 500, easingFunction: 'easeInOutQuad' }
            });
        });
    }

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

function showTaskDetail(task, memberList) {
    const start = new Date(task.start);

    const startText = start.toLocaleString('ja-JP', {
        month: 'numeric',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
    
    const member = memberList.find(m => m.id === task.group);

    document.getElementById('detail-title').textContent = task.content;
    document.getElementById('detail-member').textContent = member?.content ?? '未設定';
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