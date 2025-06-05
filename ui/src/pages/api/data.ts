import { NextApiRequest, NextApiResponse } from "next";
import fs from "fs";
import path from "path";

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  const file_path = path.join(process.cwd(), "..", "cache", "webserver_cache.txt");

  try {
    const fileContent = fs.readFileSync(file_path, "utf-8");
    res.status(200).json({ webserver_url: fileContent });
  } catch (error) {
    res.status(500).json({ error: "File not found" });
  }
}
