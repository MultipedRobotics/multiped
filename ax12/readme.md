# AX-12A Quadruped

Nature loves animals/insects with legs. Even birds have legs! Legs allow for easier
navigation across rough terrain. The more legs you have, the more redundant and
robust you are. If you are a centipede and you break a few legs, no big deal.
However, if you are a human and break one leg, then walking (forget running)
becomes extremely difficult.

In robotics you see many different types of walking robots. Common ones are:
2 legs, four legs, and 6 legs. There are advantages and disadvantages for each
of these types of robots.

- 2 legs
    - balancing and shifting the body's center of mass is critical to the
robot not falling over
    - the 2 legs are generally need to be more powerful to lift the body mass
- 4 legs:
    - there is an inherent stability with this configuration. You only need 3
    legs (tripod) to keep the robot standing, leaving one leg to move freely
    as needed
    - each of the legs can be weaker (which also translates into cost $$$) than
    its 2 legged counter part, but you still have more of them, so it is probably
    still more expensive
    - However, there is still a lot of motors, data lines, coordination complexity
    than if you only had 2 legs
- 6 legs:
    - having more than 4 legs contains all of the same advantages/disadvantages
    of 4 legs
    - you also have more redundancy, essentially able to loose 2 legs and keep
    walking
    - there are also more types of gaits available to you, which is a fancy word
    for how you control your leg moves when walking, trotting, running, etc




![](pics/spider.png)

**Still under development**

- [Mechanical Hardware](mechanical/)
- [Electrical Hardware](electrical/)

MIT License
-----------

**Copyright (c) 2018 Kevin J. Walchko**

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
