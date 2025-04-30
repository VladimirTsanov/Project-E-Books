const slider = document.querySelector('.slider');
const slides = document.querySelectorAll('.slide');
const prevBtn = document.querySelector('.prev');
const nextBtn = document.querySelector('.next');


let currentIndex = 0; // Tracks the current slide index

// Function to display a specific slide based on the index
function showSlides(index) {
    if (index >= slides.length) {
        currentIndex = 0; // Reset to first slide if at the end
    } else if (index < 0) {
        currentIndex = slides.length - 1; // Go to last slide if at the beginning
    } else {
        currentIndex = index; // Otherwise, set to the provided index
    }
    slider.style.transform = `translateX(-${currentIndex * 100}%)`; // Slide transition
}

function nextSlide() {
    showSlides(currentIndex + 1);
    slider.style.transform = `translateX(-${index * 100}%)`;
}

function prevSlide() {
    showSlides(currentIndex - 1);
}

nextBtn.addEventListener('click', nextSlide);
prevBtn.addEventListener('click', prevSlide);



let slideInterval = setInterval(nextSlide, 6000);

slider.addEventListener('mouseover', () => {
    clearInterval(slideInterval);
  });
  
slider.addEventListener('mouseout', () => {
    slideInterval = setInterval(nextSlide, 6000);
  });






  
document.getElementById("kids_stories").addEventListener("click", function() {window.location.href = "http://127.0.0.1:8000/?genre=1";});
document.getElementById("foreighn_lit").addEventListener("click", function() {window.location.href = "http://127.0.0.1:8000/?genre=15";});
document.getElementById("school").addEventListener("click", function() {window.location.href = "http://127.0.0.1:8000/?genre=10";});
