const parameters = [
  ['P', 'Position against legally defined threshold corridors.'],
  ['ΔV', 'Rate and direction of change across monitored indicators.'],
  ['σ', 'Uncertainty envelope, confidence, dispersion, and evidentiary quality.'],
  ['Lᵣ', 'Liquidity of reversibility before harm becomes locked in.'],
];

const principles = ['Pre-threshold governance', 'Evidentiary traceability', 'Automatic proportionality', 'Reversibility first'];

export default function TFPSection() {
  return (
    <section id="tfp" className="section-shell">
      <div className="section-inner">
        <div className="reveal mb-10 max-w-4xl">
          <span className="font-mono-data text-[11px] uppercase tracking-[0.28em] text-ceco-amber">
            Threshold Function Protocol
          </span>
          <h2 className="mt-4 font-display text-display-md text-ceco-text">
            TFP v1.1 formalizes when systems must shift state.
          </h2>
        </div>

        <div className="reveal panel mb-8 p-8 lg:p-10">
          <div className="font-mono-data text-xs uppercase tracking-[0.24em] text-ceco-text3">Formula card</div>
          <div className="mt-6 font-display text-6xl italic text-ceco-amber md:text-8xl">Γ = f(P, ΔV, σ, Lᵣ)</div>
          <p className="mt-6 max-w-3xl text-ceco-text2">
            The Trigger Function aggregates threshold position, velocity, uncertainty, and reversibility liquidity into
            an activation score that governs alert bands and response obligations.
          </p>
        </div>

        <div className="grid gap-4 md:grid-cols-4">
          {parameters.map(([symbol, copy]) => (
            <div key={symbol} className="reveal panel p-5">
              <div className="font-display text-4xl italic text-ceco-text">{symbol}</div>
              <p className="mt-4 text-sm leading-6 text-ceco-text2">{copy}</p>
            </div>
          ))}
        </div>

        <div className="mt-8 grid gap-4 md:grid-cols-4">
          {principles.map((principle) => (
            <div key={principle} className="reveal border-l border-ceco-amber/50 bg-ceco-bg2/60 p-5">
              <span className="font-mono-data text-[11px] uppercase tracking-[0.18em] text-ceco-amber">{principle}</span>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
