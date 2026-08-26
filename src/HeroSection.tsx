const legend = [
  ['P', 'Position'],
  ['ΔV', 'Velocity'],
  ['σ', 'Uncertainty'],
  ['Lᵣ', 'Reversibility liquidity'],
];

export default function HeroSection() {
  return (
    <section id="platform" className="section-shell flex items-center pt-28">
      <div className="section-inner">
        <div className="reveal mb-8 flex items-center gap-3">
          <span className="font-mono-data text-[11px] uppercase tracking-[0.28em] text-ceco-amber">
            c-ECO systemic governance framework
          </span>
          <span className="h-px w-24 bg-ceco-amber/40" />
        </div>

        <div className="reveal max-w-5xl">
          <h1 className="font-display text-display-lg text-ceco-text">
            Operational threshold intelligence for planetary-scale governance.
          </h1>
        </div>

        <div className="reveal my-12">
          <div className="font-display text-display-xl italic text-ceco-amber drop-shadow-[0_0_45px_rgba(196,149,106,0.18)]">
            Γ = f(P, ΔV, σ, Lᵣ)
          </div>
        </div>

        <div className="grid gap-4 md:grid-cols-4">
          {legend.map(([symbol, label]) => (
            <div key={symbol} className="reveal panel p-5">
              <div className="font-mono-data text-xs uppercase tracking-[0.2em] text-ceco-text3">{label}</div>
              <div className="mt-3 font-display text-4xl italic text-ceco-text">{symbol}</div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
