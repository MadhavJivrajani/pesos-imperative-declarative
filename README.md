# Imperative vs. Declarative Systems

You can find the talk where this demo was used [here](https://www.youtube.com/watch?v=nz99WrdgRuA&feature=youtu.be)!

## Running the demos

### Declarative System

```
python declarative.py <num. of processes>
```
To see the system reconciling, open up another terminal and run
```
kill -9 <one of the PIDs seen in logs>
```

### Imperative System
```
python imperative.py <num. of processes>
```

Open up a new terminal and run
```
curl 127.0.0.1:8080/init
ctrl + c
```

To give the command to spawn processes, run:
```
curl 127.0.0.1:8080/spawn
```

Note that the state of the system reaches `STABLE` after you execute the `spawn` command `<num. of processes>` times. 

## Resources
- The slides for this talk can be found [here](https://github.com/MadhavJivrajani/pesos-imperative-declarative/blob/main/assets/Imperative%20vs%20Declarative%20Systems.pdf).
- This talk was part of our community meetups at PESOS. Check out our community [here](https://pesos.github.io/)!

## Contributing
- Feel free to extend this demo in any way you like! All you need to do is open an issue :smile: