const rangeInput = document.querySelectorAll(".range-input input"),
priceInput = document.querySelectorAll(".price-controls input"),
range = document.querySelector(".Slider .progress");
let priceGap = (parseInt(rangeInput[1].max) - parseInt(rangeInput[0].min)) * 0.01;



function updateSlider() {
    let minVal = parseInt(rangeInput[0].value);
    let maxVal = parseInt(rangeInput[1].value);

    priceInput[0].value = minVal;
    priceInput[1].value = maxVal;

    const minPercent = ((minVal - parseInt(rangeInput[0].min)) / 
                       (parseInt(rangeInput[0].max) - parseInt(rangeInput[0].min))) * 100;
    const maxPercent = ((maxVal - parseInt(rangeInput[1].min)) / 
                       (parseInt(rangeInput[1].max) - parseInt(rangeInput[1].min))) * 100;
    
    range.style.left = minPercent + "%";
    range.style.right = (100 - maxPercent) + "%";
}

document.addEventListener('DOMContentLoaded', () => {
    const rangeMin = document.getElementById('range-min');
    const rangeMax = document.getElementById('range-max');
    const inputMin = document.getElementById('min-price-text');
    const inputMax = document.getElementById('max-price-text');
    const minLabel = document.getElementById('min-price-label');
    const maxLabel = document.getElementById('max-price-label');

    function updateSliderLabels() {
        minLabel.textContent = parseFloat(rangeMin.value).toFixed(2) + " лв.";
        maxLabel.textContent = parseFloat(rangeMax.value).toFixed(2) + " лв.";
    }

    // range -> number
    rangeMin.addEventListener('input', () => {
        inputMin.value = rangeMin.value;
        updateSliderLabels();
    });
    rangeMax.addEventListener('input', () => {
        inputMax.value = rangeMax.value;
        updateSliderLabels();
    });

    // number -> range
    inputMin.addEventListener('input', () => {
        if (parseInt(inputMin.value) <= parseInt(rangeMax.value)) {
            rangeMin.value = inputMin.value;
            updateSliderLabels();
        }
    });
    inputMax.addEventListener('input', () => {
        if (parseInt(inputMax.value) >= parseInt(rangeMin.value)) {
            rangeMax.value = inputMax.value;
            updateSliderLabels();
        }
    });

    updateSliderLabels();
});


window.addEventListener("DOMContentLoaded", updateSlider);

priceInput.forEach(input => {
    input.addEventListener("input", e => {
        let minPrice = parseInt(priceInput[0].value),
        maxPrice = parseInt(priceInput[1].value);
        
        if((maxPrice - minPrice >= priceGap) && maxPrice <= rangeInput[1].max){
            if(e.target.classList.contains("input-min") || e.target.id === "min-price-text"){
                rangeInput[0].value = minPrice;
            } else {
                rangeInput[1].value = maxPrice;
            }
            updateSlider();
        }
    });
});

rangeInput.forEach(input => {
    input.addEventListener("input", e => {
        let minVal = parseInt(rangeInput[0].value),
        maxVal = parseInt(rangeInput[1].value);
        
        if((maxVal - minVal) < priceGap){
            if(e.target === rangeInput[0]){
                rangeInput[0].value = maxVal - priceGap;
            } else {
                rangeInput[1].value = minVal + priceGap;
            }
        } else {
            updateSlider();
        }
    });
});

document.querySelectorAll('.price').forEach(span => {
    let num = parseFloat(span.textContent);
    span.textContent = num.toFixed(2);
});