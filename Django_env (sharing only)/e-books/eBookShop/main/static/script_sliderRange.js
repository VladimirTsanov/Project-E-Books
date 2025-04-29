document.addEventListener('DOMContentLoaded', () => {
    // 1. Grab необходимите елементи
    const rangeMin = document.getElementById('range-min');
    const rangeMax = document.getElementById('range-max');
    const inputMin = document.getElementById('min-price-text');
    const inputMax = document.getElementById('max-price-text');
    const progress = document.querySelector('.Slider .progress');
    
    const form = document.getElementById('filter-form');
    // 2. Функция за обновяване на прогреса и синхронизация range → number
    function updateSlider() {
      let minVal = parseInt(rangeMin.value, 10);
      let maxVal = parseInt(rangeMax.value, 10);
  
      // а) Непозволяваме min да надмине max и обратно
      if (minVal > maxVal) {
        minVal = maxVal;
        rangeMin.value = minVal;
      }
      if (maxVal < minVal) {
        maxVal = minVal;
        rangeMax.value = maxVal;
      }
  
      // b) Синхронизираме числовите полета
      inputMin.value = minVal;
      inputMax.value = maxVal;
  
      // c) Пресмятаме проценти спрямо всички цени
      const totalRange = parseInt(rangeMin.max, 10) - parseInt(rangeMin.min, 10);
      const minPercent = ((minVal - parseInt(rangeMin.min, 10)) / totalRange) * 100;
      const maxPercent = ((maxVal - parseInt(rangeMax.min, 10)) / totalRange) * 100;
  
      // d) Обновяваме стила на прогрес линията
      progress.style.left  = minPercent  + '%';
      progress.style.right = (100 - maxPercent) + '%';
    }
  
    // 3. Когато движиш плъзгача → обновяваме
    rangeMin.addEventListener('input', updateSlider);
    rangeMax.addEventListener('input', updateSlider);

    rangeMin.addEventListener('change', () => {
        updateSlider();
        form.submit();
      });
      rangeMax.addEventListener('change', () => {
        updateSlider();
        form.submit();
    });
  
    // 4. Когато пишеш в числовото поле → само валидация на числото,
    //    НЯМА да местим плъзгача тук!
    function validateNumberInput(el) {
      let val = parseInt(el.value, 10);
      const min = parseInt(el.min, 10);
      const max = parseInt(el.max, 10);
      if (isNaN(val)) return;
      if (val < min) val = min;
      if (el === inputMin && val > parseInt(inputMax.value, 10)) val = parseInt(inputMax.value, 10);
      if (el === inputMax && val < parseInt(inputMin.value, 10)) val = parseInt(inputMin.value, 10);
      if (val > max) val = max;
      el.value = val;
    }
  
    inputMin.addEventListener('input', () => validateNumberInput(inputMin));
    inputMax.addEventListener('input', () => validateNumberInput(inputMax));
  
    updateSlider();
  });
  