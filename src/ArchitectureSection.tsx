const layers = [
  ['01', 'Doctrinal', 'Systemic Governance Statute, legal principles, and threshold obligations.'],
  ['02', 'Institutional', 'Roles, mandates, custodians, auditors, and escalation authority.'],
  ['03', 'Operational', 'Alert bands, activation pathways, response protocols, and audit trails.'],
  ['04', 'Data', 'Indicators, confidence models, provenance, calibration, and verification.'],
  ['05', 'Technical', 'APIs, telemetry, dashboards, event logs, and execution infrastructure.'],
];

export default function ArchitectureSection() {
  return (
    <section id="architecture" className="section-shell">
      <div className="section-inner">
        <div className="reveal mb-10 max-w-4xl">
          <span className="font-mono-data text-[11px] uppercase tracking-[0.28em] text-ceco-amber">
            Governance stack
          </span>
          <h2 className="mt-4 font-display text-display-md text-ceco-text">
            Five layers keep doctrine, evidence, and execution aligned.
          </h2>
        </div>

        <div className="grid gap-4">
          {layers.map(([number, title, body]) => (
            <div key={number} className="reveal panel grid gap-4 p-5 md:grid-cols-[96px_220px_1fr] md:p-7">
              <div className="font-mono-data text-sm text-ceco-amber">{number}</div>
              <div className="font-display text-3xl text-ceco-text">{title}</div>
              <p className="leading-7 text-ceco-text2">{body}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
