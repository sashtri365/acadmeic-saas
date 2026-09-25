import { headers } from "next/headers";
import Link from "next/link";

import { resolveTenant } from "@/lib/tenant";
import ResetPasswordForm from "./reset-password-form";

export default async function ResetPasswordPage() {
  const requestHeaders = await headers();
  const tenant = resolveTenant(requestHeaders.get("x-tenant-hostname") ?? requestHeaders.get("host") ?? "localhost");

  return (
    <main className="auth-shell">
      <div className="auth-brand"><Link href="/" className="brand-link"><span className="brand-mark" aria-hidden="true">A</span><span>CampusOS</span></Link><span className="tenant-context">/{tenant.slug}</span></div>
      <section className="auth-layout">
        <div className="auth-intro"><p className="eyebrow accent">Required next step</p><h1>Set a new password.</h1><p className="lede">Your institution requires a password change before you can access the workspace.</p><div className="auth-rule"><span /> Tenant: <strong>{tenant.slug}</strong></div></div>
        <ResetPasswordForm tenantSlug={tenant.slug} />
      </section>
    </main>
  );
}