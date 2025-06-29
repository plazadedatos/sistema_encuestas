// app/api/imagenes/route.ts
import { NextRequest, NextResponse } from "next/server";
import path from "path";
import fs from "fs/promises";
import { v4 as uuidv4 } from "uuid";

export async function POST(req: NextRequest) {
  const formData = await req.formData();
  const file = formData.get("imagen") as File;

  if (!file) {
    return NextResponse.json({ error: "No se encontró la imagen" }, { status: 400 });
  }

  const buffer = Buffer.from(await file.arrayBuffer());
  const filename = `${uuidv4()}-${file.name}`;
  const filepath = path.join(process.cwd(), "public/uploads", filename);

  await fs.writeFile(filepath, buffer);

  const imageUrl = `/uploads/${filename}`;
  return NextResponse.json({ url: imageUrl });
}
