export type LoginPayload = {
  email: string;
  password: string;
  tenantSlug: string;
};

export type LoginResult = {
  requiresPasswordReset?: boolean;
  redirectTo?: string;
};

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "";

export async function login(payload: LoginPayload): Promise<LoginResult> {
  const response = await fetch(`${API_BASE_URL}/auth/login`, {
    method: "POST",
    credentials: "include",
    headers: { "Content-Type": "application/json" },
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