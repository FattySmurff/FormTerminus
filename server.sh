#!/usr/bin/env bash

echo
echo ===========================================================================
echo 'Starting dev server'
echo ===========================================================================
echo

cd webapp
.env/bin/python app.py
