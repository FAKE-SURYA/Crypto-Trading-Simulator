# Setup Instructions

This document provides detailed setup instructions for different environments.

## Table of Contents
1. [Windows Setup](#windows-setup)
2. [Linux/Mac Setup](#linux-mac-setup)
3. [Troubleshooting](#troubleshooting)

---

## Windows Setup

### Install Visual Studio Build Tools (Required for C++ Compilation)

1. Download [Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/)
2. Run the installer and select:
   - ✅ Desktop development with C++
   - ✅ C++ CMake tools for Windows
3. Restart your computer

### Install Python Dependencies

```powershell
# Install pybind11 and build tools
pip install scikit-build cmake pybind11

# Build C++ module
cd cpp_core
pip install .

# Verify installation
python -c "import trade_engine; print('Success!')"
```

### Install Backend Dependencies

```powershell
cd backend
pip install -r requirements.txt
```

### Install Frontend Dependencies

```powershell
cd frontend
npm install
```

### Run the Application

```powershell
# Terminal 1: Start backend
cd backend
uvicorn main:app --reload

# Terminal 2: Start frontend
cd frontend
npm run dev
```

---

## Linux/Mac Setup

### Install System Dependencies

**Ubuntu/Debian**:
```bash
sudo apt-get update
sudo apt-get install -y build-essential cmake python3-dev
```

**Mac OS**:
```bash
brew install cmake python@3.11
```

### Install Python Dependencies

```bash
# Install build tools
pip3 install scikit-build cmake pybind11

# Build C++ module
cd cpp_core
pip3 install .

# Verify
python3 -c "import trade_engine; print('Success!')"
```

### Install Backend Dependencies

```bash
cd backend
pip3 install -r requirements.txt
```

### Install Frontend Dependencies

```bash
cd frontend
npm install
```

### Run the Application

```bash
# Terminal 1: Backend
cd backend
uvicorn main:app --reload

# Terminal 2: Frontend
cd frontend
npm run dev
```

---

## Troubleshooting

### C++ Module Import Error

**Error**: `ImportError: No module named 'trade_engine'`

**Solution**:
```bash
cd cpp_core
pip install . --force-reinstall
```

### CMake Not Found

**Windows**:
```powershell
pip install cmake
```

**Linux/Mac**:
```bash
sudo apt-get install cmake  # Ubuntu
brew install cmake          # Mac
```

### Python Version Issues

Ensure you're using Python 3.8+:
```bash
python --version  # Should be 3.8 or higher
```

### Port Already in Use

If port 8000 or 3000 is in use:

**Backend** (change port):
```bash
uvicorn main:app --port 8001
```

**Frontend** (change port):
```bash
# Edit package.json: "dev": "next dev -p 3001"
npm run dev
```

### WebSocket Connection Failed

1. Ensure backend is running on port 8000
2. Check firewall settings
3. Verify WebSocket URL in `frontend/hooks/useWebSocket.ts`

### Docker Build Fails

```bash
# Clean and rebuild
docker-compose down
docker system prune -a
docker-compose up --build
```

---

## Running Tests

### C++ Tests (requires Google Test)

```bash
cd cpp_core/build
cmake ..
make
ctest -V
```

### Python Tests

```bash
cd tests/python
pip install -r requirements.txt
pytest test_api.py -v
```

### Benchmarks

```bash
cd benchmarks
python sma_benchmark.py
python plot_results.py
```

---

## Performance Tips

1. **Build C++ in Release Mode**:
   ```bash
   cd cpp_core/build
   cmake -DCMAKE_BUILD_TYPE=Release ..
   make
   ```

2. **Use Production Build for Frontend**:
   ```bash
   cd frontend
   npm run build
   npm start
   ```

3. **Enable CPU Optimizations**:
   Edit `cpp_core/CMakeLists.txt`:
   ```cmake
   set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O3 -march=native")
   ```

---

Need more help? Open an issue on GitHub!
