# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 11:34:57 2014

@author: pruvolo
"""

# you do not have to use these particular modules, but they may help
from random import randint
import Image
import math
# import pygame

base_fs = ["x", "y"]
other_fs = ["prod", "avg", "cos_pi", "sin_pi", "sigmoid"]
all_fs = base_fs + other_fs

end_base = len(base_fs) - 1
end_other = len(other_fs) - 1
end_all = len(all_fs) - 1

def build_random_function(min_depth, max_depth):
    """ Builds a random symoblic function with depth falling between
    min_depth and max_depth

    Inputs:
        min_depth: minimum number of recursive calls
        max_depth: maximum number of recursive calls

    Returns:
        A list in the form of ["func", a, b] where a and b are nested lists
    """
    
    if min_depth == 1:
        
        if max_depth == 1:
            # we MUST return "x" or "y"
            return [base_fs[randint(0,end_base)]]
        else:
            # we CAN return "x" or "y"    
            func = all_fs[randint(0,end_all)]
            if func == "x" or func == "y":
                return [func]
            elif func == "prod" or func == "avg":
                return [ func , build_random_function(min_depth, max_depth - 1), build_random_function(min_depth, max_depth - 1) ]
            else:   
                return [func, build_random_function(min_depth, max_depth - 1)]
    else: 
        # we CANNOT return "x" or "y" yet
        return [other_fs[randint(0,end_other)] , build_random_function(min_depth - 1, max_depth -1), build_random_function(min_depth - 1, max_depth -1)]

def evaluate_random_function(f, x, y):
    """ Evaluates a symbolic function f for x, y in [-1,1] 

    Inputs:
        f: symbolic function 
        x: float btwn [-1,1]
        y: float btwn [-1,1]

    Returns:
        float btwn [-1,1]
    """

    if f[0] == "x":
        return x
    elif f[0] == "y":
        return y
    else:
        if f[0] == "prod":
            return evaluate_random_function(f[1], x, y) * evaluate_random_function(f[2], x, y)
        elif f[0] == "avg":
            return (evaluate_random_function(f[1], x, y) + evaluate_random_function(f[2], x, y)) / 2.0
        elif f[0] == "cos_pi":
            return math.cos(math.pi*evaluate_random_function(f[1], x, y))
        elif f[0] == "sin_pi":
            return math.sin(math.pi*evaluate_random_function(f[1], x, y))
        elif f[0] == "**2":
            return evaluate_random_function(f[1], x, y)**2
        elif f[0] == "sigmoid":
            return 1.0 / (1 + math.exp(-(evaluate_random_function(f[1], x, y)))) - .5

def remap_interval(val, input_interval_start, input_interval_end, output_interval_start, output_interval_end):
    """ Maps the input value that is in the interval [input_interval_start, input_interval_end]
    to the output interval [output_interval_start, output_interval_end].  The mapping
    is an affine one (i.e. output = input*c + b).

    inputs:
        val: value, based on input domain
        input_interval_start: min value of input domain
        input_interval_end: max value of input domain
        output_interval_start: min value of output domain
        output_interval_end: max value of output domain

    returns:
        remapped value of input domain to output domain
    """ 

    percentile = float(val - input_interval_start) / (input_interval_end - input_interval_start) 
    return percentile*(output_interval_end - output_interval_start) + output_interval_start

if __name__ == "__main__":
    fred = build_random_function(5,17)
    fgreen = build_random_function(5,17)
    fblue = build_random_function(5,17)

    print "red(x,y): \n", fred
    print "green(x,y): \n", fgreen
    print "blue(x,y): \n", fblue


    def red(x,y): 
        val = evaluate_random_function(fred, x, y)
        return int(remap_interval(val, -1, 1, 0, 255))

    def green(x,y): 
        val = evaluate_random_function(fgreen, x, y)
        return int(remap_interval(val, -1, 1, 0, 255))
    
    def blue(x,y): 
        val = evaluate_random_function(fblue, x, y)
        return int(remap_interval(val, -1, 1, 0, 255))


    im = Image.new("RGB", (350, 350))
    horz, vert = im.size

    for i in xrange(horz):
        x = remap_interval(i, 0, horz-1, -1, 1)
        for j in xrange(vert):
            y = remap_interval(j, 0, vert-1, -1, 1)
            im.putpixel((i,j), (red(x,y), green(x,y), blue(x,y)))

    im.save("image.bmp")

    # pygame.init()
    # size = width,height= (im.get_rect().width,im.get_rect().height)
    # screen = pygame.display.set_mode(size)
    # screen.blit(im,im.get_rect())
    # pygame.display.flip()