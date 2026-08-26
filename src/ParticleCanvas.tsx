import { useEffect, useRef } from 'react';

interface Particle {
  x: number;
  y: number;
  vx: number;
  vy: number;
  radius: number;
  opacity: number;
  baseOpacity: number;
  phase: number;
  speed: number;
}

export default function ParticleCanvas() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const mouseRef = useRef({ x: -1000, y: -1000 });
  const rafRef = useRef<number>(0);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let width = 0;
    let height = 0;
    const particles: Particle[] = [];
    const particleCount = 120;
    const connectionDistance = 180;
    const mouseDistance = 250;

    const resize = () => {
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
    };

    const initParticles = () => {
      particles.length = 0;
      for (let index = 0; index < particleCount; index += 1) {
        particles.push({
          x: Math.random() * width,
          y: Math.random() * height,
          vx: (Math.random() - 0.5) * 0.3,
          vy: (Math.random() - 0.5) * 0.3,
          radius: Math.random() * 1.5 + 0.5,
          opacity: Math.random() * 0.4 + 0.1,
          baseOpacity: Math.random() * 0.3 + 0.1,
          phase: Math.random() * Math.PI * 2,
          speed: Math.random() * 0.008 + 0.003,
        });
      }
    };

    const handleResize = () => {
      resize();
      initParticles();
    };

    const handleMouseMove = (event: MouseEvent) => {
      mouseRef.current.x = event.clientX;
      mouseRef.current.y = event.clientY;
    };

    const handleMouseLeave = () => {
      mouseRef.current.x = -1000;
      mouseRef.current.y = -1000;
    };

    resize();
    initParticles();
    window.addEventListener('resize', handleResize);
    window.addEventListener('mousemove', handleMouseMove, { passive: true });
    window.addEventListener('mouseleave', handleMouseLeave);

    const animate = () => {
      ctx.clearRect(0, 0, width, height);

      for (const particle of particles) {
        particle.phase += particle.speed;
        particle.x += particle.vx + Math.sin(particle.phase) * 0.2;
        particle.y += particle.vy + Math.cos(particle.phase * 0.7) * 0.15;

        if (particle.x < -10) particle.x = width + 10;
        if (particle.x > width + 10) particle.x = -10;
        if (particle.y < -10) particle.y = height + 10;
        if (particle.y > height + 10) particle.y = -10;

        const dx = mouseRef.current.x - particle.x;
        const dy = mouseRef.current.y - particle.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        let brightness = particle.baseOpacity;

        if (distance < mouseDistance) {
          brightness = particle.baseOpacity + (1 - distance / mouseDistance) * 0.5;
        }

        particle.opacity += (brightness - particle.opacity) * 0.05;
        ctx.beginPath();
        ctx.arc(particle.x, particle.y, particle.radius, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(196, 149, 106, ${particle.opacity})`;
        ctx.fill();
      }

      for (let i = 0; i < particles.length; i += 1) {
        for (let j = i + 1; j < particles.length; j += 1) {
          const dx = particles[i].x - particles[j].x;
          const dy = particles[i].y - particles[j].y;
          const distance = Math.sqrt(dx * dx + dy * dy);

          if (distance < connectionDistance) {
            const midX = (particles[i].x + particles[j].x) / 2;
            const midY = (particles[i].y + particles[j].y) / 2;
            const mouseDx = mouseRef.current.x - midX;
            const mouseDy = mouseRef.current.y - midY;
            const mouseDistanceFromLine = Math.sqrt(mouseDx * mouseDx + mouseDy * mouseDy);
            let alpha = (1 - distance / connectionDistance) * 0.08;

            if (mouseDistanceFromLine < mouseDistance * 1.5) {
              alpha += (1 - mouseDistanceFromLine / (mouseDistance * 1.5)) * 0.12;
            }

            ctx.beginPath();
            ctx.moveTo(particles[i].x, particles[i].y);
            ctx.lineTo(particles[j].x, particles[j].y);
            ctx.strokeStyle = `rgba(196, 149, 106, ${Math.min(alpha, 0.25)})`;
            ctx.lineWidth = 0.5;
            ctx.stroke();
          }
        }
      }

      rafRef.current = requestAnimationFrame(animate);
    };

    animate();

    return () => {
      cancelAnimationFrame(rafRef.current);
      window.removeEventListener('resize', handleResize);
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('mouseleave', handleMouseLeave);
    };
  }, []);

  return (
    <canvas
      ref={canvasRef}
      className="fixed inset-0 h-full w-full pointer-events-none"
      style={{ zIndex: 1 }}
    />
  );
}
