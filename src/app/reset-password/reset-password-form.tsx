"use client";

import { FormEvent, useState } from "react";

import { resetPassword } from "@/lib/auth";

export default function ResetPasswordForm({ tenantSlug }: { tenantSlug: string }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmation, setConfirmation] = useState("");
  const [state, setState] = useState<"idle" | "submitting" | "invalid" | "unavailable" | "complete">("idle");

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (password.length < 12 || password !== confirmation) {
      setState("invalid");
      return;
    }

    setState("submitting");
    try {
      await resetPassword({ email, password, tenantSlug });
      setState("complete");
    } catch (error) {
      setState(error instanceof Error && error.message === "RESET_INVALID" ? "invalid" : "unavailable");
    }
  }

  const message = state === "invalid" ? "Use at least 12 characters and make both passwords match." : state === "unavailable" ? "Password reset is temporarily unavailable." : state === "complete" ? "Password updated. You can now sign in." : "";

  return (
    <form className="auth-card" onSubmit={handleSubmit}>
      <div className="auth-card-heading"><p className="eyebrow">Password reset</p><h2>Create a new password</h2></div>
      <label className="field-label" htmlFor="reset-email">Account email</label><input className="field-input" id="reset-email" type="email" autoComplete="username" value={email} onChange={(event) => setEmail(event.target.value)} required />
      <label className="field-label" htmlFor="new-password">New password</label><input className="field-input" id="new-password" type="password" autoComplete="new-password" minLength={12} value={password} onChange={(event) => setPassword(event.target.value)} required />
      <label className="field-label" htmlFor="confirm-password">Confirm password</label><input className="field-input" id="confirm-password" type="password" autoComplete="new-password" minLength={12} value={confirmation} onChange={(event) => setConfirmation(event.target.value)} required />
      {message && <p className={`form-message ${state === "complete" ? "form-message-info" : ""}`} role="alert">{message}</p>}
      <button className="primary-action auth-submit" type="submit" disabled={state === "submitting" || state === "complete"}>{state === "submitting" ? "Updating..." : state === "complete" ? "Password updated" : "Update password"}<span aria-hidden="true">-&gt;</span></button>
      <p className="auth-disclaimer">Password rules are enforced again by the institution server.</p>
    </form>
  );
}