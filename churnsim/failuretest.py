import simpy
import random

ball_wait = random.expovariate(20)

def racket(env, name, ball):
    while True:
        # Let the first user catch the ball
        with ball.request() as req:  # Create a waiting resource
            yield req   # Wait and get the ball

            # The time it takes for the ball to arrive. This can
            # be used to plan the strategy of how to hit the ball.
            yield env.timeout(ball_wait)
            print(env.now, name)

        # "Sleep" to get the other user have his turn.
        yield env.timeout(0)

env = simpy.Environment()
ball = simpy.Resource(env, capacity = 1)

env.process(racket(env, 'Ping', ball))
env.process(racket(env, 'Pong', ball))

env.run(until=10)
print('Done!')
