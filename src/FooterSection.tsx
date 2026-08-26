const domains = ['c-eco.io', 'c-eco.org', 'hasse.foundation'];

export default function FooterSection() {
  return (
    <footer className="relative z-[2] border-t border-ceco-border2 bg-ceco-bg px-6 py-10">
      <div className="mx-auto max-w-7xl">
        <div className="grid gap-8 md:grid-cols-[1fr_auto] md:items-end">
          <div>
            <div className="font-display text-3xl text-ceco-text">c-ECO operational platform</div>
            <div className="mt-3 flex flex-wrap gap-3 font-mono-data text-[11px] uppercase tracking-[0.16em] text-ceco-text3">
              <span>System status: monitored</span>
              <span className="text-ceco-amber">TFP v1.1</span>
              <span>ScrollTrigger active</span>
            </div>
          </div>

          <div className="flex flex-wrap gap-3">
            {domains.map((domain) => (
              <a
                key={domain}
                href={`https://${domain}`}
                className="border border-ceco-border px-3 py-2 font-mono-data text-[11px] text-ceco-text2 transition-colors hover:border-ceco-amber hover:text-ceco-amber"
              >
                {domain}
              </a>
            ))}
          </div>
        </div>
      </div>
    </footer>
  );
}
