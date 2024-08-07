document.addEventListener('DOMContentLoaded', () => {
    const counters = document.querySelectorAll('.number');
    const speed = 50; // The lower the slower

    counters.forEach(counter => {
        const updateCount = () => {
            const target = +counter.getAttribute('data-target');
            const count = +counter.innerText.replace('%', '');

            // Lower inc to slow and higher to slow
            const inc = target / speed;

            // Check if target is reached
            if (count < target) {
                // Add inc to count and output in counter
                counter.innerText = Math.ceil(count + inc) + ' %';
                // Call function every ms
                setTimeout(updateCount, 50);
            } else {
                counter.innerText = target + ' %';
            }
        };

        updateCount();
    });
});

function toggleMenu() {
    var navbar = document.getElementById("navbar");
    if (navbar.style.display === "flex") {
        navbar.style.display = "none";
    } else {
        navbar.style.display = "flex";
    }
}

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});
