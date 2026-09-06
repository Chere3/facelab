import type { NextConfig } from "next";

// FastAPI (facelab.serve) sigue siendo la API. Next.js hace de front y proxy.
const API = process.env.FACELAB_API ?? "http://127.0.0.1:8766";

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      { source: "/api/:path*", destination: `${API}/api/:path*` },
      { source: "/out/:path*", destination: `${API}/out/:path*` },
      { source: "/analyze", destination: `${API}/analyze` },
      { source: "/reports", destination: `${API}/reports` },
    ];
  },
  images: { unoptimized: true },
  agentRules: false,
  allowedDevOrigins: ["127.0.0.1", "localhost"],
};

export default nextConfig;
