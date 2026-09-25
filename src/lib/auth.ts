export type LoginPayload = {
  email: string;
  password: string;
  tenantSlug: string;
};

export type LoginResult = {
  requiresPasswordReset?: boolean;
  redirectTo?: string;
};

export type PasswordResetPayload = {
  email: string;
  password: string;
  tenantSlug: string;
};

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "";

export async function login(payload: LoginPayload): Promise<LoginResult> {
  const response = await fetch(`${API_BASE_URL}/auth/login`, {
    method: "POST",
    credentials: "include",
    headers: { "Content-Type": "application/json", "X-Tenant-Slug": payload.tenantSlug },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    if (response.status === 401) {
      throw new Error("INVALID_CREDENTIALS");
    }

    throw new Error("AUTH_UNAVAILABLE");
  }

  return response.json() as Promise<LoginResult>;
}

export async function requestPasswordReset(email: string, tenantSlug: string): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/auth/password-reset/request`, {
    method: "POST",
    credentials: "include",
    headers: { "Content-Type": "application/json", "X-Tenant-Slug": tenantSlug },
    body: JSON.stringify({ email, tenantSlug }),
  });

  if (!response.ok) {
    throw new Error("RESET_UNAVAILABLE");
  }
}

export async function resetPassword(payload: PasswordResetPayload): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/auth/password-reset/complete`, {
    method: "POST",
    credentials: "include",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error(response.status === 400 ? "RESET_INVALID" : "RESET_UNAVAILABLE");
  }
}