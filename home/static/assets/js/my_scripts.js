document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('contactForm section');
    const successMessage = document.getElementById('successMessage');
    
    if (window.location.hash === '#form') {
        const formPosition = form.getBoundingClientRect().top;
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


// When click slide botton -> scroll to form
function smoothScrollToForm() {
    const targetElement = document.getElementById('contactForm section');
    if (!targetElement) return; // اگر عنصر وجود ندارد اسکرول متوقف شود
    const targetPosition = targetElement.getBoundingClientRect().top + window.pageYOffset; // محاسبه موقعیت نهایی
    const startPosition = window.pageYOffset;
    const distance = targetPosition - startPosition - 0; // کمی فاصله برای فضای بالای فرم
    const duration = 120; // مدت زمان اسکرول (میلی‌ثانیه)
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
        } else {
            window.scrollTo(0, targetPosition); // اطمینان از اینکه دقیقاً به هدف رسیده است
        }
    }

    if (Math.abs(distance) > 5) { // جلوگیری از اسکرول‌های بسیار کوچک که ممکن است ضروری نباشد
        window.requestAnimationFrame(step);
    }
}

// show fixed footer after scrolling
document.addEventListener('DOMContentLoaded', function() {
    const footer = document.querySelector('.fixed-footer');
  
    // بررسی می‌کنیم که عرض صفحه کمتر از 991px باشد
    if (window.innerWidth <= 991) {
        // رویداد اسکرول را فقط یکبار تنظیم می‌کنیم
        const onScroll = () => {
            footer.style.display = 'block'; // نمایش نوار
            window.removeEventListener('scroll', onScroll); // پس از اولین اسکرول، رویداد اسکرول حذف می‌شود
        };
  
        window.addEventListener('scroll', onScroll); // وقتی کاربر اسکرول می‌کند، نوار نمایش داده می‌شود
    }
});


// Lazy load HTML
document.addEventListener("DOMContentLoaded", function() {
    let lazySections = document.querySelectorAll(".lazy-section");
    
    let observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                let section = entry.target;
                section.classList.add("visible");
                observer.unobserve(section); // از این به بعد دیگر نیازی به مشاهده این عنصر نیست
            }
        });
    }, {
        rootMargin: "0px 0px 200px 0px"
    });

    lazySections.forEach(section => {
        observer.observe(section);
    });
});
