import { headers } from "next/headers";
import Link from "next/link";

import { resolveTenant } from "@/lib/tenant";
import LoginForm from "./login-form";

export default async function LoginPage() {
  const requestHeaders = await headers();
  const tenant = resolveTenant(requestHeaders.get("x-tenant-hostname") ?? requestHeaders.get("host") ?? "localhost");

  return (
    <main className="auth-shell">
      <div className="auth-brand">
        <Link href="/" className="brand-link"><span className="brand-mark" aria-hidden="true">A</span><span>CampusOS</span></Link>
        <span className="tenant-context">/{tenant.slug}</span>
      </div>
      <section className="auth-layout">
        <div className="auth-intro">
          <p className="eyebrow accent">Secure access</p>
          <h1>Welcome back to your campus.</h1>
          <p className="lede">Sign in to continue to your institution&apos;s academic workspace.</p>
          <div className="auth-rule"><span /> Tenant: <strong>{tenant.slug}</strong></div>
        </div>
        <LoginForm tenantSlug={tenant.slug} />
      </section>
    </main>
  );
}