import { Menu, X } from 'lucide-react';
import { useEffect, useState } from 'react';

const navItems = [
  { label: 'Platform', href: '#platform' },
  { label: 'TFP', href: '#tfp' },
  { label: 'Alerts', href: '#alerts' },
  { label: 'Amazon', href: '#amazon' },
  { label: 'Architecture', href: '#architecture' },
  { label: 'Research', href: '#research' },
];

export default function Navigation() {
  const [scrolled, setScrolled] = useState(false);
  const [activeSection, setActiveSection] = useState('#platform');
  const [mobileOpen, setMobileOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 80);

      const current = navItems.reduce(
        (closest, item) => {
          const element = document.querySelector(item.href);
          if (!element) return closest;
          const top = element.getBoundingClientRect().top;
          return top <= 160 && top > closest.top ? { id: item.href, top } : closest;
        },
        { id: '#platform', top: -Infinity },
      );

      setActiveSection(current.id);
    };

    handleScroll();
    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const handleClick = (event: React.MouseEvent<HTMLAnchorElement>, href: string) => {
    event.preventDefault();
    setMobileOpen(false);
    const element = document.querySelector(href);
    if (!element) return;
    const top = element.getBoundingClientRect().top + window.scrollY - 76;
    window.scrollTo({ top, behavior: 'smooth' });
  };

  return (
    <nav
      className={`fixed left-0 top-0 z-50 w-full transition-all duration-700 ${
        scrolled ? 'border-b border-ceco-border2 bg-ceco-bg/90 backdrop-blur-md' : 'bg-transparent'
      }`}
    >
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-6 lg:px-8">
        <a
          href="#platform"
          onClick={(event) => handleClick(event, '#platform')}
          className="group flex items-center gap-3"
        >
          <div className="flex h-8 w-8 items-center justify-center rounded-full border border-ceco-amber/40 transition-colors duration-500 group-hover:border-ceco-amber">
            <span className="font-display text-xs text-ceco-amber">c</span>
          </div>
          <div className="hidden sm:block">
            <div className="font-display text-sm tracking-wide text-ceco-text">c-ECO.IO</div>
            <div className="-mt-0.5 text-[10px] uppercase tracking-[0.2em] text-ceco-text3">
              Operational Governance Platform
            </div>
          </div>
        </a>

        <div className="hidden items-center gap-1 lg:flex">
          {navItems.map((item) => (
            <a
              key={item.href}
              href={item.href}
              onClick={(event) => handleClick(event, item.href)}
              className={`relative px-3 py-1.5 text-[11px] uppercase tracking-[0.15em] transition-colors duration-300 ${
                activeSection === item.href ? 'text-ceco-amber' : 'text-ceco-text2 hover:text-ceco-text'
              }`}
            >
              {item.label}
              {activeSection === item.href && (
                <span className="absolute bottom-0 left-1/2 h-1 w-1 -translate-x-1/2 rounded-full bg-ceco-amber" />
              )}
            </a>
          ))}
        </div>

        <button
          type="button"
          aria-label="Toggle navigation"
          onClick={() => setMobileOpen((open) => !open)}
          className="rounded-sm p-2 text-ceco-text2 transition-colors hover:text-ceco-text lg:hidden"
        >
          {mobileOpen ? <X size={20} strokeWidth={1.5} /> : <Menu size={20} strokeWidth={1.5} />}
        </button>
      </div>

      {mobileOpen && (
        <div className="border-t border-ceco-border2 bg-ceco-bg/95 px-6 pb-6 pt-4 backdrop-blur-md lg:hidden">
          {navItems.map((item) => (
            <a
              key={item.href}
              href={item.href}
              onClick={(event) => handleClick(event, item.href)}
              className={`block py-3 text-sm uppercase tracking-[0.12em] transition-colors ${
                activeSection === item.href ? 'text-ceco-amber' : 'text-ceco-text2'
              }`}
            >
              {item.label}
            </a>
          ))}
        </div>
      )}
    </nav>
  );
}
