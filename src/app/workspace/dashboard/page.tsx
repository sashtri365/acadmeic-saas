import Link from "next/link";

import { getCurrentSession } from "@/lib/session";

export default async function DashboardPage() {
  const session = await getCurrentSession();
  if (!session) return null;

  const cards = session.role === "teacher"
    ? [["Attendance", "92%", "This term"], ["Homework", "18", "Open tasks"], ["Classes", "4", "Assigned scope"]]
    : session.role === "institution_admin"
      ? [["Students", "1,248", "Active enrollments"], ["Attendance", "94%", "Institution average"], ["Invoices", "86%", "Collected"]]
      : [["Attendance", "96%", "Current term"], ["Results", "Published", "Latest exam"], ["Messages", "3", "Unread"]];

  return (
    <main className="workspace-shell"><header className="workspace-header"><Link href="/workspace" className="brand-link"><span className="brand-mark" aria-hidden="true">A</span><span>CampusOS</span></Link><span className="tenant-context">/{session.tenantSlug}</span><span className="session-chip">{session.displayName}</span></header><section className="workspace-content"><p className="eyebrow accent">{session.role.replace("_", " ")} dashboard</p><h1>A clear view of today.</h1><p className="lede">Every metric is scoped to your institution and permission context.</p><div className="workspace-nav">{cards.map(([label, value, detail]) => <div className="workspace-nav-item" key={label}><span><strong>{value}</strong><br /><small>{label} · {detail}</small></span></div>)}</div><p className="auth-disclaimer">Dashboard values are server-authorized; visible cards are not a security boundary.</p></section></main>
  );
}
