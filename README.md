# IMC_Trading_Simulation
# 🍔 **Burger Arbitrage Bot**  
> _“Burgers, buns, lettuce, chicken — we don’t just eat them, we trade them.”_  

---

## 🌟 Overview

This repository contains a **Python trading bot** built for the IMC CMI trading challenge, where participants trade on a simulated exchange featuring synthetic products:  
- **BURGER** 🍔  
- **LETTUCE** 🥬  
- **BUN** 🍞  
- **CHICKEN** 🍗  
- **SALAD** 🥗  

The system simulates a miniature food-market exchange. Our bot capitalizes on **arbitrage opportunities** between the individual components (lettuce, bun, chicken) and the combined products (burger, salad), exploiting price discrepancies to turn a profit.

---

## 🚀 Strategies Implemented

### **1️⃣ Burger Arbitrage Strategy** 🍔

> _Main focus, core profit driver._

We observe the orderbooks for **LETTUCE**, **BUN**, **CHICKEN**, and **BURGER**, and:
- If the **sum of best ask prices** for the three components is less than the **best bid** for BURGER:  
  → **Buy** the components, **assemble** a burger, and **sell** BURGER at profit.
  
- If the **best ask** for BURGER is lower than the **sum of best bid prices** for the components:  
  → **Buy** BURGER and **disassemble/sell** the components at profit.

⚙ **Risk Management:**  
We ensure net positions stay within ±100 units, rebalancing by buying/selling extra inventory if needed.  

This mirrors the **core strategy used by the winning teams** — though we suspect our implementation lagged slightly in execution speed or had conservative risk hedging that reduced maximum profitability.

---

### **2️⃣ Salad Arbitrage Strategy** 🥗

> _Experimental — not the main profit driver._

SALAD is made of:
- **LETTUCE** 🥬  
- **CHICKEN** 🍗  

We attempted a similar arbitrage approach:
- If **LETTUCE + CHICKEN (best ask)** < **SALAD (best bid)** → **Buy components, sell salad.**
- If **SALAD (best ask)** < **LETTUCE + CHICKEN (best bid)** → **Buy salad, sell components.**

🛑 **Findings:**  
In practice, salad arbitrage **reduced profitability** — likely because it competed with or cannibalized the more profitable BURGER trades (they share chicken and lettuce!). After testing, we deprioritized this strategy.

---

## 🏗 System Design

| Product     | Components                 |
|-------------|----------------------------|
| BURGER 🍔   | BUN + LETTUCE + CHICKEN    |
| SALAD 🥗    | LETTUCE + CHICKEN          |

- **Orderbook Monitoring:**  
  Continuously fetch best bids/asks.
  
- **Arbitrage Checks:**  
  Compare combined component prices to assembled product prices.

- **Position Management:**  
  Ensure total positions per product stay within ±100 to avoid overexposure.

- **Execution:**  
  Send IOC (immediate or cancel) orders to act quickly on opportunities.

---

## ⚠ Challenges & Lessons Learned

- ⚡ **Speed Matters:**  
  Even with correct logic, code execution speed (loop time, latency) can mean the difference between winning and missing an arbitrage.

- 🛡 **Hedging Needs Balance:**  
  Too much rebalancing or hedging can eat into profits. We learned to balance position limits with efficient trade execution.

- 💡 **Salad ≠ Burger:**  
  Trying to run both burger and salad arbitrage simultaneously sometimes **reduced** net profits — the winning teams focused primarily on the burger strategy.

---

## 📦 Repository Contents

- `bot.py` → Main bot logic.
- `README.md` → This file.
- `requirements.txt` → Libraries to run the bot (if applicable).
- `student_bot.py` → Provided trading interface.

---

## 🌍 Final Thoughts

This project was an **awesome deep dive** into live trading systems, combining:
- Arbitrage math  
- Fast execution  
- Risk controls

It taught us that **strategy + speed + simplicity** often wins over trying to optimize every edge.  
Thank you IMC for the challenge! 🚀

---

### 💬 Questions or ideas?  
Feel free to open an issue or connect!

