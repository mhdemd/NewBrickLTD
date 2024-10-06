document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('contactForm');
    const successMessage = document.getElementById('successMessage');
    
    if (window.location.hash === '#form') {
        const formPosition = form.getBoundingClientRect().top + window.pageYOffset - 200; // تغییر به -50 یا 0
        window.scrollTo({ top: formPosition, behavior: 'instant' });

        const formErrors = document.querySelectorAll('.error');
        if (formErrors.length === 0) {
            successMessage.style.display = 'block';  
        }
    }

    form.addEventListener('submit', function () {
        window.location.hash = '#form';  
    });
});



function smoothScrollToForm() {
    const targetElement = document.getElementById('contactForm');
    const targetPosition = targetElement.getBoundingClientRect().top;
    const startPosition = window.pageYOffset;
    const distance = targetPosition - 0;  // کمی فاصله برای فضای بالای فرم
    const duration = 120;  // مدت زمان اسکرول (میلی‌ثانیه)
    let start = null;

    function step(timestamp) {
        if (!start) start = timestamp;
        const progress = timestamp - start;
        const percentage = Math.min(progress / duration, 1);
        
        // تابع easeInQuad برای شروع سریع‌تر و کند شدن تدریجی
        const easeInQuad = percentage * percentage;

        window.scrollTo(0, startPosition + distance * easeInQuad);

        if (progress < duration) {
            window.requestAnimationFrame(step);
        }
    }

    window.requestAnimationFrame(step);
}

