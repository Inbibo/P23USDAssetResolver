REM Clear current session log 
cls
REM Define Resolver > Has to be one of 'fileResolver'/'pythonResolver'/'cachedResolver'/'httpResolver'
set AR_RESOLVER_NAME=cachedResolver
REM Define App
set AR_DCC_NAME=MAYA
set MAYA_USD_SDK_ROOT=<path_to_autodesk_install>\MayaUSD\Maya2024\0.25.0\mayausd\USD
set MAYA_USD_SDK_DEVKIT_ROOT=<path_to_autodesk_install>\MayaUSD\Maya2024\0.25.0\mayausd\USD\devkit
set PYTHON_ROOT=<path_to_python_root_folder>
REM Clear existing build data and invoke cmake
rmdir /S /Q build
rmdir /S /Q dist/%AR_DCC_NAME%
cmake . -B build -G "Visual Studio 16 2019" -A x64 -T v142
cmake --build build  --clean-first --config Release
cmake --install build