#!/usr/bin/env python3
"""
Server lifecycle manager for Playwright tests.

Usage:
    python with_server.py --help
    python with_server.py "npm run dev" --port 3000 --test "python test_app.py"
    python with_server.py "npm start" --port 3000 --url http://localhost:3000/health

This script:
1. Starts a development server
2. Waits for it to be ready (via port or URL check)
3. Runs your test command
4. Cleans up the server regardless of test outcome
"""

import argparse
import os
import signal
import socket
import subprocess
import sys
import time
import urllib.request
import urllib.error


def wait_for_port(port: int, host: str = 'localhost', timeout: int = 60) -> bool:
    """Wait for a port to become available."""
    start = time.time()
    while time.time() - start < timeout:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            sock.connect((host, port))
            sock.close()
            return True
        except (socket.error, socket.timeout):
            time.sleep(0.5)
    return False


def wait_for_url(url: str, timeout: int = 60) -> bool:
    """Wait for a URL to return 2xx status."""
    start = time.time()
    while time.time() - start < timeout:
        try:
            response = urllib.request.urlopen(url, timeout=5)
            if 200 <= response.status < 300:
                return True
        except (urllib.error.URLError, urllib.error.HTTPError):
            time.sleep(0.5)
    return False


def run_with_server(
    server_cmd: str,
    port: int,
    test_cmd: str = None,
    health_url: str = None,
    timeout: int = 60,
    cwd: str = None,
    shell: bool = True
) -> int:
    """
    Start a server, wait for it, run tests, and clean up.
    
    Returns the exit code of the test command (or 0 if no test command).
    """
    server_process = None
    
    try:
        # Start the server
        print(f"🚀 Starting server: {server_cmd}")
        server_process = subprocess.Popen(
            server_cmd,
            shell=shell,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            preexec_fn=os.setsid if hasattr(os, 'setsid') else None
        )
        
        # Wait for server to be ready
        print(f"⏳ Waiting for server on port {port}...")
        
        if health_url:
            ready = wait_for_url(health_url, timeout=timeout)
        else:
            ready = wait_for_port(port, timeout=timeout)
        
        if not ready:
            print(f"❌ Server failed to start within {timeout}s")
            return 1
        
        print(f"✅ Server is ready on port {port}")
        
        # Run test command if provided
        if test_cmd:
            print(f"🧪 Running tests: {test_cmd}")
            result = subprocess.run(test_cmd, shell=True, cwd=cwd)
            return result.returncode
        else:
            print("ℹ️  No test command provided. Server is running.")
            print("   Press Ctrl+C to stop.")
            server_process.wait()
            return 0
            
    except KeyboardInterrupt:
        print("\n⚠️  Interrupted by user")
        return 130
        
    finally:
        # Clean up server process
        if server_process and server_process.poll() is None:
            print("🧹 Stopping server...")
            try:
                if hasattr(os, 'setsid'):
                    os.killpg(os.getpgid(server_process.pid), signal.SIGTERM)
                else:
                    server_process.terminate()
                server_process.wait(timeout=5)
            except Exception:
                if hasattr(os, 'setsid'):
                    os.killpg(os.getpgid(server_process.pid), signal.SIGKILL)
                else:
                    server_process.kill()
            print("✅ Server stopped")


def main():
    parser = argparse.ArgumentParser(
        description='Run a server and execute tests against it',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Start Next.js dev server and run Playwright tests
  python with_server.py "npm run dev" --port 3000 --test "pytest tests/"
  
  # Start server with health check URL
  python with_server.py "npm start" --port 8080 --url http://localhost:8080/api/health --test "python test.py"
  
  # Just start server (useful for manual testing)
  python with_server.py "npm run dev" --port 3000
        """
    )
    
    parser.add_argument('server_cmd', help='Command to start the server')
    parser.add_argument('--port', '-p', type=int, required=True, help='Port to wait for')
    parser.add_argument('--test', '-t', dest='test_cmd', help='Test command to run')
    parser.add_argument('--url', '-u', dest='health_url', help='Health check URL (optional)')
    parser.add_argument('--timeout', type=int, default=60, help='Startup timeout in seconds (default: 60)')
    parser.add_argument('--cwd', help='Working directory for commands')
    
    args = parser.parse_args()
    
    exit_code = run_with_server(
        server_cmd=args.server_cmd,
        port=args.port,
        test_cmd=args.test_cmd,
        health_url=args.health_url,
        timeout=args.timeout,
        cwd=args.cwd
    )
    
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
