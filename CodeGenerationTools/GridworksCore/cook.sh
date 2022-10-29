#!/bin/bash

ssotme -build

cd ../..
black -l 100 python_code
black -l 100 python_test
cd CodeGenerationTools/GridworksCore/

rm -rf SassyMQ
