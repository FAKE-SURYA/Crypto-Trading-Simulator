# High-Performance Crypto Trading Simulator - Implementation Plan

## 🎯 Project Overview

A resume-worthy full-stack trading simulator demonstrating:
- **C++17** performance optimization with pybind11 Python bindings
- **FastAPI** async backend with WebSocket streaming
- **React/Next.js** real-time dashboard with dark-mode UI

**Target Audience**: Senior Engineering Interviews (Full-Stack, Systems, Financial Technology)

---

## 📋 Technology Stack

### Core Engine (C++)
- **Language**: C++17
- **Build System**: CMake 3.15+
- **Python Binding**: pybind11
- **Key Algorithms**: 
  - Simple Moving Average (SMA) with O(1) updates
  - Order matching with price-time priority

### Backend (Python)
- **Framework**: FastAPI
- **Server**: Uvicorn (ASGI)
- **Real-time**: WebSockets
- **Data Generation**: NumPy (Geometric Brownian Motion)

### Frontend (JavaScript/TypeScript)
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Charts**: Recharts
- **Styling**: Tailwind CSS + Custom Dark Theme

---

## 🏗️ System Architecture

```
┌─────────────────┐
│  React Frontend │  ← WebSocket Client
│   (Next.js)     │  ← Real-time Charts
└────────┬────────┘
         │ WebSocket
         ↓
┌─────────────────┐
│  Python Backend │  ← FastAPI
│   (FastAPI)     │  ← WebSocket Server
└────────┬────────┘
         │ Python Bindings
         ↓
┌─────────────────┐
│   C++ Engine    │  ← SMA Calculator
│   (pybind11)    │  ← Order Matching
└─────────────────┘
```

**Data Flow**:
1. Mock price generator creates Bitcoin prices
2. Python passes prices to C++ for SMA calculation
3. C++ returns optimized SMA values
4. Backend broadcasts {price, sma, orderbook} via WebSocket
5. Frontend renders real-time chart updates

---

## 📁 Project Structure

```
euler/
├── PLAN.md                    # This file
├── README.md                  # Project documentation
│
├── cpp_core/                  # C++ Performance Engine
│   ├── include/
│   │   └── engine.hpp         # Class definitions
│   ├── src/
│   │   ├── engine.cpp         # SMA + OrderBook implementation
│   │   └── bindings.cpp       # pybind11 Python interface
│   ├── CMakeLists.txt         # Build configuration
│   └── setup.py               # Python packaging
│
├── backend/                   # Python FastAPI Server
│   ├── main.py                # FastAPI app + WebSocket endpoint
│   ├── market_simulator.py    # Fake price generator (GBM)
│   ├── trading_service.py     # C++ integration layer
│   └── requirements.txt       # Python dependencies
│
└── frontend/                  # React/Next.js Dashboard
    ├── app/
    │   ├── page.tsx           # Main dashboard page
    │   └── layout.tsx         # Root layout with dark theme
    ├── components/
    │   ├── PriceChart.tsx     # Real-time line chart (Recharts)
    │   ├── OrderBook.tsx      # Live order book display
    │   └── TradingPanel.tsx   # Buy/Sell order form
    ├── hooks/
    │   └── useWebSocket.ts    # WebSocket connection hook
    └── styles/
        └── globals.css        # Dark mode design tokens
```

---

## 🚀 Implementation Phases

### Phase 1: C++ Core Engine (Est. 2-3 hours)

**Deliverables**:
- [ ] `engine.hpp` - Class interfaces for `SMACalculator` and `OrderBook`
- [ ] `engine.cpp` - C++ implementation with circular buffer optimization
- [ ] `bindings.cpp` - pybind11 module exposing classes to Python
- [ ] `CMakeLists.txt` - CMake build script
- [ ] `setup.py` - Python packaging script

**Technical Details**:

**SMACalculator**:
- Uses fixed-size circular buffer for price history
- Maintains running sum for O(1) average calculation
- Avoids recalculating entire window on each update

**OrderBook**:
- Stores buy/sell orders in sorted maps (std::map)
- Matches orders when bid price ≥ ask price
- Returns executed trades with price/quantity

**Build Process**:
```bash
cd cpp_core
pip install .  # Compiles C++ and installs Python module
```

**Verification**:
```python
import trade_engine
sma = trade_engine.SMACalculator(window_size=5)
sma.add_price(100.0)
sma.add_price(102.0)
print(sma.get_sma())  # Output: 101.0
```

---

### Phase 2: Python Backend (Est. 2-3 hours)

**Deliverables**:
- [ ] FastAPI app with CORS and WebSocket support
- [ ] `/ws/market-data` WebSocket endpoint
- [ ] Mock Bitcoin price generator using Geometric Brownian Motion
- [ ] Integration with C++ `trade_engine` module
- [ ] Connection manager for multiple WebSocket clients

**Technical Details**:

**Price Generation**:
- Starting price: ~$45,000 (Bitcoin)
- Update frequency: 100-500ms
- Volatility: ~2% (realistic market movement)
- Mathematical model: `dS = μ·S·dt + σ·S·dW`

**WebSocket Message Format**:
```json
{
  "timestamp": 1234567890.123,
  "price": 45123.45,
  "sma": 45050.20,
  "orderbook": {
    "bids": [[44950, 2.5], [44900, 1.2]],
    "asks": [[45100, 1.8], [45150, 3.0]]
  }
}
```

