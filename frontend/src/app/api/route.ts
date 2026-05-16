/**
 * API Route Handler
 */

import { NextResponse } from "next/server";

export async function GET() {
  return NextResponse.json({
    status: "ok",
    version: "4.0.0",
    antigravity: "connected",
    agents: 18,
  });
}

export async function POST(request: Request) {
  const body = await request.json();
  
  // Forward to backend
  const backendUrl = process.env.BACKEND_URL || "http://localhost:8000";
  
  try {
    const response = await fetch(`${backendUrl}/api/proxy`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    
    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    return NextResponse.json(
      { error: "Backend unavailable" },
      { status: 503 }
    );
  }
}