# search for Docker containers with the name 'dft'
set dft_containers (docker ps -a -q --filter name=readit2me --filter status=exited)

# remove the found containers
if test (count $dft_containers) -gt 0
    docker rm $dft_containers
end
