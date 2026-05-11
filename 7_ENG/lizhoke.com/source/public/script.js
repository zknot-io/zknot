// Footer year
document.getElementById('year').textContent = new Date().getFullYear();

// Reveal on scroll
const revealEls = document.querySelectorAll(
  '.collection__head, .gallery__item, .card, .testimonial, .faq__item, .about__photos, .about__copy'
);

revealEls.forEach((el) => {
  el.style.opacity = '0';
  el.style.transform = 'translateY(20px)';
  el.style.transition = 'opacity 0.7s cubic-bezier(0.22, 1, 0.36, 1), transform 0.7s cubic-bezier(0.22, 1, 0.36, 1)';
});

const io = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'translateY(0)';
        io.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.12, rootMargin: '0px 0px -60px 0px' }
);

revealEls.forEach((el) => io.observe(el));

// Stagger gallery items within each collection
document.querySelectorAll('.gallery').forEach((gallery) => {
  gallery.querySelectorAll('.gallery__item').forEach((el, i) => {
    el.style.transitionDelay = `${Math.min(i * 70, 350)}ms`;
  });
});
