const pipeline = ['Observe', 'Classify', 'Validate', 'Activate', 'Audit'];

export default function PlatformSection() {
  return (
    <section className="section-shell">
      <div className="section-inner">
        <div className="reveal mb-10 max-w-3xl">
          <span className="font-mono-data text-[11px] uppercase tracking-[0.28em] text-ceco-amber">
            Recognition-Action Gap
          </span>
          <h2 className="mt-4 font-display text-display-md text-ceco-text">
            c-eco.io converts recognized systemic risk into governed activation.
          </h2>
        </div>

        <div className="grid gap-6 lg:grid-cols-[1fr_1.2fr]">
          <div className="reveal panel p-8">
            <p className="text-lg leading-8 text-ceco-text2">
              Institutions already recognize ecological and social thresholds, but operational systems still wait for
              discretionary decisions after the threshold is visible. The platform closes that gap by binding signals,
              statutes, alert bands, and execution protocols into one governed surface.
            </p>
          </div>

          <div className="grid gap-3">
            {pipeline.map((step, index) => (
              <div key={step} className="reveal panel flex items-center gap-5 p-5">
                <span className="font-mono-data text-sm text-ceco-amber">0{index + 1}</span>
                <span className="font-display text-2xl text-ceco-text">{step}</span>
                <span className="ml-auto h-px flex-1 bg-ceco-border2" />
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
