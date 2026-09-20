document.addEventListener("DOMContentLoaded", function() {
    const calendarEl = document.getElementById('calendar');
	const projectsDataElement = document.getElementById('projects-data');
	const projects = JSON.parse(projectsDataElement.textContent);

    const calendar = new FullCalendar.Calendar(calendarEl, {
    	initialView: 'dayGridMonth',
    	locale: 'ja',
		events: projects,

    	headerToolbar: {
        	start: 'title',
        	end: 'today prev,next'
	    },

        
        dateClick: function (info) {
			// project_create_viewに移動
			const createUrl = calendarEl.dataset.createUrl;
            window.location.href = `${createUrl}?date=${info.dateStr}`;
		}
    });
    
    calendar.render();
});