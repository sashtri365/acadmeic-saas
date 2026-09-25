import { NextRequest, NextResponse } from "next/server";

import { resolveTenant } from "@/lib/tenant";

export function middleware(request: NextRequest) {
  const tenant = resolveTenant(request.headers.get("host") ?? "localhost");
  const requestHeaders = new Headers(request.headers);

  requestHeaders.set("x-tenant-slug", tenant.slug);
  requestHeaders.set("x-tenant-hostname", tenant.hostname);

  return NextResponse.next({ request: { headers: requestHeaders } });
}

export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico).*)"],
};