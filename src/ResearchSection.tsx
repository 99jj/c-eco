const references = [
  ['Level I', 'Systemic Governance Statute'],
  ['Level I', 'Threshold Function Protocol v1.1'],
  ['Level I', 'Model Law for Pre-threshold Ecological Governance'],
  ['Level I', 'International Emergency Exchange Protocol'],
  ['Level II', 'UNDRR Global Assessment Report'],
  ['Level II', 'IPCC Sixth Assessment Report'],
  ['Level II', 'Stockholm Resilience Centre planetary boundaries'],
  ['Level II', 'UNIDROIT principles and secured transactions references'],
];

export default function ResearchSection() {
  return (
    <section id="research" className="section-shell">
      <div className="section-inner">
        <div className="reveal mb-10 max-w-4xl">
          <span className="font-mono-data text-[11px] uppercase tracking-[0.28em] text-ceco-amber">
            Publications
          </span>
          <h2 className="mt-4 font-display text-display-md text-ceco-text">
            Research references connect the platform to doctrine and external authority.
          </h2>
        </div>

        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          {references.map(([level, title]) => (
            <article key={title} className="reveal panel min-h-44 p-5">
              <div className="font-mono-data text-[11px] uppercase tracking-[0.18em] text-ceco-amber">{level}</div>
              <h3 className="mt-5 font-display text-2xl leading-7 text-ceco-text">{title}</h3>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}