**Running the Backend**:
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

### Phase 3: React Frontend (Est. 3-4 hours)

**Deliverables**:
- [ ] Next.js 14 app with TypeScript
- [ ] Dark mode design system (deep navy + electric blue accents)
- [ ] `PriceChart` component with dual-line chart (price + SMA)
- [ ] `OrderBook` component with color-coded bids/asks
- [ ] `TradingPanel` component for submitting orders
- [ ] `useWebSocket` hook with auto-reconnection

**Technical Details**:

**Design Aesthetics**:
- **Color Palette**: 
  - Background: `#0a0e27` (deep space navy)
  - Cards: `rgba(26, 29, 46, 0.8)` (glassmorphism)
  - Accents: `#3b82f6` (electric blue), `#10b981` (cyber green)
- **Typography**: Inter font family
- **Animations**: Smooth transitions, pulse effects for live updates

**PriceChart Features**:
- Recharts `<LineChart>` with responsive container
- Two `<Line>` components: price (blue) and SMA (gold)
- Auto-scaling axes
- Tooltips with exact values
- Rolling window of last 100 data points

**WebSocket Hook**:
```typescript
const { data, sendMessage, isConnected } = useWebSocket(
  'ws://localhost:8000/ws/market-data'
);
```

**Running the Frontend**:
```bash
cd frontend
npm install
npm run dev  # Open http://localhost:3000
```

---

## ✅ Verification & Testing

### Phase 4: Integration Testing

**End-to-End Flow Test**:
1. Start backend: `uvicorn main:app --reload`
2. Start frontend: `npm run dev`
3. Open browser to `http://localhost:3000`
4. Verify chart shows live price updates
5. Verify SMA line smoothly trails price
6. Submit buy order via TradingPanel
7. Verify order appears in OrderBook
8. Submit matching sell order
9. Verify trade executes and removes from OrderBook

**Performance Benchmarks**:
- **C++ SMA**: 10,000 price updates in <10ms
- **WebSocket Latency**: <50ms from backend to frontend (localhost)
- **Chart FPS**: Smooth 60fps with 100 data points

**Code Quality**:
- Python: `pylint backend/` (target score >8.0)
- TypeScript: `npm run lint` (zero errors)
- C++: Compile with `-Wall -Wextra` (zero warnings)

---

## 🎤 Interview Talking Points

**Systems Design**:
- "I chose C++ for the calculation engine to achieve microsecond-level performance, which is critical in high-frequency trading scenarios"
- "The circular buffer implementation reduces memory allocations and provides O(1) time complexity for SMA updates"

**Full-Stack Integration**:
- "I used pybind11 to create Python bindings, allowing seamless interoperability while maintaining C++ performance benefits"
- "The WebSocket architecture provides sub-50ms latency for real-time market data streaming"

**Production Thinking**:
- "I implemented auto-reconnection with exponential backoff to handle network failures gracefully"
- "The order matching algorithm uses price-time priority, the same mechanism used by major exchanges like NASDAQ"

**Trade-offs**:
- "I evaluated using Rust vs C++, but chose C++ for wider industry adoption and easier Python interop with pybind11"
- "For the frontend, I chose Recharts over D3.js for faster development, though D3 would offer more customization"

---

## 🛠️ Prerequisites

Before starting, ensure you have:

- [x] **C++ Compiler**: 
  - Windows: Visual Studio 2019+ or Build Tools
  - Linux: GCC 7+ or Clang 6+
  - macOS: Xcode Command Line Tools
- [x] **CMake**: Version 3.15 or higher
- [x] **Python**: Version 3.8 or higher
- [x] **Node.js**: Version 18 or higher
- [x] **pip packages**: `pip install pybind11 cmake`

**Verify Setup**:
```bash
cmake --version      # Should be 3.15+
python --version     # Should be 3.8+
node --version       # Should be 18+
gcc --version        # Or clang/MSVC
```

---

## 📚 Next Steps

Once you approve this plan, I will:

1. **Create project structure** (`cpp_core/`, `backend/`, `frontend/`)
2. **Implement C++ engine** (SMA calculator + order matching)
3. **Configure build system** (CMakeLists.txt + setup.py)
4. **Test C++ module** (verify Python imports and functionality)
5. **Build Python backend** (FastAPI + WebSocket + price generator)
6. **Create React frontend** (charts, order book, trading panel)
7. **End-to-end testing** (full system integration)
8. **Documentation** (README, architecture diagrams, setup guide)

**Estimated Total Time**: 8-12 hours of focused development

---

## 🚨 Important Notes

> [!WARNING]
> **Windows Users**: You may need to install Visual Studio Build Tools for C++ compilation. I can provide detailed setup instructions if needed.

> [!IMPORTANT]
> **Portfolio Ready**: This project includes all elements recruiters look for:
> - Complex multi-language integration
> - Performance optimization
> - Real-time systems
> - Production-quality UI/UX
> - Comprehensive testing

> [!TIP]
> **Resume Bullet Points**:
> - "Built high-performance trading simulator with C++/Python/React stack"
> - "Optimized calculation engine achieving <1ms latency for SMA computations"
> - "Implemented real-time WebSocket streaming serving 100+ updates/second"
> - "Designed order matching algorithm with price-time priority queues"

---

**Ready to begin?** Please review and approve this plan, and I'll start with Phase 1! 🚀
