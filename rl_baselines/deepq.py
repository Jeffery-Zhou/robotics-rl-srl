from baselines import deepq
from baselines.common import set_global_seeds
from baselines import logger

import environments.kuka_button_gym_env as kuka_env
from pytorch_agents.envs import make_env

def customArguments(parser):
    parser.add_argument('--prioritized', type=int, default=1)
    parser.add_argument('--dueling', type=int, default=1)
    return parser


def main(args, callback):
    logger.configure()
    set_global_seeds(args.seed)
    env = make_env(args.env, 0, 0, args.log_dir, pytorch=False)()
    if args.srl_model != "":
        model = deepq.models.mlp([64])
    else:
        # Atari CNN
        model = deepq.models.cnn_to_mlp(
            convs=[(32, 8, 4), (64, 4, 2), (64, 3, 1)],
            hiddens=[256],
            dueling=bool(args.dueling),
        )

    act = deepq.learn(
        env,
        q_func=model,
        lr=1e-4,
        max_timesteps=args.num_timesteps,
        buffer_size=10000,
        exploration_fraction=0.1,
        exploration_final_eps=0.01,
        train_freq=4,
        learning_starts=500,
        target_network_update_freq=500,
        gamma=0.99,
        prioritized_replay=bool(args.prioritized),
        print_freq=10,  # Print every 10 episodes
        callback=callback
    )
    act.save(args.log_dir + "deepq_model.pkl")
    env.close()
