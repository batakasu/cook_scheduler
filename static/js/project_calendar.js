document.addEventListener("DOMContentLoaded", function() {
    const calendarEl = document.getElementById('calendar');

    const calendar = new FullCalendar.Calendar(calendarEl, {
    	initialView: 'dayGridMonth',
    	locale: 'ja',
        
        dateClick: function (info) {
			// project_create_viewに移動
			const createUrl = calendarEl.dataset.createUrl;
            window.location.href = `${createUrl}?date=${info.dateStr}`;
		}
    });
    
    calendar.render();
});