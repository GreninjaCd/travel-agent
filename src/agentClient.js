const { spawn } = require("child_process");
const path = require("path");

/**
 * Wrapper to call Python CLI (agent_cli.py) and return parsed JSON response
 * This explicitly forwards environment variables (including OPENAI_API_KEY)
 * to the child Python process and prefers the project's venv python when present.
 */
async function callPythonAgent(request) {
  return new Promise((resolve, reject) => {
    const projectRoot = path.join(__dirname, "..");
    const pythonScriptPath = path.join(projectRoot, "app", "agent_cli.py");

    // Prefer a provided PYTHON_EXEC or the virtualenv python inside the project, else fall back to 'python'
    const venvPython = path.join(projectRoot, ".venv", "Scripts", "python.exe");
    const pythonExec = process.env.PYTHON_EXEC || venvPython;

    // Build environment for child process — inherit all current env vars and ensure OPENAI_API_KEY is forwarded
    const childEnv = { ...process.env };

    // If pythonExec does not exist on filesystem, fallback to 'python'
    const fs = require('fs');
    const execToUse = fs.existsSync(pythonExec) ? pythonExec : (process.env.PYTHON_EXEC || 'python');

    const pythonProcess = spawn(execToUse, [pythonScriptPath], {
      cwd: projectRoot,
      env: childEnv,
      stdio: ['pipe', 'pipe', 'pipe']
    });

    let stdout = "";
    let stderr = "";

    pythonProcess.stdout.on("data", (data) => {
      stdout += data.toString();
    });

    pythonProcess.stderr.on("data", (data) => {
      stderr += data.toString();
    });

    pythonProcess.on("close", (code) => {
      if (code !== 0) {
        reject(new Error(`Python process exited with code ${code}: ${stderr}`));
      } else {
        try {
          const result = JSON.parse(stdout);
          resolve(result);
        } catch (e) {
          reject(new Error(`Failed to parse Python output: ${e.message}\nStdout:${stdout}\nStderr:${stderr}`));
        }
      }
    });

    // Send request to Python stdin
    pythonProcess.stdin.write(JSON.stringify(request));
    pythonProcess.stdin.end();
  });
}

module.exports = { callPythonAgent };
