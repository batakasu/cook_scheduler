const container = document.querySelector('.card-container');
const totalForms =  document.querySelector('input[name$="-TOTAL_FORMS"]')
let button = document.getElementById('add-ingredient')

button.addEventListener("click", function() {
    const formIndex = totalForms.value;
    const template = document.getElementById('empty-ingredient-form')
    const newFormHtml = template.innerHTML.replaceAll(
        '__prefix__',
        formIndex
    );

    container.insertAdjacentHTML('beforeend', newFormHtml);
    totalForms.value = Number(totalForms.value) + 1;
})