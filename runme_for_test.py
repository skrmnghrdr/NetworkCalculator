#!/usr/bin/python3

#hey, i'm using vim okay.


"""
git add (things)
git status (to see status)
git commit -m "define what milestone did you accomplish on this commit"
git push origin main (push to git site)
"""

import Hostcalculator


a = Hostcalculator.hosts(verbose=True).cidr_to_fullmask(2)
b = Hostcalculator.hosts
pass