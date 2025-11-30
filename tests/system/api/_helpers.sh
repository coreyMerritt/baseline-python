export log_path="/tmp/projectname-exit-test.log"

function cleanup(){
  killServer
  rm -rf "$log_path"
}

function killServer() {
  pid=$(ss -lntp | awk -F 'pid=' '/:8000/ { split($2, a, ","); print a[1] }') || true
  if [[ -n "$pid" ]]; then
    kill "$pid"
  fi
}

function startServer() {
  killServer
  bash "./start-server.sh" "run" "server" "--host" "127.0.0.1" "--port" "8000" "test" > "$log_path" 2>&1 &
}