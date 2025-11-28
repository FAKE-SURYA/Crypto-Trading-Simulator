"""
High-Performance Crypto Trading Simulator - C++ Engine
Build script using scikit-build for cross-platform compatibility
"""

from skbuild import setup
from pathlib import Path

# Read README if it exists
readme_file = Path(__file__).parent.parent / "README.md"
long_description = "High-performance cryptocurrency trading engine with C++ core"
if readme_file.exists():
    long_description = readme_file.read_text(encoding="utf-8")

setup(
    name="trade_engine",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="High-performance C++ trading engine for cryptocurrency simulation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/crypto-trading-simulator",
    license="MIT",
    
    # Package configuration
    packages=[],  # Pure C++ extension, no Python packages
    python_requires=">=3.8",
    
    # Build requirements
    setup_requires=[
        "scikit-build>=0.17.0",
        "cmake>=3.15",
        "pybind11>=2.10.0",
    ],
    
    # Runtime requirements
    install_requires=[
        "pybind11>=2.10.0",
    ],
    
    # CMake configuration
    cmake_install_dir=".",
    cmake_args=[
        "-DCMAKE_BUILD_TYPE=Release",
    ],
    
    # Classifiers for PyPI
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: C++",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Office/Business :: Financial",
        "Topic :: Software Development :: Libraries",
    ],
    
    # Keywords for discoverability
    keywords="trading cryptocurrency c++ high-performance finance",
)
