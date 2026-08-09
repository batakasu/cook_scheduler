document.addEventListener("DOMContentLoaded", function() {
    // 1. HTMLからデータ要素を取得
    const dataElement = document.getElementById('tasks-data');
    const container = document.getElementById('visualization');

    if (!dataElement || !container) return;

    // 2. タスクデータの取得
    let taskList = JSON.parse(dataElement.textContent);
    if (typeof taskList === 'string') {
        taskList = JSON.parse(taskList);
    }

    // 3. タイムライン用のデータを生成（Djangoから来た start/end をそのまま使う）
    const timelineItems = taskList.map(task => {
        return {
            id: task.id,
            content: task.content, // Django側から来ている 'content' を使用
            start: new Date(task.start), // 文字列をDate型に変換
            end: new Date(task.end)      // 文字列をDate型に変換
        };
    });

    const sortedByStart = [...timelineItems].sort((a, b) => a.start - b.start);
    const firstTask = sortedByStart[0].start;

    const sortedByEnd = [...timelineItems].sort((a, b) => a.end - b.end);
    const lastTask = sortedByEnd[sortedByEnd.length - 1].end;
    let startDate = new Date(firstTask.getFullYear(), firstTask.getMonth(), firstTask.getDate(), 0, 0, 0);
    let endDate = new Date(lastTask.getFullYear(), lastTask.getMonth(), lastTask.getDate() + 1, 0, 0, 0);

    // 4. タイムラインのオプション設定
    const options = {
        locale: 'ja',
        zoomable: true,
        moveable: true,
        stack: false,
        showCurrentTime: false,
        orientation:'top',
        editable: true,
        
        onMove: function(item, callback) {
            // Django側へデータを送信（Ajax通信）
            fetch('/tasks/update-task-time/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    id: item.id,
                    start: item.start,
                    end: item.end
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
        
        zoomMin: 1000 * 60 ,    // ミリ秒 * 秒
        zoomMax: 1000 * 60 * 60 * 24 * 2,   // ミリ秒 * 秒 * 分 * 時 * 日
        // 
        min: startDate, // これより過去にはスクロールできない
        max: endDate,   // これより未来にはスクロールできない
    };

    // 5. タイムラインを描画
    const timeline = new vis.Timeline(container, new vis.DataSet(timelineItems), options);
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