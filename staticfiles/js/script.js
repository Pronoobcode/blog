document.addEventListener('DOMContentLoaded', function() {
    // Smooth scroll for anchor links
    const anchors = document.querySelectorAll('a[href^="#"]');
    anchors.forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Comment form validation (checking if the body of comment is not empty)
    const commentForm = document.querySelector('.comment-form form');
    if (commentForm) {
        commentForm.addEventListener('submit', function(e) {
            const body = commentForm.querySelector('textarea').value.trim();
            if (!body) {
                alert('Please write a comment before submitting.');
                e.preventDefault();
            }
        });
    }
});
