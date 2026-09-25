import { headers } from "next/headers";

import { resolveTenant } from "@/lib/tenant";

export default async function Home() {
  const requestHeaders = await headers();
  const tenant = resolveTenant(requestHeaders.get("x-tenant-hostname") ?? requestHeaders.get("host") ?? "localhost");

  return (
    <main className="shell">
      <header className="topbar">
        <div className="brand-mark" aria-hidden="true">A</div>
        <div>
          <p className="eyebrow">Academic operations platform</p>
          <h1>CampusOS <span className="tenant-label">/{tenant.slug}</span></h1>
        </div>
        <span className="status-pill"><span /> F2 in progress</span>
      </header>

      <section className="hero-grid">
        <div className="hero-copy">
          <p className="eyebrow accent">Foundation workspace</p>
          <h2>One calm surface for every academic day.</h2>
          <p className="lede">
            A tenant-aware foundation for institutions, teachers, students, and families.
            The workspace is being assembled phase by phase from the production blueprint.
          </p>
          <div className="hero-actions">
            <a className="primary-action" href="/login">Open workspace <span aria-hidden="true">-&gt;</span></a>
            <a className="text-action" href="/architecture.md">View architecture</a>
          </div>
        </div>
        <aside className="signal-panel" aria-label="Build status">
          <div className="panel-heading"><span>Build signal</span><strong>01 / 16</strong></div>
          <div className="signal-line"><span className="signal-dot" /><span>Frontend foundation</span><b>Active</b></div>
          <div className="progress-track"><span /></div>
          <div className="panel-foot"><span>Next checkpoint</span><strong>Tenant context</strong></div>
        </aside>
      </section>

      <section className="phase-section" aria-labelledby="phase-heading">
        <div className="section-heading">
          <div><p className="eyebrow">Delivery map</p><h3 id="phase-heading">Build in deliberate steps</h3></div>
          <span className="section-note">Frontend first, backend after validation</span>
        </div>
        <div className="phase-list">
          <div className="phase-item"><span className="phase-number">F0</span><div><strong>Setup &amp; tooling</strong><p>Next.js, Tailwind, linting, and the shared visual language.</p></div><span className="phase-state">Complete</span></div>
          <div className="phase-item"><span className="phase-number">F1</span><div><strong>Tenant-aware routing</strong><p>Subdomain resolution and institution branding context.</p></div><span className="phase-state">Complete</span></div>
          <div className="phase-item current"><span className="phase-number">F2</span><div><strong>Authentication UI</strong><p>Login, reset flow, refresh, and secure session boundaries.</p></div><span className="phase-state">Current</span></div>
        </div>
      </section>

      <footer className="footer-line"><span>Tenant isolation is a system rule, not a visual feature.</span><span>CampusOS / foundation</span></footer>
    </div>
  );
}
