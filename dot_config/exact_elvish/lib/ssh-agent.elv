use re
use util

# The path to the SSH agent environment configuration to use.
var environment-path = $E:HOME/.ssh/environment

# Check that an SSH agent pid and socket exist.
fn is-running { |pid sock|
  and (util:is-user-process $pid) (util:path-exists $sock)
}

# Read the SSH environment variables from the environment configuration.
fn read-environment-variables {
  var text = (e:cat $environment-path | slurp)
  var pid = (re:find 'SSH_AGENT_PID=(.+?);' $text)[groups][1][text]
  var sock = (re:find 'SSH_AUTH_SOCK=(.+?);' $text)[groups][1][text]
  put [&pid=$pid &sock=$sock]
}

# Read the SSH agent environment. If there is no environment then a new SSH
# agent is started.
fn read-environment {
  # If the environment does not exist then start a new SSH agent
  if (not (util:file-exists $environment-path)) {
    e:ssh-agent -s > $environment-path
  }
  # Get the SSH environment variables
  var env = (read-environment-variables)
  if (not (is-running $env[pid] $env[sock])) {
    # Start the SSH agent and try reading the environment again
    e:ssh-agent -s > $environment-path
    set env = (read-environment-variables)
  }
  put $env
}

# Initialize an SSH agent. If an SSH agent is already running, then the
# environment will be set up to use it.
fn init {
  var env = (read-environment)
  set E:SSH_AGENT_PID = $env[pid]
  set E:SSH_AUTH_SOCK = $env[sock]
}

# Show some information about the current SSH agent configuration.
fn info {
  if (and (has-env SSH_AGENT_PID) (has-env SSH_AUTH_SOCK)) {
    echo "SSH agent ("$E:SSH_AGENT_PID") running on "$E:SSH_AUTH_SOCK"."
  } else {
    echo "SSH agent not configured."
  }
}

# Kill all SSH agents and clear the SSH environment configuration. This should
# probably not be used.
fn kill-all {
  nop ?(e:pkill ssh-agent)
  e:rm $environment-path
  del E:SSH_AGENT_PID
  del E:SSH_AUTH_SOCK
}
