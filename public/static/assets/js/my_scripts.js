// When click on form botton scroll to form again
document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('contactForm'); // تغییر انتخابگر
    const successMessage = document.getElementById('successMessage');
    
    if (window.location.hash === '#form') {
        const formPosition = form.getBoundingClientRect().top;
        window.scrollTo({ top: formPosition, behavior: 'instant' });

        const formErrors = document.querySelectorAll('.error');
        if (formErrors.length === 0) {
            successMessage.style.display = 'block';  
        }
    }

    if (form) { // بررسی اینکه فرم وجود دارد
        form.addEventListener('submit', function () {
            window.location.hash = '#form';  
        });
    }
});



// When click slide botton -> scroll to form
function smoothScrollToForm() {
    const isMobile = window.innerWidth < 768; // تشخیص حالت موبایل یا دسکتاپ
    const targetElement = isMobile
        ? document.getElementById('contactForm_Form') // هدف در موبایل
        : document.getElementById('contactForm'); // هدف در دسکتاپ

    if (!targetElement) return; // اگر عنصر وجود ندارد، متوقف شود

    const headerOffset = isMobile ? 220 : 0; // در موبایل فاصله از بالا، در دسکتاپ بدون فاصله
    const targetPosition = targetElement.getBoundingClientRect().top + window.pageYOffset - headerOffset; 
    const startPosition = window.pageYOffset;
    const distance = targetPosition - startPosition;
    const duration = 120; // مدت زمان اسکرول نرم
    let start = null;

    function step(timestamp) {
        if (!start) start = timestamp;
        const progress = timestamp - start;
        const percentage = Math.min(progress / duration, 1);
        
        const easeInQuad = percentage * percentage; // تابع ease-in برای حرکت نرم‌تر
        window.scrollTo(0, startPosition + distance * easeInQuad);

        if (progress < duration) {
            window.requestAnimationFrame(step);
        } else {
            window.scrollTo(0, targetPosition); // اطمینان حاصل کنید که دقیقا به هدف می‌رسد
        }
    }

    if (Math.abs(distance) > 5) { // جلوگیری از اسکرول‌های بسیار کوچک
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
                section.style.opacity = "1"; // تنظیم مقدار opacity برای نمایش بخش
                observer.unobserve(section);
            }
        });
    }, {
        rootMargin: "0px 0px 200px 0px"
    });

    lazySections.forEach(section => {
        observer.observe(section);
    });
});

