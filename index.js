import express from "express";
import fetch from "node-fetch";
import * as cheerio from "cheerio";

const app = express();
app.use(express.json());

const CASES = [
  { name: "Revolution Case", url: "https://steamcommunity.com/market/listings/730/Revolution%20Case" },
  { name: "Kilowatt Case", url: "https://steamcommunity.com/market/listings/730/Kilowatt%20Case" },
  { name: "Recoil Case", url: "https://steamcommunity.com/market/listings/730/Recoil%20Case" },
  { name: "Dreams & Nightmares Case", url: "https://steamcommunity.com/market/listings/730/Dreams%20%26%20Nightmares%20Case" },
  { name: "Snakebite Case", url: "https://steamcommunity.com/market/listings/730/Snakebite%20Case" },
  { name: "Operation Broken Fang Case", url: "https://steamcommunity.com/market/listings/730/Operation%20Broken%20Fang%20Case" },
  { name: "Fracture Case", url: "https://steamcommunity.com/market/listings/730/Fracture%20Case" },
  { name: "Prisma Case", url: "https://steamcommunity.com/market/listings/730/Prisma%20Case" },
  { name: "Prisma 2 Case", url: "https://steamcommunity.com/market/listings/730/Prisma%202%20Case" },
  { name: "Horizon Case", url: "https://steamcommunity.com/market/listings/730/Horizon%20Case" },
  { name: "Danger Zone Case", url: "https://steamcommunity.com/market/listings/730/Danger%20Zone%20Case" },
  { name: "Clutch Case", url: "https://steamcommunity.com/market/listings/730/Clutch%20Case" },
  { name: "Spectrum Case", url: "https://steamcommunity.com/market/listings/730/Spectrum%20Case" },
  { name: "Spectrum 2 Case", url: "https://steamcommunity.com/market/listings/730/Spectrum%202%20Case" },
  { name: "Glove Case", url: "https://steamcommunity.com/market/listings/730/Glove%20Case" },
  { name: "Chroma Case", url: "https://steamcommunity.com/market/listings/730/Chroma%20Case" },
  { name: "Chroma 2 Case", url: "https://steamcommunity.com/market/listings/730/Chroma%202%20Case" },
  { name: "Chroma 3 Case", url: "https://steamcommunity.com/market/listings/730/Chroma%203%20Case" },
  { name: "Falchion Case", url: "https://steamcommunity.com/market/listings/730/Falchion%20Case" },
  { name: "Gamma Case", url: "https://steamcommunity.com/market/listings/730/Gamma%20Case" },
  { name: "Gamma 2 Case", url: "https://steamcommunity.com/market/listings/730/Gamma%202%20Case" },
  { name: "Shadow Case", url: "https://steamcommunity.com/market/listings/730/Shadow%20Case" },
  { name: "Huntsman Weapon Case", url: "https://steamcommunity.com/market/listings/730/Huntsman%20Weapon%20Case" },
  { name: "Operation Phoenix Weapon Case", url: "https://steamcommunity.com/market/listings/730/Operation%20Phoenix%20Weapon%20Case" },
  { name: "Operation Breakout Weapon Case", url: "https://steamcommunity.com/market/listings/730/Operation%20Breakout%20Weapon%20Case" },
  { name: "Operation Wildfire Case", url: "https://steamcommunity.com/market/listings/730/Operation%20Wildfire%20Case" },
  { name: "Operation Hydra Case", url: "https://steamcommunity.com/market/listings/730/Operation%20Hydra%20Case" },
  { name: "Operation Vanguard Weapon Case", url: "https://steamcommunity.com/market/listings/730/Operation%20Vanguard%20Weapon%20Case" },
  { name: "Operation Bravo Case", url: "https://steamcommunity.com/market/listings/730/Operation%20Bravo%20Case" },
  { name: "CS20 Case", url: "https://steamcommunity.com/market/listings/730/CS20%20Case" },
  { name: "CS:GO Weapon Case", url: "https://steamcommunity.com/market/listings/730/CS%3AGO%20Weapon%20Case" },
  { name: "CS:GO Weapon Case 2", url: "https://steamcommunity.com/market/listings/730/CS%3AGO%20Weapon%20Case%202" },
  { name: "CS:GO Weapon Case 3", url: "https://steamcommunity.com/market/listings/730/CS%3AGO%20Weapon%20Case%203" },
  { name: "Winter Offensive Weapon Case", url: "https://steamcommunity.com/market/listings/730/Winter%20Offensive%20Weapon%20Case" },
  { name: "Revolver Case", url: "https://steamcommunity.com/market/listings/730/Revolver%20Case" },
  { name: "Gallery Case", url: "https://steamcommunity.com/market/listings/730/Gallery%20Case" },
  { name: "Sealed Genesis Terminal", url: "https://steamcommunity.com/market/listings/730/Sealed%20Genesis%20Terminal" },
  { name: "Fever Case", url: "https://steamcommunity.com/market/listings/730/Fever%20Case" },
  { name: "X-Ray P250 Package", url: "https://steamcommunity.com/market/listings/730/X-Ray%20P250%20Package" },
  { name: "eSports 2013 Case", url: "https://steamcommunity.com/market/listings/730/eSports%202013%20Case" },
  { name: "eSports 2013 Winter Case", url: "https://steamcommunity.com/market/listings/730/eSports%202013%20Winter%20Case" },
  { name: "eSports 2014 Summer Case", url: "https://steamcommunity.com/market/listings/730/eSports%202014%20Summer%20Case" }
];

async function scrapeSteam(url) {
  const html = await fetch(url).then(r => r.text());
  const $ = cheerio.load(html);

  const priceText = $("#market_commodity_order_quantity span.market_commodity_orders_header_promote").text() ||
                    $(".market_commodity_orders_header span").text();

  let price = "N/A";
  const match = priceText.match(/\$([0-9]+\.[0-9]+)/);

  if (match) price = parseFloat(match[1]);

  const listingsText = $("#market_commodity_order_quantity .market_commodity_orders_header_qty").text();
  const listings = parseInt(listingsText.replace(/\D/g, "")) || null;

  return { price, listings };
}

app.get("/cases", async (req, res) => {
  const output = [];

  for (const c of CASES) {
    const data = await scrapeSteam(c.url);
    output.push({
      name: c.name,
      price: data.price,
      listings: data.listings
    });
  }

  res.json({
    updated: Date.now(),
    cases: output
  });
});

app.listen(3000, () => console.log("Scraper funcionando en Railway"));
