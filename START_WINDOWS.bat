@echo off
title D:ROCHILA // DESTROY PROTOCOL
if not exist "node_modules" (
  echo Installing dependencies...
  npm install
)
npm run dev
pause
