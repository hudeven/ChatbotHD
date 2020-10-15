#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
"""
Script for safety protected interaction between a local human keyboard input and a
trained model.
"""

from parlai.core.params import ParlaiParser
from parlai.core.script import ParlaiScript, register_script
from parlai.core.agents import create_agent
from parlai.core.worlds import create_task
from parlai.agents.safe_local_human.safe_local_human import SafeLocalHumanAgent
import parlai.utils.logging as logging
import random


def setup_args(parser=None):
    if parser is None:
        parser = ParlaiParser(True, True, 'Like interactive, but adds a safety filter')
    parser.add_argument('-d', '--display-examples', type='bool', default=False)
    parser.add_argument(
        '--display-prettify',
        type='bool',
        default=False,
        help='Set to use a prettytable when displaying '
        'examples with text candidates',
    )
    parser.add_argument(
        '--display-ignore-fields',
        type=str,
        default='label_candidates,text_candidates',
        help='Do not display these fields',
    )
    parser.add_argument(
        '-it',
        '--interactive-task',
        type='bool',
        default=True,
        help='Create interactive version of task',
    )
    parser.set_defaults(interactive_mode=True, task='interactive')
    SafeLocalHumanAgent.add_cmdline_args(parser)
    return parser


agent = None


def safe_interactive(opt):
    if isinstance(opt, ParlaiParser):
        logging.error('interactive should be passed opt not Parser')
        opt = opt.parse_args()

    # Create model and assign it to the specified task
    global agent
    agent = create_agent(opt, requireModelExists=True)
    agent.opt.log()
    # human_agent = SafeLocalHumanAgent(opt)
    # world = create_task(opt, [human_agent, agent])

    # Interact until episode done
    # while True:
    #     world.parley()
    #     bot_act = world.get_acts()[-1]
    #     if 'bot_offensive' in bot_act and bot_act['bot_offensive']:
    #         agent.reset()
    #
    #     if opt.get('display_examples'):
    #         print('---')
    #         print(world.display())
    #     if world.epoch_done():
    #         logging.info('epoch done')
    #         break


def get_answer(text):
    reply = {'episode_done': False, 'text': text}
    agent.observe(reply)
    model_res = agent.act()
    print(model_res["text"])
    return model_res["text"]


@register_script('safe_interactive')
class SafeInteractive(ParlaiScript):
    @classmethod
    def setup_args(cls):
        return setup_args()

    def run(self):
        return safe_interactive(self.opt)


if __name__ == '__main__':
    random.seed(42)
    SafeInteractive.main("-mf", "zoo:blender/blender_90M/model", "-t", "blended_skill_talk")
    for text in ["hello", "good !"]:
        print(get_answer(text))

