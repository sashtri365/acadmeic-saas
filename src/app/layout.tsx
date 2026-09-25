import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "CampusOS | Academic operations",
  description: "A tenant-aware academic operations workspace.",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="en"><body>{children}</body></html>
  );
}
