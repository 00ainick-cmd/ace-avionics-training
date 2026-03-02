
        // High-performance 3D tilt tracking using requestAnimationFrame
        document.querySelectorAll('.holo-card').forEach(card => {
            let rafId;
            let currentX = 0;
            let currentY = 0;
            let targetX = 0;
            let targetY = 0;
            const ease = 0.1; // Smoothness factor

            // Limit max rotation degrees
            const maxRot = card.classList.contains('card-campaign') ? 6 : 8;

            function animate() {
                // Ease interpolation
                currentX += (targetX - currentX) * ease;
                currentY += (targetY - currentY) * ease;

                // Calculate rotation (inverted so it tilts towards mouse)
                const rotateX = currentY * maxRot;
                const rotateY = currentX * -maxRot;

                card.style.transform = \`perspective(1000px) rotateX(\${rotateX}deg) rotateY(\${rotateY}deg) scale3d(1.02, 1.02, 1.02)\`;
                
                rafId = requestAnimationFrame(animate);
            }

            card.addEventListener('mouseenter', () => {
                cancelAnimationFrame(rafId);
                animate();
            });

            card.addEventListener('mousemove', e => {
                const rect = card.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                
                const centerX = rect.width / 2;
                const centerY = rect.height / 2;
                
                // Normalize to -1 to 1 range
                targetX = (x - centerX) / centerX;
                targetY = (y - centerY) / centerY;
            });
            
            card.addEventListener('mouseleave', () => {
                cancelAnimationFrame(rafId);
                // Return to flat state smoothly
                card.style.transform = \`perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)\`;
                targetX = 0;
                targetY = 0;
                currentX = 0;
                currentY = 0;
            });
        });
    