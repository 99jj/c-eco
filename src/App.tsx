import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { useEffect } from 'react';
import AlertSection from './AlertSection';
import AmazonLabSection from './AmazonLabSection';
import ArchitectureSection from './ArchitectureSection';
import FooterSection from './FooterSection';
import HeroSection from './HeroSection';
import Navigation from './Navigation';
import ParticleCanvas from './ParticleCanvas';
import PlatformSection from './PlatformSection';
import ResearchSection from './ResearchSection';
import TFPSection from './TFPSection';

gsap.registerPlugin(ScrollTrigger);

export default function App() {
  useEffect(() => {
    const context = gsap.context(() => {
      gsap.utils.toArray<HTMLElement>('.reveal').forEach((element, index) => {
        gsap.fromTo(
          element,
          { opacity: 0, y: 30 },
          {
            opacity: 1,
            y: 0,
            duration: 0.8,
            ease: 'power3.out',
            delay: (index % 5) * 0.05,
            scrollTrigger: {
              trigger: element,
              start: 'top 86%',
              once: true,
            },
          },
        );
      });
    });

    const refreshTimer = window.setTimeout(() => ScrollTrigger.refresh(), 300);
    return () => {
      window.clearTimeout(refreshTimer);
      context.revert();
    };
  }, []);

  return (
    <div className="relative min-h-screen overflow-x-hidden bg-ceco-bg text-ceco-text">
      <ParticleCanvas />
      <div className="grain-overlay" />
      <Navigation />
      <main>
        <HeroSection />
        <PlatformSection />
        <TFPSection />
        <AlertSection />
        <AmazonLabSection />
        <ArchitectureSection />
        <ResearchSection />
      </main>
      <FooterSection />
    </div>
  );
}
