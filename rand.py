#! /usr/bin/env python3
#
#	Copyright 2014 Sean Hewitt <contact@SeanHewitt.com>
#	
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#	
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#	
#	You should have received a copy of the GNU General Public License
#	along with this program.  If not, see <http://www.gnu.org/licenses/>.
#	

from random import random

def weighted_choice(choices):
	r = random() * sum(choices)
	for i, w in enumerate(choices):
		r -= w
		if r < 0:
			return i
	return None

if __name__ == "__main__":
	print("Weighted choice:",end=" ")
	for i in range(10):
		print(weighted_choice([33,77,11,80,44,33,77,55,99,22,66,88]),end=" ")
	print()
