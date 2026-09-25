export type TenantContext = {
  slug: string;
  hostname: string;
  isLocal: boolean;
};

const RESERVED_HOSTS = new Set(["www", "app", "localhost"]);

export function resolveTenant(hostname: string): TenantContext {
  const normalizedHostname = hostname.split(":")[0].toLowerCase();
  const parts = normalizedHostname.split(".");
  const candidate = parts.length > 2 ? parts[0] : "demo";
  const slug = RESERVED_HOSTS.has(candidate) ? "demo" : candidate;

  return {
    slug,
    hostname: normalizedHostname,
    isLocal: normalizedHostname === "localhost" || normalizedHostname === "127.0.0.1",
  };
}