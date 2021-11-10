function inside --description="Run a command in a directory"
    if [ (count $argv) -lt 2 ]
        return 1
    end

    set -l dir $argv[1]
    set -l cmd $argv[2..-1]

    # Change to the target directory
    set -l curr_dir (pwd)
    cd $dir
    set -l rc $status
    if [ $rc -ne 0 ]
        return $rc
    end

    # Run the the command
    eval $cmd
    set -l rc $status
    if [ $rc -ne 0 ]
        return $rc
    end
    set -l exit_code $rc

    # Change the directory back
    cd $curr_dir

    return $exit_code
end
