const infrastructure = ['Hydrological sensing', 'Satellite observation', 'Tailings risk telemetry', 'Community verification'];

export default function AmazonLabSection() {
  return (
    <section id="amazon" className="section-shell">
      <div className="section-inner">
        <div className="reveal mb-10 max-w-4xl">
          <span className="font-mono-data text-[11px] uppercase tracking-[0.28em] text-ceco-amber">
            Amazon Living Lab
          </span>
          <h2 className="mt-4 font-display text-display-md text-ceco-text">
            A living laboratory for threshold governance in the Amazon basin.
          </h2>
        </div>

        <div className="grid gap-6 lg:grid-cols-[1.1fr_0.9fr]">
          <div className="reveal panel p-8">
            <div className="font-mono-data text-xs uppercase tracking-[0.24em] text-ceco-text3">Brumadinho case study</div>
            <p className="mt-5 text-lg leading-8 text-ceco-text2">
              Brumadinho is treated as a canonical failure of pre-threshold governance: warnings existed before the
              collapse, but operational authority did not shift fast enough. The Amazon Living Lab tests how TFP v1.1
              can turn monitored signals into reversible, auditable interventions before catastrophic lock-in.
            </p>
          </div>

          <div className="grid gap-4">
            {infrastructure.map((item, index) => (
              <div key={item} className="reveal panel flex items-center gap-4 p-5">
                <span className="font-mono-data text-xs text-ceco-amber">S{index + 1}</span>
                <span className="text-ceco-text">{item}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
