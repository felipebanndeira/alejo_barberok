
document.addEventListener('DOMContentLoaded', () => {
    const glow = document.createElement('div');
    glow.id = 'cursor-glow';
    document.body.appendChild(glow);

    let mouseX = 0, mouseY = 0;
    let glowX = 0, glowY = 0;

    document.addEventListener('mousemove', (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;
    });

    // Smooth follow effect
    function animate() {
        glowX += (mouseX - glowX) * 0.1;
        glowY += (mouseY - glowY) * 0.1;
        
        glow.style.left = glowX + 'px';
        glow.style.top = glowY + 'px';
        
        requestAnimationFrame(animate);
    }
    
    animate();

    // Enlarge on clickable elements
    const clickables = document.querySelectorAll('button, a, input, select, .service-card, .time-slot');
    clickables.forEach(el => {
        el.addEventListener('mouseenter', () => {
            glow.style.width = '400px';
            glow.style.height = '400px';
        });
        el.addEventListener('mouseleave', () => {
            glow.style.width = '300px';
            glow.style.height = '300px';
        });
    });
});
