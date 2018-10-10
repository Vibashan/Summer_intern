#!/usr/bin/env python

import rl_env_pur_eva as env
import cv2
import numpy as np
import time

def main():
	i = 0
	game = env.pur_eva()
	while(1):
		x_t, r_0, terminal = game.game_state(i)
		print('r',r_0,'T',terminal)
		i = i+1
		if i == 350:
			i = 0
if __name__ == "__main__":
	main()