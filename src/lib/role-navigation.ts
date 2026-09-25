import type { UserRole } from "./session";

export type NavigationItem = {
  label: string;
  href: string;
};

const NAVIGATION: Record<UserRole, NavigationItem[]> = {
  platform_admin: [{ label: "Institutions", href: "/workspace/institutions" }, { label: "Audit", href: "/workspace/audit" }],
  institution_admin: [{ label: "People", href: "/workspace/people" }, { label: "Academics", href: "/workspace/academics" }],
  teacher: [{ label: "Classes", href: "/workspace/classes" }, { label: "Attendance", href: "/workspace/attendance" }],
  student_parent: [{ label: "Overview", href: "/workspace" }, { label: "Results", href: "/workspace/results" }],
};

export function getRoleNavigation(role: UserRole): NavigationItem[] {
  return NAVIGATION[role];
}