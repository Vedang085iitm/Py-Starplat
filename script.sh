#!/bin/bash

# Define color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}************************************************ Welcome to the Python to Starplat Translator! ***********************************************${NC}"
echo " "
sleep 1
while true; do
    echo " "
    echo -e "${YELLOW}Please enter one of the following options: PageRank, SSSP, V_Cover, TriangleCounting or type 'q' to quit${NC}"
    echo " "
    echo -n "[> "
    read input
    input=$(echo "$input" | tr '[:upper:]' '[:lower:]')

    case $input in
        "trianglecounting")
            python3 translators/triangleCountingTranslator.py availableGraphs/TriangleCounting.py
            ;;
        "v_cover")
            python3 translators/v_CoverTranslator.py availableGraphs/v_cover.py
           
            ;;
        "pagerank")
            python3 translators/prTranslator.py availableGraphs/PageRank.py
            ;;
        "sssp")
            python3 translators/ssspTranslator.py availableGraphs/SSSP.py
            ;;
        "q")
            echo " "
            echo -e "${RED}*************************************************Exiting the script*********************************************************************${NC}"
            break
            ;;
        *)
            echo -e "${RED}Invalid option. Please enter one of the following: PageRank, SSSP, V_Cover, TriangleCounting or type 'exit' to quit${NC}"
            ;;
    esac
done