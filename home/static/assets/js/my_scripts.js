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


// Main function to load all lazy resources after scroll
function loadAllLazyResources() {
    loadLazyCSS(); // Load CSS
    loadLazyJS();  // Load JS
    lazyLoadHTMLSections(); // Load HTML sections
    lazyLoadBackgroundImages(); // Load background images
    lazyLoadFAQImages(); // Load FAQ background images
    showFooterAfterScroll(); // Show footer after scroll
}

// When clicking the slide button -> scroll to form
function smoothScrollToForm(event) {
    // Prevent the default anchor behavior
    event.preventDefault();

    // First, load all lazy resources
    loadAllLazyResources();

    // Then, perform smooth scroll to the form
    const isMobile = window.innerWidth < 768; // Detect mobile or desktop
    const targetElement = isMobile
        ? document.getElementById('contactForm_Form') // Mobile target
        : document.querySelector(event.target.getAttribute('data-target')); // Desktop target

    if (!targetElement) return; // Stop if target element doesn't exist

    const headerOffset = isMobile ? 220 : 0; // Offset for mobile
    const targetPosition = targetElement.getBoundingClientRect().top + window.pageYOffset - headerOffset;
    const startPosition = window.pageYOffset;
    const distance = targetPosition - startPosition;
    const duration = 120; // Duration for smooth scrolling
    let start = null;

    // Smooth scroll function
    function step(timestamp) {
        if (!start) start = timestamp;
        const progress = timestamp - start;
        const percentage = Math.min(progress / duration, 1);
        const easeInQuad = percentage * percentage; // Ease-in for smoother scroll
        window.scrollTo(0, startPosition + distance * easeInQuad);

        if (progress < duration) {
            window.requestAnimationFrame(step);
        } else {
            window.scrollTo(0, targetPosition); // Ensure precise end scroll
        }
    }

    if (Math.abs(distance) > 5) { // Avoid tiny scrolls
        window.requestAnimationFrame(step);
    }
}


// DOMContentLoaded Event
document.addEventListener('DOMContentLoaded', function () {
    let lazyCSSLoaded = false;
    let lazyJSLoaded = false;

    // Show fixed footer after first scroll
    const showFooterAfterScroll = () => {
        const footer = document.querySelector('.fixed-footer');
        if (!footer) return;

        if (window.innerWidth <= 991) { // Check if screen width is less than 991px
            footer.style.display = 'block'; // Show footer
        }
    };

    // Lazy load HTML sections using IntersectionObserver
    const lazyLoadHTMLSections = () => {
        let lazySections = document.querySelectorAll(".lazy-section");
        if (!lazySections.length) return;

        let observer = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    let section = entry.target;
                    section.style.opacity = "1"; // Show section
                    observer.unobserve(section); // Stop observing after load
                }
            });
        }, {
            rootMargin: "0px 0px 200px 0px"
        });

        lazySections.forEach(section => {
            observer.observe(section); // Observe each section
        });
    };

    // Lazy load background images (for About Us, Contact Us, Services)
    const lazyLoadBackgroundImages = () => {
        const elementsToLazyLoad = document.querySelectorAll('.lazy-bg, .page-header__bg');
        if (!elementsToLazyLoad.length) return;

        if ("IntersectionObserver" in window) {
            let observer = new IntersectionObserver(function (entries, observer) {
                entries.forEach(function (entry) {
                    if (entry.isIntersecting) {
                        let element = entry.target;
                        let bgUrl = element.getAttribute("data-bg-url");
                        element.style.backgroundImage = `url(${bgUrl})`;
                        observer.unobserve(element); // Stop observing after image load
                    }
                });
            });

            elementsToLazyLoad.forEach(function (element) {
                observer.observe(element); // Observe each element
            });
        } else {
            // Fallback for older browsers without IntersectionObserver support
            elementsToLazyLoad.forEach(function (element) {
                let bgUrl = element.getAttribute("data-bg-url");
                element.style.backgroundImage = `url(${bgUrl})`;
            });
        }
    };

    // Lazy load CSS after scroll
    const loadLazyCSS = () => {
        if (lazyCSSLoaded) return;
        lazyCSSLoaded = true;

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

        stylesheets.forEach(function (href) {
            const link = document.createElement('link');
            link.rel = 'stylesheet';
            link.href = href;
            document.head.appendChild(link); // Append CSS to page
        });
    };

    // Lazy load JavaScript after scroll
    const loadLazyJS = () => {
        if (lazyJSLoaded) return;
        lazyJSLoaded = true;

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

            // Local files
            "/public/static/assets/vendors/swiper/swiper.min.js",
            "/public/static/assets/vendors/wnumb/wNumb.min.js",
            "/public/static/assets/vendors/isotope/isotope.js",
            "/public/static/assets/vendors/countdown/countdown.min.js",
            "/public/static/assets/vendors/sidebar-content/jquery-sidebar-content.js"
        ];

        scripts.forEach(function (src) {
            const script = document.createElement('script');
            script.src = src;
            script.defer = true;
            document.body.appendChild(script); // Append JS to page
        });
    };

    // Lazy load FAQ's background images
    const lazyLoadFAQImages = () => {
        const bgElements = document.querySelectorAll(".faq-one__bg");

        if (bgElements.length > 0) {
            const loadBackgroundImage = (element) => {
                const bgImageUrl = element.getAttribute("data-bg-url");
                element.style.backgroundImage = `url(${bgImageUrl})`;
            };

            const observer = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        loadBackgroundImage(entry.target);
                        observer.unobserve(entry.target); // Stop observing after image load
                    }
                });
            });

            bgElements.forEach(element => {
                observer.observe(element); // Observe each element
            });
        }
    };

    // Main function to load all lazy resources after scroll
    const loadAllLazyResources = () => {
        loadLazyCSS(); // Load CSS
        loadLazyJS();  // Load JS
        lazyLoadHTMLSections(); // Load HTML sections
        lazyLoadBackgroundImages(); // Load background images
        lazyLoadFAQImages(); // Load FAQ background images
        showFooterAfterScroll(); // Show footer after scroll
    };

    // Load all lazy resources after first scroll
    window.addEventListener('scroll', loadAllLazyResources, { once: true });

    // When click slide button -> scroll to form
    window.smoothScrollToForm = function () {
        // First, load all lazy resources
        loadAllLazyResources();

        // Then, perform smooth scroll to the form
        const isMobile = window.innerWidth < 768; // Detect mobile or desktop
        const targetElement = isMobile
            ? document.getElementById('contactForm_Form') // Mobile target
            : document.getElementById('contactForm'); // Desktop target

        if (!targetElement) return; // Stop if target element doesn't exist

        const headerOffset = isMobile ? 220 : 0; // Offset for mobile
        const targetPosition = targetElement.getBoundingClientRect().top + window.pageYOffset - headerOffset;
        const startPosition = window.pageYOffset;
        const distance = targetPosition - startPosition;
        const duration = 120; // Duration for smooth scrolling
        let start = null;

        // Smooth scroll function
        function step(timestamp) {
            if (!start) start = timestamp;
            const progress = timestamp - start;
            const percentage = Math.min(progress / duration, 1);
            const easeInQuad = percentage * percentage; // Ease-in for smoother scroll
            window.scrollTo(0, startPosition + distance * easeInQuad);

            if (progress < duration) {
                window.requestAnimationFrame(step);
            } else {
                window.scrollTo(0, targetPosition); // Ensure precise end scroll
            }
        }

        if (Math.abs(distance) > 5) { // Avoid tiny scrolls
            window.requestAnimationFrame(step);
        }
    };
});
