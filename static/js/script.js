document.addEventListener('DOMContentLoaded', () => {
    // Create twinkling stars
    const starCount = 100;
    const body = document.body;

    for (let i = 0; i < starCount; i++) {
        const star = document.createElement('div');
        star.className = 'star';

        // Random position
        const x = Math.random() * 100;
        const y = Math.random() * 100;

        // Random size
        const size = Math.random() * 3;

        // Random animation duration
        const duration = 2 + Math.random() * 4;
        const delay = Math.random() * 5;

        star.style.left = `${x}%`;
        star.style.top = `${y}%`;
        star.style.width = `${size}px`;
        star.style.height = `${size}px`;
        star.style.setProperty('--duration', `${duration}s`);
        star.style.animationDelay = `${delay}s`;

        body.appendChild(star);
    }

    // Add a subtle mouse-follow glow effect
    body.addEventListener('mousemove', (e) => {
        const glow = document.getElementById('mouse-glow');
        if (glow) {
            glow.style.left = e.clientX + 'px';
            glow.style.top = e.clientY + 'px';
        }
    });
});
