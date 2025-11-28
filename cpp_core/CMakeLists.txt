cmake_minimum_required(VERSION 3.15...3.26)
project(trade_engine)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Optimization flags
if(MSVC)
    add_compile_options(/W4 /O2)
else()
    add_compile_options(-Wall -Wextra -O3)
endif()

# Find Python and pybind11
find_package(Python COMPONENTS Interpreter Development REQUIRED)
find_package(pybind11 CONFIG REQUIRED)

# Create Python extension module
pybind11_add_module(trade_engine
    src/engine.cpp
    src/bindings.cpp
)

# Include directories
target_include_directories(trade_engine PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/include
)

# Enable testing
enable_testing()

# Add Google Test if available (for C++ unit tests)
find_package(GTest QUIET)
if(GTest_FOUND)
    add_executable(test_engine
        tests/test_engine.cpp
        src/engine.cpp
    )
    
    target_include_directories(test_engine PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/include
    )
    
    target_link_libraries(test_engine
        GTest::GTest
        GTest::Main
    )
    
    add_test(NAME EngineTests COMMAND test_engine)
    
    message(STATUS "Google Test found - C++ tests enabled")
else()
    message(STATUS "Google Test not found - C++ tests disabled (install with: pip install pytest)")
endif()

# Installation settings
install(TARGETS trade_engine LIBRARY DESTINATION .)
