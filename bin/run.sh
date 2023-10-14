#!/bin/bash

if [ "${DIAGNOSTIC_TOOL_HOME}X" =  "X" ]
then
      export DIAGNOSTIC_TOOL_HOME=/opt/tools/diagnostic/DiagnosticTool
fi
cd $DIAGNOSTIC_TOOL_HOME

python3 bin/main.py

