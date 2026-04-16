import { NextResponse } from 'next/server';

export async function POST(req) {
  try {
    // Read the incoming request
    const body = await req.json();
    
    // Test Response (This prevents the 500 error)
    return NextResponse.json({
      title: "Test Video",
      sd: "https://www.w3schools.com/html/mov_bbb.mp4",
      hd: "https://www.w3schools.com/html/mov_bbb.mp4",
      thumbnail: "https://via.placeholder.com/300"
    });
  } catch (error) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}
