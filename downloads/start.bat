@echo off
set Disk=y
subst %Disk%: "data"

%Disk%:

set HomePath=%Disk%:\home_ipv6
set HomeDrive=%Disk%:\home_ipv6
set Home=%Disk%:\home_ipv6
set USERPROFILE=%Disk%:\home_ipv6

REM 將系統 Python 程式的 io 設為 utf-8
set PYTHONIOENCODING="utf-8"

set PYTHONPATH=%Disk%:\Python313\DLLs;%Disk%:\Python313\Lib;%Disk%:\Python313\Lib\site-packages;%Disk%:\Webots_2025a\msys64\mingw64\bin;%Disk%:\Webots_2025a\lib\controller\python;%Disk%:\NX\NXBIN\python;
set PYTHONHOME=%Disk%:\Python313
REM for Webots
set PYTHON_PATH=%Disk%:\Python313
set WEBOTS_HOME=%Disk%:\Webots_2025a

REM for putty
set GIT_SSH=%Disk%:\PuTTY\plink.exe

REM for Java and Android SDK
set java_home=%Disk%:\java\jdk8u222-b10
set ANDROID_SDK_home=%Disk%:\home_ipv6
set GRADLE_USER_home=%Disk%:\home_ipv6
set ANDROID_SDK_ROOT=%Disk%:\android\sdk
set ANDROID_Home=%Disk%:\android\sdk
set REPO_OS_OVERRIDE=windows

REM 設定跟 Python 有關的命令搜尋路徑
set path_python=%Disk%:\Python313;%Disk%:\Python313\Scripts;
REM 設定跟Git 有關的命令搜尋路徑
set path_git=%Disk%:\portablegit\bin;
REM 設定 msys2 64 位元的執行路徑
REM %Disk%:\msys64\mingw64\bin is for GD library
set path_msys2=%Disk%:\msys64\ucrt64\bin;%Disk%:\msys64\mingw64\bin;
REM set for LaTeX
set path_miketex=%Disk%:\miktex-portable\texmfs\install\miktex\bin\x64;
REM Flutter path
set path_flutter=%Disk%:\flutter\bin;%java_home%\bin;%Disk%:\Android\sdk;%Disk%:\Android\sdk\tools;%Disk%:\Android\sdk\tools\bin;%Disk%:\Android\sdk\emulator;%Disk%:\Android\sdk\platform-tools;%Disk%:\flutter\bin\cache\dart-sdk\bin;%Disk%:\vscode;
set path_node=%Disk%:\node-v14.15.4-win-x64;

set path_postgresql=%Disk%:\postgresql13\bin;
set path_range=%Disk%:\Range3_official\bin;
rem set path_range=%Disk%:\range-3.2.5_kmol\bin;
set path_lua=%Disk%:\lua-5.3.5\;
set path_core=%Disk%:\coreutils-5.3.0\bin;
REM for gogs
set path_putty=%Disk%:\PuTTY;
set path_vscode=%Disk%:\vscode;

REM for Rust
set MINGW_PATH=%path_msys2%;
set GIT_PATH=%path_git%;
set VSCODE_PATH=%path_vscode%
set RUSTUP_HOME=%Disk%:\Rust\rust
set CARGO_HOME=%Disk%:\Rust\cargo
set RUST_PATH=%CARGO_HOME%\bin

REM for Erlang and Elixir
set path_erlang=%Disk%:\elixir\erl10.7\bin\;%Disk%:\elixir\erl10.7\erts-10.7\bin;%Disk%:\elixir\elixir\bin;
set ERTSPATH=%Disk%:\elixir\erl10.7\erts-10.7\bin
set ERLINI=%Disk%:\elixir\erl10.7\erts-10.7\bin\erl.ini

REM for Haskell
set path_haskell=%Disk%:\ghc-9.0.1-x86_64-unknown-mingw32\bin;
REM for node.js
set path_nodejs=%Disk%:\node-v14.17.2-x64\nodejs;%Disk%:\node-v14.17.2-x64\nodejs\node_modules\npm;

REM 加入 PostgreSQL 所需的環境變數設定

