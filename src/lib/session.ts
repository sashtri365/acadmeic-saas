import { cookies } from "next/headers";

export type UserRole = "platform_admin" | "institution_admin" | "teacher" | "student_parent";

export type CurrentSession = {
  userId: string;
  displayName: string;
  role: UserRole;
  tenantSlug: string;
};

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "";

export async function getCurrentSession(): Promise<CurrentSession | null> {
  const cookieHeader = (await cookies()).toString();
  const response = await fetch(`${API_BASE_URL}/auth/session`, {
    headers: { Cookie: cookieHeader },
    cache: "no-store",
  });

  if (response.status === 401) {
    return null;
  }

  if (!response.ok) {
    throw new Error("SESSION_UNAVAILABLE");
  }

  return response.json() as Promise<CurrentSession>;
}