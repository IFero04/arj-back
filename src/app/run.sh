#!/bin/bash
if [ "$USE_DEV_MODE" = "true" ];
    then fastapi dev main.py --proxy-headers --host 0.0.0.0 --port $API_PORT_INTERNAL; 
    else fastapi run main.py --proxy-headers --port $API_PORT_INTERNAL;
fi

echo "Executed script at $(date)"