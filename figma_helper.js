/**
 * Figma API Helper Utility
 * Usage:
 *   node figma_helper.js
 *   node figma_helper.js "https://www.figma.com/design/YOUR_FILE_KEY/..."
 *   node figma_helper.js file YOUR_FILE_KEY
 *   node figma_helper.js node YOUR_FILE_KEY NODE_ID
 */

const FIGMA_API_KEY = process.env.FIGMA_API_KEY || "";

function cleanInput(str) {
  if (!str) return "";
  return str.replace(/^[<"'\s]+|[>"'\s]+$/g, "").trim();
}

function parseFigmaUrl(input) {
  const cleaned = cleanInput(input);
  // Match standard Figma URLs: /design/:key/ or /file/:key/
  const urlMatch = cleaned.match(/figma\.com\/(?:design|file)\/([a-zA-Z0-9_-]+)/);
  if (urlMatch) {
    const fileKey = urlMatch[1];
    // Check if node-id is present in URL
    const nodeMatch = cleaned.match(/node-id=([^&]+)/);
    const nodeId = nodeMatch ? decodeURIComponent(nodeMatch[1]).replace("-", ":") : null;
    return { fileKey, nodeId };
  }
  return { fileKey: cleaned, nodeId: null };
}

async function figmaFetch(endpoint) {
  if (!FIGMA_API_KEY) {
    throw new Error("FIGMA_API_KEY is not set. Please set the FIGMA_API_KEY environment variable or configure it in .env");
  }
  const url = `https://api.figma.com/v1/${endpoint}`;
  const response = await fetch(url, {
    headers: {
      "X-Figma-Token": FIGMA_API_KEY,
    },
  });
  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Figma API Error (${response.status}): ${errorText}`);
  }
  return response.json();
}

async function main() {
  const rawArgs = process.argv.slice(2).map(cleanInput).filter(Boolean);
  let cmd = rawArgs[0] || "me";
  let target = rawArgs[1];
  let extra = rawArgs[2];

  // If the user pasted a Figma URL directly as first argument
  if (cmd.includes("figma.com/")) {
    const parsed = parseFigmaUrl(cmd);
    target = parsed.fileKey;
    extra = parsed.nodeId;
    cmd = extra ? "node" : "file";
  }

  // Prevent user from confusing API Token with File Key
  if (target && target.startsWith("figd_")) {
    console.log("\n⚠️ Notice: You entered a Figma API Token ('figd_...') instead of a File Key.");
    console.log("Your API token is configured in your environment!");
    console.log("\nWhat is a Figma File Key?");
    console.log("When you open any project in Figma, look at the URL in your browser:");
    console.log("👉 https://www.figma.com/design/ABC123XYZ456/My-App-Design");
    console.log("The File Key is: ABC123XYZ456");
    console.log("\nTry running:");
    console.log('  node figma_helper.js "https://www.figma.com/design/ABC123XYZ456/My-App-Design"');
    console.log("  or: node figma_helper.js file ABC123XYZ456\n");
    return;
  }

  try {
    if (cmd === "me") {
      console.log("Connecting to Figma API...");
      const user = await figmaFetch("me");
      console.log("=========================================");
      console.log("✅ Authenticated Successfully!");
      console.log(`👤 Name   : ${user.handle}`);
      console.log(`📧 Email  : ${user.email}`);
      console.log(`🆔 User ID: ${user.id}`);
      console.log("=========================================");
      console.log("\nTo fetch your design from Figma, run:");
      console.log('  node figma_helper.js "PASTE_YOUR_FIGMA_FILE_URL_HERE"');
    } else if (cmd === "file") {
      if (!target) {
        throw new Error("Missing File Key! Example: node figma_helper.js file YOUR_FILE_KEY or paste the full Figma URL.");
      }
      const parsed = parseFigmaUrl(target);
      const fileKey = parsed.fileKey;

      console.log(`\n🔍 Fetching Figma File [${fileKey}]...`);
      const file = await figmaFetch(`files/${fileKey}`);
      console.log("=========================================");
      console.log(`📁 File Name    : ${file.name}`);
      console.log(`🕒 Last Modified: ${file.lastModified}`);
      console.log(`📄 Pages Count  : ${file.document.children ? file.document.children.length : 0}`);
      if (file.document.children) {
        file.document.children.forEach((page, i) => {
          console.log(`   Page ${i + 1}: "${page.name}" (ID: ${page.id})`);
        });
      }
      console.log(`🧩 Components   : ${Object.keys(file.components || {}).length}`);
      console.log("=========================================");
      console.log("✅ File data retrieved successfully!");
    } else if (cmd === "node") {
      const parsed = parseFigmaUrl(target);
      const fileKey = parsed.fileKey;
      const nodeId = extra || parsed.nodeId;

      if (!fileKey || !nodeId) {
        throw new Error("Missing Node ID! Example: node figma_helper.js node YOUR_FILE_KEY NODE_ID");
      }

      console.log(`\n🔍 Fetching Node [${nodeId}] from File [${fileKey}]...`);
      const data = await figmaFetch(`files/${fileKey}/nodes?ids=${encodeURIComponent(nodeId)}`);
      console.log("=========================================");
      console.log("✅ Node data retrieved successfully!");
      const node = data.nodes[nodeId]?.document;
      if (node) {
        console.log(`Type: ${node.type} | Name: "${node.name}"`);
      }
    } else {
      console.log("Available commands:");
      console.log("  node figma_helper.js me");
      console.log('  node figma_helper.js "https://www.figma.com/design/YOUR_KEY/..."');
      console.log("  node figma_helper.js file YOUR_FILE_KEY");
      console.log("  node figma_helper.js node YOUR_FILE_KEY NODE_ID");
    }
  } catch (err) {
    console.error("\n❌ Error:", err.message);
  }
}

main();
