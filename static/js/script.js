// Comment form validation
const commentForm = document.querySelector('.comment-form form');
if (commentForm) {
    commentForm.addEventListener('submit', function(e) {
        const body = commentForm.querySelector('textarea').value.trim();
        if (!body) {
            e.preventDefault();
            alert('Please write a comment before submitting.');
        }
    });
}

// Mobile menu toggle
const menuToggle = document.querySelector('.menu-toggle');
const mobileMenu = document.querySelector('.mobile-menu');

if (menuToggle && mobileMenu) {
    menuToggle.addEventListener('click', function() {
        mobileMenu.classList.toggle('active');
    });
}
