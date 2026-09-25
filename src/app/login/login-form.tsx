"use client";

import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";

import { login, requestPasswordReset } from "@/lib/auth";

type LoginFormProps = { tenantSlug: string };
type FormState = "idle" | "submitting" | "invalid" | "unavailable" | "reset" | "reset-requested" | "reset-unavailable";

export default function LoginForm({ tenantSlug }: LoginFormProps) {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [formState, setFormState] = useState<FormState>("idle");

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setFormState("submitting");

    try {
      const result = await login({ email, password, tenantSlug });
      if (result.requiresPasswordReset) {
        router.push(`/reset-password?email=${encodeURIComponent(email)}`);
        return;
      }

      setFormState("idle");

      if (result.redirectTo) {
        window.location.assign(result.redirectTo);
      }
    } catch (error) {
      setFormState(error instanceof Error && error.message === "INVALID_CREDENTIALS" ? "invalid" : "unavailable");
    }
  }

  async function handleForgotPassword() {
    if (!email) {
      setFormState("reset-unavailable");
      return;
    }

    setFormState("submitting");
    try {
      await requestPasswordReset(email, tenantSlug);
      setFormState("reset-requested");
    } catch {
      setFormState("reset-unavailable");
    }
  }

  const message = formState === "invalid"
    ? "The email or password is not correct."
    : formState === "unavailable"
      ? "Sign-in is temporarily unavailable. Try again shortly."
      : formState === "reset-requested"
        ? "If this account exists, reset instructions are on their way."
        : formState === "reset-unavailable"
          ? "Enter your email first, then try password recovery again."
        : "";

  return (
    <form className="auth-card" onSubmit={handleSubmit}>
      <div className="auth-card-heading"><p className="eyebrow">Institution login</p><h2>Sign in</h2></div>
      <label className="field-label" htmlFor="email">Work or school email</label>
      <input className="field-input" id="email" type="email" autoComplete="username" value={email} onChange={(event) => setEmail(event.target.value)} required />
      <label className="field-label" htmlFor="password">Password</label>
      <input className="field-input" id="password" type="password" autoComplete="current-password" value={password} onChange={(event) => setPassword(event.target.value)} required />
      <div className="auth-options"><label className="remember-option"><input type="checkbox" /> Keep me signed in</label><button className="forgot-link" type="button" onClick={handleForgotPassword}>Forgot password?</button></div>
      {message && <p className={`form-message ${formState === "reset-requested" ? "form-message-info" : ""}`} role="alert">{message}</p>}
      <button className="primary-action auth-submit" type="submit" disabled={formState === "submitting"}>{formState === "submitting" ? "Checking access..." : "Sign in"}<span aria-hidden="true">-&gt;</span></button>
      <p className="auth-disclaimer">Access is verified by the institution server. This page never decides your role or permissions.</p>
    </form>
  );
}