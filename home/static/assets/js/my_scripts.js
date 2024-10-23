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


// Lazy load top-img (in about us, contact us, services)
document.addEventListener("DOMContentLoaded", function() {
    const elementsToLazyLoad = document.querySelectorAll('.lazy-bg, .page-header__bg'); // انتخاب المان‌ها با هر دو کلاس

    if ("IntersectionObserver" in window) {
        let observer = new IntersectionObserver(function(entries, observer) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    let element = entry.target;
                    let bgUrl = element.getAttribute("data-bg-url");
                    element.style.backgroundImage = `url(${bgUrl})`;
                    observer.unobserve(element); // حذف نظارت پس از لود تصویر
                }
            });
        });

        elementsToLazyLoad.forEach(function(element) {
            observer.observe(element); // نظارت بر روی هر المان
        });
    } else {
        // Fallback برای مرورگرهایی که IntersectionObserver را پشتیبانی نمی‌کنند
        elementsToLazyLoad.forEach(function(element) {
            let bgUrl = element.getAttribute("data-bg-url");
            element.style.backgroundImage = `url(${bgUrl})`;
        });
    }
});


// Lazy load CSS
document.addEventListener('DOMContentLoaded', function() {
    let lazyLoaded = false;

    const loadLazyCSS = () => {
        if (lazyLoaded) return;
        lazyLoaded = true;

        const stylesheets = [
            '/public/static/assets/css/footer.css',
            '/public/static/assets/vendors/fontawesome/css/all.min.css',
            '/public/static/assets/vendors/owl-carousel/owl.carousel.min.css',
            '/public/static/assets/vendors/owl-carousel/owl.theme.default.min.css',
            '/public/static/assets/vendors/jquery-magnific-popup/jquery.magnific-popup.css',
            '/public/static/assets/vendors/jarallax/jarallax.css',
            '/public/static/assets/vendors/odometer/odometer.min.css',
            '/public/static/assets/vendors/bxslider/jquery.bxslider.css',
            '/public/static/assets/vendors/vegas/vegas.min.css',
            '/public/static/assets/vendors/timepicker/timePicker.css',
            '/public/static/assets/vendors/bootstrap-select/css/bootstrap-select.min.css',
            '/public/static/assets/vendors/jquery-ui/jquery-ui.css',
            '/public/static/assets/vendors/reey-font/stylesheet.css',
            '/public/static/assets/vendors/tiny-slider/tiny-slider.min.css',
            '/public/static/assets/vendors/nouislider/nouislider.min.css',
            '/public/static/assets/vendors/animate/animate.min.css',
            '/public/static/assets/vendors/nouislider/nouislider.pips.css'
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

            // فایل‌های محلی شما
            "/public/static/assets/vendors/swiper/swiper.min.js",
            "/public/static/assets/vendors/wnumb/wNumb.min.js",
            "/public/static/assets/vendors/isotope/isotope.js",
            "/public/static/assets/vendors/countdown/countdown.min.js",
            "/public/static/assets/vendors/sidebar-content/jquery-sidebar-content.js"
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


// Lazy load FAQ's image (in home)
document.addEventListener("DOMContentLoaded", function() {
    const bgElements = document.querySelectorAll(".faq-one__bg");

    if (bgElements.length > 0) { // فقط اگر المان‌های faq-one__bg وجود داشته باشند
        const loadBackgroundImage = (element) => {
            const bgImageUrl = element.getAttribute("data-bg-url");
            element.style.backgroundImage = `url(${bgImageUrl})`;
        };

        const observer = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    loadBackgroundImage(entry.target);
                    observer.unobserve(entry.target); // حذف نظارت پس از لود تصویر
                }
            });
        });

        bgElements.forEach(element => {
            observer.observe(element); // نظارت بر روی هر المان
        });
    }
});

