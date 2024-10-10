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


// Lazy load js
document.addEventListener('DOMContentLoaded', function() {
    let lazyLoaded = false;

    const loadLazyScripts = () => {
        if (lazyLoaded) return;
        lazyLoaded = true;

        const scripts = [
            "https://cdnjs.cloudflare.com/ajax/libs/jarallax/1.12.1/jarallax.min.js",
            "https://cdnjs.cloudflare.com/ajax/libs/lettering.js/0.7.0/jquery.lettering.min.js",
            "https://cdnjs.cloudflare.com/ajax/libs/jquery-ajaxchimp/1.3.0/jquery.ajaxchimp.min.js",
            "https://cdnjs.cloudflare.com/ajax/libs/jquery.appear/0.4.1/jquery.appear.min.js",
            "https://cdnjs.cloudflare.com/ajax/libs/jquery-circle-progress/1.2.2/circle-progress.min.js",
            "https://cdnjs.cloudflare.com/ajax/libs/magnific-popup.js/1.1.0/jquery.magnific-popup.min.js",
            "https://cdnjs.cloudflare.com/ajax/libs/jquery-validate/1.19.5/jquery.validate.min.js",
            "https://cdnjs.cloudflare.com/ajax/libs/noUiSlider/14.6.3/nouislider.min.js",
            "https://cdnjs.cloudflare.com/ajax/libs/OwlCarousel2/2.3.4/owl.carousel.min.js",
            "https://cdnjs.cloudflare.com/ajax/libs/bxslider/4.2.15/jquery.bxslider.min.js",
            "https://cdnjs.cloudflare.com/ajax/libs/bootstrap-select/1.14.0-beta2/js/bootstrap-select.min.js",
            "https://cdnjs.cloudflare.com/ajax/libs/vegas/2.5.4/vegas.min.js",
            "https://cdnjs.cloudflare.com/ajax/libs/jqueryui/1.13.2/jquery-ui.min.js",
            "https://cdnjs.cloudflare.com/ajax/libs/timepicker/1.3.5/jquery.timepicker.min.js",
            

            // فایل‌های اضافه شده شما
            "{% static 'assets/vendors/swiper/swiper.min.js' %}",
            "{% static 'assets/vendors/wnumb/wNumb.min.js' %}",
            "{% static 'assets/vendors/isotope/isotope.js' %}",
            "{% static 'assets/vendors/countdown/countdown.min.js' %}",
            "{% static 'assets/vendors/sidebar-content/jquery-sidebar-content.js' %}",
            "{% static 'assets/vendors/wnumb/wNumb.min.js' %}",
            "{% static 'assets/vendors/isotope/isotope.js' %}",
            "{% static 'assets/vendors/countdown/countdown.min.js' %}",
            "{% static 'assets/vendors/sidebar-content/jquery-sidebar-content.js' %}",
            ];

        scripts.forEach(function(src) {
            const script = document.createElement('script');
            script.src = src;
            script.defer = true;
            document.body.appendChild(script);
        });
    };

    window.addEventListener('scroll', loadLazyScripts); // لود اسکریپت‌ها بعد از اولین اسکرول
});

// Lazy load CSS
document.addEventListener('DOMContentLoaded', function() {
    let lazyLoaded = false;

    const loadLazyCSS = () => {
        if (lazyLoaded) return;
        lazyLoaded = true;

        const stylesheets = [
            "{% static 'assets/vendors/owl-carousel/owl.carousel.min.css' %}",
            "{% static 'assets/vendors/owl-carousel/owl.theme.default.min.css' %}",
            "{% static 'assets/vendors/jquery-magnific-popup/jquery.magnific-popup.css' %}",
            "{% static 'assets/vendors/jarallax/jarallax.css' %}",
            "{% static 'assets/vendors/odometer/odometer.min.css' %}",
            "{% static 'assets/vendors/bxslider/jquery.bxslider.css' %}",
            "{% static 'assets/vendors/vegas/vegas.min.css' %}",
            "{% static 'assets/vendors/timepicker/timePicker.css' %}",
            "{% static 'assets/vendors/bootstrap-select/css/bootstrap-select.min.css' %}",
            "{% static 'assets/vendors/jquery-ui/jquery-ui.css' %}",
            
        ];

        stylesheets.forEach(function(href) {
            const link = document.createElement('link');
            link.rel = 'stylesheet';
            link.href = href;
            document.head.appendChild(link);
        });
    };

    // بارگذاری CSSها بعد از اولین اسکرول
    window.addEventListener('scroll', loadLazyCSS);
});
