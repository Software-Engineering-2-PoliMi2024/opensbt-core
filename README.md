# Useful stuff to know

# Simulator service
The simulator is now available as a service. To run it you just need to do:
```bash
docker compose up
```

This will launch the simulation server exposing the necessary APIs @ http://0.0.0.0:8000

To see the OpenApi documentation you can go to [/docs](http://127.0.0.1:8000/docs)

You can enqueue a simulation by posting the simulation to `/simulate`. This will return a jobId. You can then check the status/result of the simulation with a get request to `/simulate/{job_id}`