@SET PGDATA=%Disk%:\postgresql13\data
@SET PGDATABASE=postgres
@SET PGUSER=postgres
@SET PGPORT=5432
@SET PGLOCALEDIR=%Disk%:\postgresql13\share\locale

REM for Range3
REM REG IMPORT %Disk%:\range3.reg

REM proxy needed for heroku login
REM proxy can not use with fossil scm
REM proxy can not use with Rust installation
REM needed for node.js
REM set HTTP_PROXY=http://[2001:288:6004:xx::42]:3128
REM set HTTPS_PROXY=http://[2001:288:6004:xx::42]:3128

REM for PyRep
set VREP_PATH=%Disk%:\CoppeliaSim

REM BOOST_ROOT for compiling coppeliasim but maybe not for linking
REM set BOOST_ROOT=%Disk%:\boost_1_76_0\;
set path_copsim=%Disk%:\boost_1_76_0\;%Disk%:\Strawberry\perl\bin;%Disk%:\cmake-3.21.0-windows-x86_64\bin;%Disk%:\diffutils-2.8.7-1\bin;%Disk%:\patch-2.5.9-7\bin;%D%:\jom_1_1_2;%Disk%:\LLVM\bin;%Disk%:\QtCreator\bin;%Disk%:\CoppeliaSimEdu;%Disk%:\Python313\tcl\tcl8.6;

REM for CMake
set CMAKE_C_COMPILER=%Disk%:\msys64\ucrt64\bin\gcc;
set CMAKE_CXX_COMPILER=%Disk%:\msys64\ucrt64\bin\g++;

REM set QT_QPA_PLATFORM_PLUGIN_PATH=Y:\msys64_20240507\mingw64\share\qt5\plugins\platforms
REM set QT_PLUGIN_PATH=Y:\msys64_20240507\mingw64\share\qt5\plugins

REM for execute scite directly
set path_scite=%Disk%:\wscite\;

REM for simExtZMQ
set path_xsltproc=%Disk%:\xsltproc;

REM for OpenSSL
Set OPENSSL_CONF=%Disk%:\OpenSSL-Win64\SSL\openssl.cnf
set path_openssl=%Disk%:\OpenSSL-Win64\bin;

REM for textract
set path_poppler=%Disk%:\poppler-24.07.0\Library\bin;

REM for tiny C compiler
set path_tcc=%Disk%:\tcc;

REM for webots
set  path_webots=%Disk%:\Webots_2025a\msys64\mingw64\bin;%Disk%:\Webots_2025a\msys64\usr\bin

REM for blender
set path_blender=%Disk%:\Blender 4.2;

path=%Disk%:;%path_python%;%path_git%;%path_copsim%;%path_msys2%;%path_miketex%;%path_flutter%;%path_node%;%path_tcc%;%path_postgresql%;%path_range%;%path_lua%;%path_core%;%path_putty%;%path_vscode%;%RUST_PATH%;%path_erlang%;%path_nodejs%;%path_haskell%;%path_scite%;%path_xsltproc%;%path_gnuplot%;%path_openssl%;%path_poppler%;%path_webots%;%path_blender%;%path%;

REM for NX2312, must after path setup 
set SPLM_LICENSE_SERVER=29000@your_server
set UGII_LANG=english
set UGS_LICENSE_BUNDLE=ACD11,ACD10
set UGII_BASE_DIR=%Disk%:\NX\
set UGII_TMP_DIR=%Disk%:\NX\temp
set UGII_LIB_PATH=%Disk%:\NX\NXBIN\python
set ugii=%Disk%:\NX\ugii;%Disk%:\NX\nxbin;
path = %ugii%;%path%
REM Xcopy %Disk%:\home_ipv6\AppData\Local\Siemens\NX2312 C:\users\%USERNAME%\AppData\Local\Siemens\NX2312 /E /H /C /I /Y

REM start ugraf -nx

REM python %Disk%:\tmp\nx_ex\new_part.py

start /MIN cmd.exe
start /MIN cmd.exe
start /MIN cmd.exe
start /MIN cmd.exe

start /MIN %Disk%:\wscite\SciTE.exe
start /MIN %Disk%:\wscite\SciTE.exe

start webotsw.exe


Exit
