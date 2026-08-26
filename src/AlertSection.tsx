const bands = [
  ['GREEN', '#4A7A5C', 'Safe Operating Space'],
  ['AMBER', '#C4956A', 'Pre-threshold'],
  ['RED', '#B85C5C', 'Threshold breach'],
  ['BLACK', '#9A9AA0', 'Systemic cascade'],
];

export default function AlertSection() {
  return (
    <section id="alerts" className="section-shell">
      <div className="section-inner">
        <div className="reveal mb-10 max-w-4xl">
          <span className="font-mono-data text-[11px] uppercase tracking-[0.28em] text-ceco-amber">
            Alert logic
          </span>
          <h2 className="mt-4 font-display text-display-md text-ceco-text">
            Four bands translate threshold evidence into operational posture.
          </h2>
        </div>

        <div className="grid gap-4">
          {bands.map(([band, color, title]) => (
            <div key={band} className="reveal panel overflow-hidden">
              <div className="grid items-center gap-5 p-5 md:grid-cols-[180px_1fr] md:p-7">
                <div className="flex items-center gap-4">
                  <span className="h-4 w-4 rounded-full" style={{ backgroundColor: color }} />
                  <span className="font-mono-data text-sm uppercase tracking-[0.22em]" style={{ color }}>
                    {band}
                  </span>
                </div>
                <div>
                  <div className="font-display text-3xl text-ceco-text">{title}</div>
                  <div className="mt-2 h-px w-full" style={{ backgroundColor: `${color}55` }} />
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
