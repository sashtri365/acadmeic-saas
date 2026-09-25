import { headers } from "next/headers";
import { redirect } from "next/navigation";
import Link from "next/link";

import { getRoleNavigation } from "@/lib/role-navigation";
import { getCurrentSession } from "@/lib/session";
import { resolveTenant } from "@/lib/tenant";

export default async function WorkspacePage() {
  const session = await getCurrentSession();
  if (!session) {
    redirect("/login?next=/workspace");
  }

  const requestHeaders = await headers();
  const tenant = resolveTenant(requestHeaders.get("x-tenant-hostname") ?? requestHeaders.get("host") ?? "localhost");
  const navigation = getRoleNavigation(session.role);

  return (
    <main className="workspace-shell">
      <header className="workspace-header"><Link href="/" className="brand-link"><span className="brand-mark" aria-hidden="true">A</span><span>CampusOS</span></Link><span className="tenant-context">/{tenant.slug}</span><span className="session-chip">{session.displayName}</span></header>
      <section className="workspace-content"><p className="eyebrow accent">{session.role.replace("_", " ")}</p><h1>Your academic workspace.</h1><p className="lede">The navigation below is tailored for your role. Every destination still requires a server-side permission check.</p><nav className="workspace-nav" aria-label="Workspace navigation">{navigation.map((item) => <Link key={item.href} href={item.href} className="workspace-nav-item">{item.label}<span aria-hidden="true">-&gt;</span></Link>)}</nav></section>
    </main>
  );
}