
  (function ($) {
  
  "use strict";

    // MENU
    $('#sidebarMenu .nav-link').on('click',function(){
      $("#sidebarMenu").collapse('hide');
    });
    
    // CUSTOM LINK
    $('.smoothscroll').click(function(){
      var el = $(this).attr('href');
      var elWrapped = $(el);
      var header_height = $('.navbar').height();
  
      scrollToDiv(elWrapped,header_height);
      return false;
  
      function scrollToDiv(element,navheight){
        var offset = element.offset();
        var offsetTop = offset.top;
        var totalScroll = offsetTop-navheight;
  
        $('body,html').animate({
        scrollTop: totalScroll
        }, 300);
      }
    });
  
  })(window.jQuery);


  // Stretch navbar on scroll
  document.addEventListener("DOMContentLoaded", () => {
    const navbar = document.getElementById('navbar');
    const toggler = document.querySelector(".navbar-toggler");
    const homeSection = document.getElementById('home');

    window.addEventListener('scroll', () => {
        const homeSectionRect = homeSection.getBoundingClientRect();

        // Check if the Home section is in view
        if (homeSectionRect.top <= 0 && homeSectionRect.bottom >= 0) {
            navbar.classList.add('stretched');
            toggler.classList.remove("visible");
        } else {
            navbar.classList.remove('stretched');
            toggler.classList.add("visible");
        }
    });
});




    // Smooth scrolling for navigation links
document.querySelectorAll('.sidebar a').forEach(link => {
  link.addEventListener('click', function (e) {
    e.preventDefault(); // Prevent default anchor click behavior
    const targetId = this.getAttribute('href').substring(1); // Remove the #
    const targetSection = document.getElementById(targetId);

    // Scroll to the target section smoothly
    targetSection.scrollIntoView({
      behavior: 'smooth',
      block: 'start'
    });
  });
});

document.addEventListener('DOMContentLoaded', function () {
  const sections = document.querySelectorAll('section'); // Select all sections
  const navLinks = document.querySelectorAll('#sidebarMenu .nav-link'); // Select all nav links

  // Function to remove 'active' from all links
  const removeActiveClasses = () => {
      navLinks.forEach(link => link.classList.remove('active'));
  };

  // Function to add 'active' to the current section link
  const setActiveLink = () => {
      let currentSection = '';

      sections.forEach(section => {
          const sectionTop = section.offsetTop;
          const sectionHeight = section.offsetHeight;
          if (pageYOffset >= sectionTop - sectionHeight / 3) {
              currentSection = section.getAttribute('id'); // Get section ID
          }
      });

      removeActiveClasses();

      // Add 'active' class to the matching link
      navLinks.forEach(link => {
          if (link.getAttribute('href') === `#${currentSection}`) {
              link.classList.add('active');
          }
      });
  };

  // Run on scroll
  window.addEventListener('scroll', setActiveLink);
});

document.addEventListener("DOMContentLoaded", () => {
  const headers = document.querySelectorAll(".card-header");

  headers.forEach(header => {
      header.addEventListener("click", () => {
          const body = header.nextElementSibling;

          // Toggle the dropdown
          body.style.display = body.style.display === "block" ? "none" : "block";
          
          // Rotate the arrow indicator
          header.classList.toggle("open");
      });
  });
});
