const container = document.querySelector('.card-container');

new Sortable(container, {
    animation: 150,
    handle: '.drag-handle',

    onEnd: function (event) {
        const cards = document.querySelectorAll('.step-card');
        cards.forEach((card, index) => {
            const orderInput = card.querySelector('input[name$="-order"]')
            orderInput.value = index + 1;
        })
    }
});

const totalForms =  document.querySelector('input[name$="-TOTAL_FORMS"]')
let button = document.getElementById('add-step')

button.addEventListener("click", function() {
    const formIndex = totalForms.value;
    const template = document.getElementById('empty-step-form')
    const newFormHtml = template.innerHTML.replaceAll(
        '__prefix__',
        formIndex
    );

    container.insertAdjacentHTML('beforeend', newFormHtml);
    totalForms.value = Number(totalForms.value) + 1;
})