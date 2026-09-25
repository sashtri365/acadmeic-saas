import type { UserRole } from "./session";

export type NavigationItem = {
  label: string;
  href: string;
};

const NAVIGATION: Record<UserRole, NavigationItem[]> = {
  platform_admin: [{ label: "Dashboard", href: "/workspace/dashboard" }, { label: "Audit", href: "/workspace/audit" }],
  institution_admin: [{ label: "Dashboard", href: "/workspace/dashboard" }, { label: "People", href: "/workspace/people" }, { label: "Audit", href: "/workspace/audit" }],
  teacher: [{ label: "Dashboard", href: "/workspace/dashboard" }, { label: "Classes", href: "/workspace/classes" }, { label: "Attendance", href: "/workspace/attendance" }],
  student_parent: [{ label: "Dashboard", href: "/workspace/dashboard" }, { label: "Overview", href: "/workspace" }, { label: "Results", href: "/workspace/results" }],
};

export function getRoleNavigation(role: UserRole): NavigationItem[] {
  return NAVIGATION[role];
}