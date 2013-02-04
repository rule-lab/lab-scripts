"""
A script for stylizing PyMOL structures similarly to QuteMol.
"""

from pymol import cmd, util

cmd.set_color('oxygen', [1.0,0.4,0.4])
cmd.set_color('nitrogen', [0.5,0.5,1.0])
cmd.set_color('carbon', [0.2,0.2,0.2])
cmd.set_color('hydrogen', [0.7,0.7,0.7])
cmd.hide('everything')
cmd.show('spheres')
cmd.hide('everything', 'solvent')
util.cbaw
cmd.bg_color(color='white')
cmd.set('light_count', '10')
cmd.set('spec_count', '1')
cmd.set('shininess', '10')
cmd.set('specular', '0.25')
cmd.set('ambient', '0')
cmd.set('direct', '0')
cmd.set('reflect', '1.5')
cmd.set('ray_shadow_decay_factor', '0.1')
cmd.set('ray_shadow_decay_range', '2')
cmd.unset('depth_cue')