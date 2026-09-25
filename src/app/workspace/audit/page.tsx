import Link from "next/link";

import { getCurrentSession } from "@/lib/session";

export default async function AuditPage() {
  const session = await getCurrentSession();
  if (!session || !["platform_admin", "institution_admin"].includes(session.role)) return null;

  return (
    <main className="workspace-shell"><header className="workspace-header"><Link href="/workspace" className="brand-link"><span className="brand-mark" aria-hidden="true">A</span><span>CampusOS</span></Link><span className="tenant-context">/{session.tenantSlug}</span><span className="session-chip">Read only</span></header><section className="workspace-content"><p className="eyebrow accent">Security trail</p><h1>Accountability, kept visible.</h1><p className="lede">Sensitive writes are recorded server-side. This view never offers edit or delete controls.</p><div className="phase-list"><div className="phase-item"><span className="phase-number">NOW</span><div><strong>Audit API contract</strong><p>Tenant and actor scope required for every record.</p></div><span className="phase-state">Read only</span></div><div className="phase-item"><span className="phase-number">LOG</span><div><strong>Append-only storage</strong><p>Database permissions revoke updates and deletes.</p></div><span className="phase-state">Protected</span></div></div></section></main>
  );
}
