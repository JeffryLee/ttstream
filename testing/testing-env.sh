sudo sysctl -w net.ipv4.ip_forward=1
mm-delay 1 mm-link networktrace/traces/TMobile-UMTS-driving.up networktrace/traces/TMobile-UMTS-driving.down --downlink-queue=droptail --downlink-queue-args="bytes=150000" --uplink-queue=infinite
tmux new -s abr
tmux split-window -h