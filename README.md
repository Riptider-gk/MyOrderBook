# Limit Order Book Matching Engine

A price-time priority matching engine, exposed over a REST API, with SQLite persistence and a benchmark suite measuring the cost of durability.

Built as a technical deep-dive for a trading-systems / technology-developer internship application, focused on components that mirror a real exchange's core: matching logic, a trade/order gateway, and persistence — the same pieces referenced in most trading-systems job descriptions (trading systems workflow, core trading system components, low-latency middleware).

## What it does

- Accepts buy/sell limit orders and matches them using **price-time priority** — the standard rule real exchanges use: best price wins, ties broken by arrival order.
- Supports **partial fills**: a single incoming order can match against multiple resting orders across several price levels in one pass.
- Persists every order and trade to SQLite, distinguishing an order's original size from its live remaining size.
- Exposes order submission and book state over a REST API (FastAPI).
- Includes a benchmark script quantifying the throughput/latency cost of durable persistence vs. pure in-memory matching.

## Architecture

```
order.py       -> Order, Trade, OrderRequest data models
orderbook.py   -> OrderBook: heap-based matching engine (the core logic)
db.py          -> SQLite persistence layer
main.py        -> FastAPI app (HTTP layer)
benchmark.py   -> throughput/latency benchmark, persist=True vs persist=False
```

## Design decisions

| Decision | Choice | Why |
|---|---|---|
| Matching algorithm | Price-time priority | Industry-standard exchange matching rule |
| Bid/ask storage | Binary heap (`heapq`) | O(log n) insert, O(1) best-price lookup — matters when every match needs "what's the best price right now" |
| Max-heap for bids | Negate prices | Python's `heapq` only provides a min-heap; negation is the standard workaround |
| Heap tie-breaking | `itertools.count()` counter | Avoids comparing non-comparable objects on price ties, and encodes time-priority for free |
| Persistence | SQLite | Zero setup, single file, real SQL — matched to a 1-day project scope, not claimed as a production choice |
| Schema | Separate `orders` / `trades` tables | Normalization — "what orders exist" and "what executed" are different questions |
| Trade execution price | Resting order's price, not incoming order's | Standard convention — the order already in the book "set" that price first |
| API layer | FastAPI over raw sockets | Faster to build under time constraints while still exercising real client-server/HTTP design |
| Persistence toggle | `OrderBook(persist=bool)` | Lightweight dependency injection — lets the benchmark isolate pure matching-engine speed from I/O cost, without two duplicate engines |

## Benchmark results

1,000 randomly generated orders (narrow price band so orders actually cross and force real matches), same order sequence run through two configurations of the same engine:

| Configuration | Throughput | Avg. latency |
|---|---|---|
| `persist=False` (pure in-memory matching) | ~2,109,000 orders/sec | ~0.47 µs/order |
| `persist=True` (with SQLite logging) | ~336 orders/sec | ~2,977 µs/order |

**The matching algorithm itself is fast — heap operations on 1,000 orders complete in well under a millisecond.** The ~6,300x slowdown with persistence enabled comes entirely from synchronous SQLite writes: each trade triggers multiple `INSERT`/`UPDATE` calls, each opening a connection and forcing a disk-durable `commit()`. This isolates the actual bottleneck in the system — not the matching logic, but I/O — which is the same bottleneck real trading infrastructure spends most of its engineering effort working around (batching, async writes, in-memory-first with async durability, etc.).

## Known limitations / deliberate scope tradeoffs

These are intentional cuts for a 1-day build, not oversights:

- **Single-threaded, single-process** — no concurrent order handling. A real matching engine would need to reason carefully about concurrent access to the order book.
- **JSON over HTTP, not a binary protocol** — real low-latency systems typically use custom binary formats (or FIX) for order gateways; JSON was a deliberate simplicity tradeoff.
- **Synchronous DB writes on the hot path** — every trade blocks on a disk commit. A production system would decouple matching from persistence (e.g. write-ahead log, async batched writes) — the benchmark above is direct evidence for why that separation matters.
- **Self-assigned order IDs** — IDs are generated in application code rather than by the database, which required care around ID collisions across restarts.

## Possible extensions

- Rewrite the matching core in C++ and compare latency against the Python version.
- Move persistence off the synchronous hot path (write-ahead log / async batched commits) and re-run the benchmark to quantify the recovered throughput.
- Add basic concurrency handling for simultaneous order submission.

## Running it

```bash
# install deps
pip install fastapi uvicorn

# run the API
uvicorn main:app --reload
# interactive docs at http://127.0.0.1:8000/docs

# run the benchmark
python3 benchmark.py
```
